# ATHENAi

ATHENAi 是一个终身学习的智能体，在预设目标下，终身探索，永无止境。

## 代码目录

```bash
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
/alice: 智能助理、导师（慢思考）
    /vision: 【人】期望的愿景
        /research：【人&Alice】基于 vision 拆解出的课题【初始人提供，后续 god 可以建议】。
            /judge: 【人】判断课题完成情况
            /plan：【Alice&人】生成 deepthink 课题
                /plan_next：继续生成新的 deepthink 课题
                /summary：对 thinker 所有deepthink的完成情况进行总结，生成下一步的 plan
                /supervise：主动监督 thinker 执行的过程
            /summary：【alice】对当前 Topic 的进展进行总结
        /summary：【alice】对当前 Vision 的进展进行总结，生成建议的新的 Topic。
    /next_deepthink: 给 thinker 下一个可以执行的 deepthink。
/thinker: 思考者（快思考），对记忆进行加工，thinker 可以有多个，共享长期记忆，短期记忆取决于 thinker 自己的内部实现。
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
```

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


## APIs

http://127.0.0.1:8000/api/v1/vision
http://127.0.0.1:8000/api/v1/research?vision=05052e93-a27c-46e4-84fa-1633c9b92499
http://127.0.0.1:8000/api/v1/deepthink?research=6209399e-a91f-4c43-b41d-256f5961e385
http://127.0.0.1:8000/api/v1/task?deepthink=xxxxx


## Core Workflow

### 定期 Task

#### Alice - Plan Vision

- 遍历所有 Vision，生成 Vision 相关的研究课题
    - 如果没有任何 Research，生成 5 个研究课题。
    - 如果已经有 Research，但是没有处于可执行/提议状态的，且状态未出于完成，就再生成 5 个研究课题
    - 如果有出于可执行状态的，但是不够 5 个，就额外生成补足 5 个
    - 生成时，带上历史的正反案例，且不要生成重复的研究课题。


#### Alice - Plan Research

- 遍历所有的 Research，生成 Research 相关的 Deepthink
    - 如果没有，就生成 5 个
    - 如果已经有，但是没有处于可执行/提议状态的，且状态未出于完成，就再生成 5 个。
    - 生成时，带上历史的正反案例，且不要生成重复的。


#### Alice - Report Research

- 对当前的 Research 执行情况做一个总结汇报。


#### Alice - Schedule Deepthink

- 针对所有的 Deepthink，排序（高优先级、 提出早的位于前面）
- 按照次序赋予所有的 Thinker 执行（Thinker Pull 模式）


#### Alice - Judge Deepthink

- 针对出于 阶段完成 状态的 Deepthink，判断其是否到达完成标准，如果到达将其置为 提案，由人进行审阅判断
- 如果未达到标准，将其状态扭转为 驳回，并附上期望整改的点。
- 如果驳回达到一定次数，转为 提案状态。


### 常驻线程

#### Thinker - Run Deepthink

- 从 Alice 获取下一个 Deepthink
- 检查是否已经有相关的 Task，如果已经有，可能是中断重跑的，跳过 Plan Task 步骤
- 生成 Deepthink 相关的 Task (中生成质量), 参考 阿里 心流 的实现方式
- 对于驳回的 Deepthink，按照 Alice 的建议，生成额外的 Task （注意不要生成重复的）
- 按次序完成所有待完成的 Task。
- 生成总结，将状态记录为 提交（COMMIT）。


#### Alice - Judge

- 针对 Thinker 的工作进行初步判定（后续再交给人 2 次把关），是否满足需求
