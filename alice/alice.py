import logging
import time
import json
from models.memory import Vision, Research, VisionProgress, ResearchProgress, Deepthink, DeepthinkProgress, Status, LLMChatHistory, Id, ProposalBy
from memory.research import ResearchSM
from memory.deepthink import DeepthinkSM
from alice_prompts import AlicePrompts
from llm.llm import defaultLLM
from util.time import get_now_unixtime


class Alice:
    logger = logging.getLogger("Alice")

    KEEP_ACTIVE_RESEARCHS = 5

    def schedule_plan_vision(self):
        todo_visions = Vision.select().where(Vision.status.in_([Status.INIT, Status.ASSIGNED, Status.RESUMED, Status.DOING]))
        for vision in todo_visions:
            self.logger.info("[Alice] schedule_plan_vision, will process vision: {}".format(vision.vision))
            not_active_status = [Status.FAIL, Status.CANCEL, Status.SUSPENDED, Status.DONE]
            researchs = Research.select().where(Research.vision_id == vision.id)
            active_researchs = list(map(lambda x: x.status not in not_active_status, researchs))
            if len(active_researchs) < self.KEEP_ACTIVE_RESEARCHS:
                need_researchs = self.KEEP_ACTIVE_RESEARCHS - len(active_researchs)
            else:
                need_researchs = 0
            if need_researchs > 0:
                self.logger.info("[Alice] schedule_plan_vision, Plan research for vision: {}".format(vision.vision))
                self.plan_vision(vision, need_researchs, researchs)


    def plan_vision(self, vision, plan_cnt, current_researchs):
        bad_case = ""
        good_case = ""
        for reseach in current_researchs:
            if reseach.status in [Status.REJECTED_PROPOSAL]:
                bad_case += "研究课题：{}， 研究细节：{}".format(reseach.research, reseach.research_desc)
            if reseach.status not in [Status.INIT, Status.PROPOSED, Status.REJECTED_PROPOSAL]:
                good_case += "研究课题：{}， 研究细节：{}".format(reseach.research, reseach.research_desc)
        
        query = AlicePrompts.PLAN_VISION
        query = query.replace("{vision}", vision.vision)
        query = query.replace("{vision_desc}", vision.vision_desc)
        query = query.replace("{plan_cnt}", str(plan_cnt))
        query = query.replace("{good_case}", good_case)
        query = query.replace("{bad_case}", bad_case)
        
        self.logger.info("[Alice] plan_vision[prompt], for vision: " + vision.vision, "\n, prompt: ", query)

        LLMChatHistory.create(id=Id.new_id(), vision_id=vision.id, propose_by=ProposalBy.ALICE, 
                              message=query, propose_time=get_now_unixtime(), cost_ms=0, tags="")
        start = time.time()
        result = defaultLLM.generate(query)
        cost_ms = int((time.time() - start) * 1000)
        self.logger.info("[Alice] plan_vision[llm_generate], for vision: " + vision.vision, "\n", query, "\n LLM Result: ", result, ", Cost: ", cost_ms)
        LLMChatHistory.create(id=Id.new_id(), vision_id=vision.id, propose_by=ProposalBy.LLM, 
                              message=result, propose_time=get_now_unixtime(), cost_ms=cost_ms, tags="")
        
        process_content = ""
        researchs, err_msg = defaultLLM.format_json(result)
        if researchs:
            for research in researchs:
                process_content += "研究课题：{}， 研究细节：{}\n\n".format(research["research_title"], research["research_desc"])
                rsm = ResearchSM(research=research["research_title"], vision_id=vision.id, start_value=Status.PROPOSED)
                rsm.research_desc = research["research_desc"]
                rsm.save_model()
            
            VisionProgress.create(id=Id.new_id(), vision=vision.id, 
                                title="新增 {} 个研究课题题案".format(len(researchs)), 
                                content=process_content, 
                                propose_by=ProposalBy.ALICE, propose_time=get_now_unixtime())
        else:
            self.logger.error("[Alice] plan_vision[llm_generate], llm resp parse error, vision: {}, raw resp: {}, err: {}"
                              .format(vision.vision, result, err_msg))
            
    
    def schedule_plan_research(self):
        todo_researchs = Research.select().where( (Research.status.in_([Status.READY, Status.ASSIGNED])) 
                                               | ((Research.propose_by == ProposalBy.HUMEN) & (Research.status.in_([Status.INIT]))) )
        for research in todo_researchs:
            self.logger.info("[Alice] schedule_plan_research, will process research: {}".format(research.research))
            not_active_status = [Status.FAIL, Status.CANCEL, Status.SUSPENDED, Status.DONE]
            deepthinks = Deepthink.select().where(Deepthink.research_id == research.id)
            active_deepthinks = list(map(lambda x: x.status not in not_active_status, deepthinks))
            if len(active_deepthinks) < self.KEEP_ACTIVE_RESEARCHS:
                need_deepthinks = self.KEEP_ACTIVE_RESEARCHS - len(active_deepthinks)
            else:
                need_deepthinks = 0
            if need_deepthinks > 0:
                self.logger.info("[Alice] schedule_plan_research, Plan deepthink for research: {}".format(research.research))
                self.plan_research(research, need_deepthinks, deepthinks)


    def plan_research(self, research, plan_cnt, current_deepthinks):
        bad_case = ""
        good_case = ""
        for deepthink in current_deepthinks:
            if deepthink.status in [Status.REJECTED_PROPOSAL]:
                bad_case += "深度思考：{}， 思考细节：{}".format(deepthink.deepthink, deepthink.deepthink_desc)
            if deepthink.status not in [Status.INIT, Status.PROPOSED, Status.REJECTED_PROPOSAL]:
                good_case += "深度思考：{}， 思考细节：{}".format(deepthink.deepthink, deepthink.deepthink_desc)
        
        query = AlicePrompts.PLAN_RESEARCH
        query = query.replace("{vision}", research.vision.vision)
        query = query.replace("{vision_desc}", research.vision.vision_desc)
        query = query.replace("{research}", research.research)
        query = query.replace("{research_desc}", research.research_desc)
        query = query.replace("{plan_cnt}", str(plan_cnt))
        query = query.replace("{good_case}", good_case)
        query = query.replace("{bad_case}", bad_case)
        
        self.logger.info("[Alice] plan_research[prompt], for research: " + research.research, "\n, prompt: ", query)

        LLMChatHistory.create(id=Id.new_id(), vision_id=research.vision.id, propose_by=ProposalBy.ALICE, 
                              message=query, propose_time=get_now_unixtime(), cost_ms=0, tags="")
        start = time.time()
        result = defaultLLM.generate(query)
        cost_ms = int((time.time() - start) * 1000)
        self.logger.info("[Alice] plan_research[llm_generate], for research: " + research.research, "\n", query, "\n LLM Result: ", result, ", Cost: ", cost_ms)
        LLMChatHistory.create(id=Id.new_id(), vision_id=research.vision.id, propose_by=ProposalBy.LLM, 
                              message=result, propose_time=get_now_unixtime(), cost_ms=cost_ms, tags="")
        
        process_content = ""
        deepthinks, err_msg = defaultLLM.format_json(result)
        if deepthinks:
            for deepthink in deepthinks:
                process_content += "深度思考：{}， 思考细节：{}\n\n".format(deepthink["deepthink_title"], deepthink["deepthink_desc"])
                rsm = DeepthinkSM(deepthink=deepthink["deepthink_title"], research_id=research.id, start_value=Status.PROPOSED)
                rsm.deepthink_desc = deepthink["deepthink_desc"]
                rsm.save_model()
            
            ResearchProgress.create(id=Id.new_id(), research=research.id, 
                                title="新增 {} 个深度思考".format(len(deepthinks)), 
                                content=process_content, 
                                propose_by=ProposalBy.ALICE, propose_time=get_now_unixtime())
        else:
            self.logger.error("[Alice] plan_research[llm_generate], llm resp parse error, research: {}, raw resp: {}, err: {}"
                              .format(research.research, result, err_msg))


if __name__ == "__main__":
    alice = Alice()
    alice.schedule_plan_research()