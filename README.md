# ATHENAi

ATHENAi 是一个终身学习的智能体，在预设目标下，终身探索，永无止境。

## 代码目录

/models: 数据结构
/memory: 记忆，一切的知识的载体，思考及学习即为对 memory 进行加工
    /vision
        /topic
            /deepthink
                /task
    /streams：记忆流
    /cache：短期记忆
/humen: 记录人类本身的信息，用于机器和人的结伴学习
    /humen_memory：humen_name, entity, is_known ?
/mentor: 导师（Thinker 和 人类共同的导师）
    /vision: 【人】期望的愿景
        /topic：【人】基于 vision 拆解出的课题【初始人提供，后续 god 可以建议】。
            /judge: 【人】判断课题完成情况
            /plan：【god】生成 deepthink 课题
                /plan_next：继续生成新的 deepthink 课题
                /summary：对 thinker 所有deepthink的完成情况进行总结，生成下一步的 plan
                /supervise：主动监督 thinker 执行的过程
            /summary：【god】对当前 Topic 的进展进行总结
        /summary：【god】对当前 Vision 的进展进行总结，生成建议的新的 Topic。
    /next_deepthink: 给 thinker 下一个可以执行的 deepthink。
/thinker: 对记忆进行加工，thinker 可以有多个，共享长期记忆，短期记忆取决于 thinker 自己的内部实现。
    /deepthink：深度思考，拆解为多个 task
        /task：短任务
        /summary：深度思考结果输出
/pipeline：流水线
    /subscription: 订阅（保证最新进展可以被动获得），例如 Nature、Science、Cell
        - 数学：Annals of Mathematics、Inventiones Mathematicae、Acta Mathematica、Journal Of The American Mathematical Society、
/ui：展示记忆及学习过程
    /memory：探索记忆
    /mate：机器和人结伴学习
/util：基础库
    /io：pdf、html 解析等
    /web: 网络搜索工具
    /paper: 论文搜索及解读工具
/agent: Agent 基类
    /base_agent: 基础 Agent
    /rag_agent: 支持 RAG 能力的 Agent


## workflow

- God 模块启动
  - 检查所有 Vision，选择进行中的 Vision
    - 有未完成的 Topic ？没有的话自动生成新的 Topic，等待人确认
    - 针对未完成的 Topic，查看 Plan 是否生成，未生成的话就生成 Plan。
    - 执行 Plan，如果 Plan 执行完，生成 Summary，继续加入新的 Deepthink
    - 针对 Plan 生成的 Summary，人可以判断是非完成，完成的话就可以设置状态为完成。
- Thinker【可并行启动】
  - 向 God 取下一条 Deepthink（包含建议完成时间，最大执行时长）
  - 执行 Deepthink，如果超时，就记录过程，总结并以失败告终。

