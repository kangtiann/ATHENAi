import json
import logging
from haystack import Pipeline
from haystack.utils import Secret
from haystack.components.generators import OpenAIGenerator
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage


class LLM():
    def __init__(self, system_prompt="", temperature=0, top_p=0.6):
        self.temperature = temperature
        self.top_p = top_p
        self.system_prompt = system_prompt

    def generate(self, prompt):
        pass

    def format_json(self, resp):
        pass


class LMStudioLLM(LLM):
    logger = logging.getLogger("LMStudioLLM")
    
    def __init__(self, system_prompt="", temperature=0, top_p=0.6):
        super().__init__(system_prompt, temperature, top_p)
        self.client = OpenAIGenerator(
            api_base_url = "http://127.0.0.1:1234/v1",
            api_key=Secret.from_token("not_need"),
            system_prompt=self.system_prompt,
            generation_kwargs=dict(temperature=self.temperature, top_p=self.top_p)
        )

    def generate(self, prompt):
        response = self.client.run(prompt=prompt)
        return response["replies"][-1]
    
    def format_json(self, response_str):
        try:
            response_json = json.loads(response_str.replace("```json", "").replace("```", ""))
        except Exception as e:
            response_json = None
            self.logger.error("[LMStudioLLM] generate_json, parse json resp error: {}, raw resp: {}".format(e, response_str))
            return response_json, str(e)
        return response_json, "ok"

    def generate_json(self, prompt):
        response = self.client.run(prompt=prompt)
        response_str = response["replies"][-1]
        try:
            response_json = json.loads(response_str.replace("```json", "").replace("```", ""))
        except Exception as e:
            response_json = None
            self.logger.error("[LMStudioLLM] generate_json, parse json resp error: {}, raw resp: {}".format(e, response_str))
            return response_json, str(e)
        return response_json, "ok"


defaultLLM = LMStudioLLM(
    system_prompt="你是一个富有科学探索精神的科学家，会以专业的科学视角，帮助用户实现愿景。",
    temperature=0,
    top_p=0.6
)
