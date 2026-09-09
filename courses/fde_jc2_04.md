# 第 4 章 · Agent 框架 · LangChain

> 来源：B站《FDE零基础教程》UP主「大模型基础知识」· 技术底座篇
> 加工方式：视频口播 → whisper 转写 → 结构化精读
> 一句话价值：LangChain 核心组件 / 输入输出封装 / 数据连接 / 对话历史 / LCEL / Agent 架构 / LangServe 部署

---

## 上篇 · 书籍内容

### 引子：为什么需要「LangChain」这样的开发框架

大模型应用开发不是「调一次 API」那么简单。一个真正可上线的产品，至少要做这些事：

- 不同大模型（OpenAI、文心、Qianfan、星火、Claude…）的**接口适配**，不能被单一厂商绑定。
- **Prompt 模板**与多轮消息历史的管理。
- 把大模型输出的纯文本**结构化解析**回程序可用的对象。
- **文档加载、切分、向量化、检索**，把私域知识塞进大模型上下文。
- **多轮对话历史**的裁剪、筛选、存取。
- 把上面的零散步骤**串成一个工作流**，支持流式、批量、异步、回退、调试。
- 当任务复杂到要多次推理 + 选工具时，需要 **Agent（智能体）**。
- 写完以后还要把整套链路**部署成 HTTP 服务**，给前端或外部系统调用。

这些事情每件都可以自己写。但每件都自己写，意味着每一个项目都在重新发明轮子。LangChain 的价值，就是把这些「与大模型打交道时高频出现的重复劳动」封装成统一接口、统一工具包，让开发者把精力集中在业务逻辑而不是胶水代码上。

> 与 LlamaIndex 的关系：二者是**错位竞争**。LlamaIndex 把更多精力花在「以 RAG 为中心」的文档加载、切分、检索、增强生成这条流水线上，工具更细更全；LangChain 是更**通用**的大模型应用开发框架，Prompt、模型、解析、回调、Agent、部署什么都有，但 RAG 这一段做得相对粗糙。所以——重 RAG 的项目优先考虑 LlamaIndex，重工程化和 Agent 的项目优先考虑 LangChain，混用也可以。

> 学习提醒：现在所有大模型应用开发框架都还在快速迭代，平均一天一个新版本。LangChain 接口也在漂移（JsonOutputParser、PydanticOutputParser 都有过反复），所以学习这一类框架的正确姿势是「**学设计思想 + 学代码结构**」，而不是「死记 API」。理解了为什么这样设计，自己写一套等价的代码库也不难。

---

### 一、LangChain 的核心组件全景

LangChain 把上面那些事拆成 7 大工具集：

| 组件 | 解决的痛点 |
|---|---|
| 模型封装（Models） | 抹平不同大模型的接口差异 |
| Prompt 模板（Prompts） | 把 Prompt 变成可复用的「带参数函数」 |
| 输出解析（Output Parsers） | 把大模型的纯文本输出解析成结构化对象 |
| 数据连接（Data Connection） | 文档加载、切分、Embedding、向量库、检索 |
| 对话历史（Memory） | 多轮消息的裁剪、筛选、存取 |
| LCEL（LangChain Expression Language） | 用声明式语法把上面所有组件串成链路 |
| Agent | 多步推理 + 自动选工具完成复杂任务 |
| 回调（Callbacks） | 在链路每个环节插入日志、监控、重试 |

这 7 大组件加在一起构成了一个与大模型打交道的「**完整工具箱**」。下面按直播课顺序逐个精读。

---

### 二、输入输出封装

#### 1. 模型封装：换模型不动业务代码

每个大模型厂商的接口都不一样——参数名、消息格式、鉴权方式都不同。如果直接写原生接口，换一家厂商基本等于重写一遍。

LangChain 的做法是给每个主流模型封一个 `ChatXXX` 类（`ChatOpenAI`、`ChatQianfan`、`ChatSpark`、`ChatClaude` 等），所有类对外暴露**同一个接口**（如 `.invoke()`）。换模型只需要换实例化的类，业务代码完全不动。

一个最小例子（OpenAI → 文心一言）：

```
# 原来用 OpenAI
model = ChatOpenAI(model="gpt-4o-mini")

# 换成百度文心一言，只要改这一行
model = ChatQianfan(model="ERNIE-Bot")

# 后面所有调用代码都不变
response = model.invoke([HumanMessage(content="你好")])
```

> 常见坑：百度文心的 key 分两段（access key + secret key），要分别传入；不同厂商的 `temperature` / `max_tokens` 等参数命名也有细微差别，要查对应类的文档。

#### 2. Prompt 模板：把 Prompt 变成「带参数的函数」

把 Prompt 模板本身看成一个**带槽（占位符）的函数**——你给它不同的参数，它就生成不同的完整 Prompt。这跟 Python 里 `str.format()` 的思路一致，但 LangChain 的封装更系统。

三种用法递进：

**（1）单字符串模板**：最简单，模板里用 `{variable}` 抠槽。

```
template = PromptTemplate.from_template(
    "讲一个关于 {subject} 的笑话"
)
prompt = template.format(subject="小明")
```

**（2）多轮消息模板（ChatPromptTemplate）**：用 `from_messages` 传一个列表，每条消息可以是固定文本，也可以带槽。System 角色定人设，Human 角色是用户输入，AI 角色可填历史回复。

```
template = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template("你是{role}"),
    HumanMessagePromptTemplate.from_template("{question}"),
])
```

**（3）MessagePlaceholder：把整段历史做槽**：如果某一段是「整段多轮对话历史」（比如检索回来的 Q/A 对、或之前几轮的聊天记录），不想一行行定义，就用一个 `MessagePlaceholder` 把它整体挖空，运行时把消息列表整个塞进去。

```
template = ChatPromptTemplate.from_messages([
    SystemMessage(content="根据上下文回答问题"),
    MessagesPlaceholder("history"),       # 整段历史填这里
    HumanMessagePromptTemplate.from_template("翻译成{language}：{question}"),
])
```

> **Prompt 与代码分离**：实战中强烈建议把 Prompt 模板从代码里**剥离到外部文件**（YAML / JSON / txt）。LangChain 直接支持 `from_file`，一行就能从文件加载。这样：
> - Prompt 改文案不用动代码、不用重新部署。
> - 自然语言逻辑与代码逻辑解耦。
> - 团队里负责调 Prompt 的同学可以独立迭代。

LlamaIndex 没提供这个功能，需要自己实现——这是 LangChain 设计上更周到的地方。

#### 3. 输出解析：把纯文本变回结构化对象

大模型默认输出是纯文本，但程序代码更擅长处理**结构化对象**（dict、JSON、Pydantic class）。常见场景：用户一句话「订一个十元的流量包」，要先把它解析成 `{price: 10, package_type: "流量包", ...}`，再去查后端数据库。

LangChain 给三种主要工具：

**（1）Pydantic + `with_structured_output()`**：用 Pydantic 定义你想要的输出结构（字段名、类型、描述），直接把类传给大模型，大模型会按这个 Schema 输出，解析完直接得到 Pydantic 对象。**最推荐**。

```
from pydantic import BaseModel

class Date(BaseModel):
    year: int
    month: int
    day: int
    era: str  # "BC" 或 "AD"

model = ChatOpenAI(model="gpt-4o-mini").with_structured_output(Date)
result = model.invoke("2024 年 3 月 15 日")
# result.year == 2024, result.month == 3 ...
```

**（2）`JsonOutputParser`**：不锁死输出 Schema，让大模型自由输出 JSON 字符串，再用 Parser 解析成 dict。灵活，但需要自己写 Prompt 约束格式。

**（3）`OutputFixingParser`（自修复解析器）**：大模型不是 100% 听话的，偶尔会吐出非法 JSON（比如数字字段写成汉字「四」没加引号）。这个解析器在解析失败时会**自动再调一次大模型**让它重新生成——省去你手写重试逻辑。

> **核心教训**：任何大模型驱动的结构化输出，**都必须容错**。即使你 Prompt 写得再好，也有概率出错。线上代码如果没用 OutputFixingParser 或自己写的等价容错，分分钟被一次偶发失败打挂。

#### 4. Function Calling / Tool Calling 的封装

OpenAI 推出「让大模型输出结构化函数调用请求」的接口后，LangChain 跟上做了封装：

- **定义工具**：在你普通函数上挂一个 `@tool` 装饰器，LangChain 自动读取函数名、参数、注释，生成给大模型的工具描述。
- **绑定工具**：`model.bind_tools([add, multiply])`，得到一个「知道有哪些工具可用」的大模型。
- **处理调用请求**：当大模型决定要调工具时，它的返回里会带一个 `tool_calls` 字段，告诉你调哪个工具、参数是什么。
- **执行 + 回传**：你本地真的执行这个函数，把结果用 `ToolMessage` 包起来塞回消息历史，再调大模型，大模型会基于工具结果生成最终回答。

完整流程 = 触发调用 → 本地执行 → 把结果回传 → 生成最终答案。

---

### 三、数据连接（RAG 的那一段）

LangChain 的 RAG 工具链分 4 步：

| 步骤 | LangChain 提供的工具 |
|---|---|
| 加载文档 | `DocumentLoaders`（PDF、Word、HTML、Markdown、CSV…） |
| 切分文本 | `TextSplitters`（按字符、按 Token、按句子，可配 chunk_size 和 overlap） |
| Embedding | `OpenAIEmbeddings` / 各厂商的 Embedding 类，统一接口 |
| 灌库 + 检索 | `VectorStore`（FAISS、Chroma…）+ `Retriever`（接口统一） |

灌库与检索的最简流程：

```
# 加载 → 切分
docs = PyPDFLoader("xxx.pdf").load()
chunks = CharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(docs)

# Embedding → 灌库
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# 检索
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
results = retriever.invoke("用户的问题")
```

> **直播课的诚实警告**：LangChain 的数据连接这一段**做得比 LlamaIndex 粗糙**，各种小坑多。**生产环境不建议直接用 LangChain 的 RAG 工具**，要么换成 LlamaIndex，要么自己基于这套接口再封装一层兜底。LangChain 的强项不在 RAG，而在工程化和 Agent。

---

### 四、对话历史管理

多轮对话里消息历史会越聊越长。要么 Token 超限把账单打爆，要么上下文太杂把模型搞晕。LangChain 给两类工具：

#### 1. 裁剪：`trim_messages`

按 Token 数量上限裁剪历史，默认从尾部往前保留（保留最近的）。可配置项：
- `max_tokens`：保留多少。
- `strategy="last"`：从末尾往前数。
- `token_counter`：告诉它按哪个模型的 Tokenizer 计费（不同模型 Token 切法不同，不指明会算错）。
- 强制保留 SystemMessage（把系统人设裁掉，模型连自己是谁都不知道了）。

```
from langchain_core.messages import trim_messages
trim_messages(
    history,
    max_tokens=45,
    strategy="last",
    token_counter=ChatOpenAI(model="gpt-4o").get_num_tokens,
    include_system=True,
)
```

#### 2. 筛选：自定义 id / name 标签 + Filter

每条消息可以挂两个自定义字段 `id` 和 `name`（LangChain 不约定语义，你自己定义）。然后用 `filter_messages` 按三种维度筛选：
- **角色**（system / human / ai）。
- **id 包含/不包含**。
- **name 包含/不包含**。

可以组合筛选：「保留 human 和 ai 消息，但排除 id=3 的那轮」。

> **思考题**：什么样的业务场景需要这种自定义筛选？
> 答案举例——客服系统里多个子任务的历史混在一个用户的消息数组里（售前对话、技术支持对话、投诉对话各占几轮），按 `name` 区分场景，调用时只把「当前场景」的历史喂给模型。

#### 3. 持久化：`RunnableWithMessageHistory`

把「消息历史」和「业务逻辑（Chain）」**解耦**——这是工程化最重要的设计：

```
def get_session_history(session_id: str):
    # 你的实现：内存 dict / Redis / MongoDB / Postgres 都行
    return MessageHistory(...)

chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history",
)

# 调用时传 session_id
chain_with_history.invoke(
    {"input": "我叫小明"},
    config={"configurable": {"session_id": "user_123"}},
)
```

每次调用时，自动用 `session_id` 去取这个用户的完整历史 → 拼到当前输入前面 → 调 Chain → 把新的一轮塞回历史 → 存起来。**多用户并发天然支持**。

生产环境不要用内存 dict（重启就丢），用 Redis 或 Postgres。

---

### 五、LCEL（LangChain Expression Language）

这是 LangChain 的**灵魂**——也是它最大的设计创新。

#### 1. 它是什么

LCEL 是 LangChain 自己定义的**声明式语言**，用来描述「**A 的输出给 B，B 的输出给 C**」这种调用顺序。语法只有一条规则：**用 `|` 把组件串起来**。

```
chain = prompt | model | output_parser
result = chain.invoke({"subject": "小明"})
```

`prompt | model | output_parser` 就是一个 **Runnable**（LangChain 给这玩意起的名字：Chain / Runnable / Runnabl 三个词混用，都是它）。

#### 2. 为什么要有 LCEL

不用 LCEL，你也能 `result = output_parser.parse(model.invoke(prompt.format(x)))`，写起来也不算长。但 LCEL 给你换来了**白送**的 6 个能力：

| 能力 | 一行代码 | 不用 LCEL 怎么写 |
|---|---|---|
| **流式输出** `chain.stream(x)` | 链路上每个 token 实时推给前端 | 自己写 SSE / WebSocket 拼装 |
| **批量调用** `chain.batch([x1,x2,x3])` | 后台并发跑 | 手写线程池 / asyncio.gather |
| **异步调用** `chain.ainvoke(x)` | 同步改异步一行 | 重写所有调用 |
| **并行分支** | 多个组件并列后再合并 | 手写并发合并逻辑 |
| **回退 Fallback** | `chain.with_fallbacks([alt_chain])` | 自己写 try/except |
| **调试追踪** | 自动对接 LangSmith | 自己埋点打日志 |

也就是说，**同一个 Chain 定义，从原型到生产，从调试到部署，无需修改一行代码**。这是 LCEL 的核心价值——把「调试态代码」和「生产态代码」统一成一份。

#### 3. RunnableWithMessageHistory 是 LCEL 的扩展

上一节提到的对话历史管理，本质上就是给一个 `Runnable` 套了一层壳，自动管理消息历史存取。

#### 4. 工厂模式：`configurable_alternatives`

工程上经常需要「同一个业务流程，底层大模型可换」（国内用文心、海外用 GPT）。LangChain 不叫它「工厂」，但实现的功能就是工厂：

```
model = ChatOpenAI(model="gpt-4o-mini").configurable_alternatives(
    ConfigurableField(id="llm"),
    default_key="gpt",
    wenxin=ChatQianfan(model="ERNIE-Bot"),
)

# 运行时决定用哪个
chain.invoke(x, config={"configurable": {"llm": "wenxin"}})  # 走文心
chain.invoke(x, config={"configurable": {"llm": "gpt"}})     # 走 GPT
```

`configurable_alternatives` 可以挂在 **Prompt、Model、OutputParser 任一环节**——任何一个你想要「根据配置切换」的地方都能用。

> **设计模式彩蛋**：LCEL 本身是**建造者模式（Builder Pattern）**的典型应用——你可以换 Prompt、换 Model、换 Parser，但组件之间的「工作关系」不变。换一台电脑，CPU/内存/显示器都可以换，但它们怎么连起来是不变的——这就是 Builder。

---

### 六、Agent（智能体）

#### 1. 什么是 Agent

简单任务（调一个函数）走 Function Calling 就够了。复杂任务——需要**多次思考 → 选工具 → 看结果 → 再思考 → 再选工具**——这种多步推理的应用叫 **Agent**。

Agent 必须具备三要素：
1. **一组工具**：能调外部世界（搜索、计算、数据库、API…）。
2. **思考 / 计划能力**：大模型自己推理，决定下一步调哪个工具。
3. **短时记忆 + 长时记忆**：短时记当前多步推理过程，长时记多轮对话历史。

#### 2. LangChain 自带的两种玩具型 Agent

LangChain Hub 上下载两个内置 Prompt 就能跑的 Demo：

**（1）ReAct Agent**（主流）：Thought → Action → Observation → Thought → Action → … → Final Answer。每一步都从工具列表里选一个执行。

**例子**：「2024 年周杰伦的演唱会日期是星期几？」
- 思考：需要先查演唱会日期。
- 调用搜索工具 → 拿到 2024-05-20。
- 思考：要把日期转成星期几。
- 调用日历工具 → 拿到星期一。
- 输出最终答案。

**（2）Self-Ask Agent**（次主流）：每一步**反问自己**下一个子问题，然后搜。比如「冯小刚老婆演过什么电影？」→ 自动反问「冯小刚老婆是谁？」→ 搜到「徐帆」→ 再问「徐帆演过什么电影？」→ 搜到 → 输出答案。

> Self-Ask 适合「**单工具 + 多步推理**」的场景（比如只能调搜索），通用性不如 ReAct。**生产首选 ReAct**。

直播课强调：这两个是**玩具 Demo**，Prompt 写得很简单。真正能实战的 Agent 需要专门设计 Prompt、设计复杂业务工作流、必要时用微调模型——后续三堂课专门讲。

---

### 七、LangServe：把 Chain 一键部署成 HTTP 服务

写完 Chain 后，怎么给前端用？LangServe 是 LangChain 团队原生的部署工具（Python 版，JS 版也有，接口还略超前）。

一行命令启动：

```
langchain serve
```

它会做三件事：
1. 把你的 Chain 部署成一个 HTTP 服务（FastAPI 框架）。
2. 自动生成一个 **Playground 调试界面**——可视化看到 Prompt 模板、模型输入输出、中间结果。
3. 提供 Client SDK，前端 / 后端可以直接通过 HTTP 调用。

> **直播课的坑警告（必须知道）**：LangServe **Python 版在 2.x 之后**，**流式调用一旦启动，没有任何办法停下来**。如果产品里有大段文本流式输出，用户中途想中断（比如「我不想听了」），**Python 版做不到**——只有 JS 版有停流接口。这是 2.x 版本最大的坑。

如果你正在做大段流式交互产品，请评估：
- 用 JS 版 LangServe（牺牲 Python 生态）。
- 自己基于 LangChain 的 Chain 写一个轻量部署层，加停流控制。
- 等 LangServe 修复。

---

### 结论与金句

1. **LangChain 的价值是「封装胶水代码、让你聚焦业务」**——但前提是你得先理解它为什么这样封装，否则就是在黑盒里调 API。
2. **LCEL 是 LangChain 的灵魂**——一个 Chain 定义走完「调试→生产→部署」全程不修改一行代码，这是一切工程化收益的源头。
3. **Prompt 必须与代码分离**——`from_file` 不是花活，是 AI 产品能不能被非工程师同学独立迭代的分水岭。
4. **结构化输出必须容错**——`OutputFixingParser` 不是可选项，是生产必需。
5. **RAG 重活别全压给 LangChain**——它在这一段做得粗糙，重 RAG 项目优先考虑 LlamaIndex 或自研。
6. **LangServe Python 版的流式不可中断**——这是当前最大的工程化坑，决策前必须验证。

---

## 下篇 · 方法论精华（可迁移）

### 一张速查表

| 场景 | LangChain 方案 | 关键 API | 替代 / 注意 |
|---|---|---|---|
| 跨厂商模型调用 | `ChatXXX` 类 | `model.invoke([msg])` | 换厂商换类，业务代码不动 |
| Prompt 复用 | `PromptTemplate` / `ChatPromptTemplate` | `.from_template` / `.from_messages` / `.from_file` | **必须 `.from_file` 分离** |
| 把模型输出变对象 | `with_structured_output(Pydantic)` | `.with_structured_output(Date)` | 优先 Pydantic 不用 JSON |
| 模型输出不可控容错 | `OutputFixingParser` | `OutputFixingParser(parser=base, model=llm)` | 生产必备 |
| 函数调用 | `@tool` + `bind_tools` | `model.bind_tools([fn])` | 处理 `tool_calls` 后回传 |
| 文档加载 | `PyPDFLoader` / `UnstructuredXXXLoader` | `.load()` | LangChain 这段粗糙 |
| 文本切分 | `CharacterTextSplitter` / `TokenTextSplitter` | `chunk_size` / `chunk_overlap` | 按业务调整 |
| Embedding | `OpenAIEmbeddings` / `QianfanEmbeddings` | `.embed_query(text)` | 切模型要重新灌库 |
| 向量库 | `FAISS` / `Chroma` | `.from_documents(docs, emb)` | 选轻量 FAISS，重型选 Milvus |
| 历史裁剪 | `trim_messages` | `max_tokens` + `strategy="last"` | 必须指定 tokenizer |
| 历史筛选 | `filter_messages` | 按 role / id / name | 自定义字段自己定语义 |
| 历史持久化 | `RunnableWithMessageHistory` | `config={"configurable": {"session_id": ...}}` | 生产用 Redis/Postgres |
| 工作流串联 | LCEL `\|` | `chain = prompt \| model \| parser` | 灵魂，必须会用 |
| 流式 / 批量 / 异步 | `chain.stream/batch/ainvoke` | 白送 | LCEL 自带 |
| 回退 | `chain.with_fallbacks` | — | 业务级容错 |
| 多模型可切换 | `configurable_alternatives` | `config={"configurable": {"llm": ...}}` | 工厂模式实现 |
| Agent 玩具 | `create_react_agent` | LangChain Hub Prompt | 实战要重写 Prompt |
| 部署成 HTTP | `langchain serve` | — | **Python 流式不可中断** |

### 通用原则

1. **接口先行，理解再写**。LangChain 的每个类背后都是一个真实软件工程问题。先搞懂「为什么要这么封装」，再去看 API。
2. **Prompt 外置化是 AI 工程化的第一原则**。能用 `from_file` 就别写死在代码里。
3. **链路的每个环节都加容错**。大模型不是数据库，任何解析、调用都要考虑失败路径。
4. **生产环境必接 LangSmith 或自建回调**。没日志的 AI 应用等于没排障能力的黑盒。
5. **框架漂移是常态**。一天一版的迭代节奏下，文档可能比代码旧。读源码永远比读文档靠谱。
6. **学框架的真正姿势是学设计模式**。LCEL 是 Builder，模型切换是 Factory + Strategy，Agent 调度是 Chain of Responsibility——这些模式不因框架版本变化而过时。

### 可复用模式

**模式 1：Template-as-Function（模板即函数）**
Prompt 模板 = 一个带类型约束的函数。输入是参数，输出是结构化结果。把所有 Prompt 收口在一个目录里，按业务模块分子目录，文件名就是函数名。

**模式 2：Chain-as-Unit（链路即单元）**
任何业务功能都封装成一个 LCEL Chain。Chain 是版本化、可测试、可部署、可回退的最小单元。前端 / 后端 / Agent 全部通过调用 Chain 完成业务。

**模式 3：Stateful-Chain（带状态的链路）**
对所有需要多轮对话的能力，统一用 `RunnableWithMessageHistory` 包装，session_id 由外部传入，存储后端抽象成接口（生产用 Redis，测试用内存）。

**模式 4：Configurable-Component（可配置组件）**
对所有「同业务逻辑、不同底层实现」的组件（不同厂商模型、不同业务线 Prompt、不同输出格式），统一加 `configurable_alternatives` 或类似机制。**让切换成本变成零**。

**模式 5：Callback-as-Observability（回调即可观测性）**
链路每个环节插一个 Callback：记录输入、输出、耗时、Token 数、失败原因。线上问题的 80% 来自这层日志的回溯。

---

## 借鉴篇 · 我们能借鉴的点

结合王昕业务（企业 AI 客户交付 / FDE / 获客系统 / 8895 知识库），逐条落地：

### 1. 把 8895 知识库从「文档堆」变成「RAG 知识服务」
- **业务场景**：现在 8895 知识库里的方法论、案例、SOP 还是散落文档。客户问问题时，咨询师靠人肉检索。
- **怎么做**：用 LangChain 的 `DocumentLoaders` 把现有文档全部灌库 → `TextSplitter` 切分（按业务章节，保持 chunk 语义完整）→ `FAISS` 或 `Milvus` 灌向量库 → 用 LCEL 串一条「用户问题 → Retriever → Prompt 模板（含上下文）→ 大模型 → 结构化输出」的 RAG Chain。
- **产出**：8895 知识 API，对外可被获客系统的「AI 顾问」调用，对内可被 FDE 在客户现场做 demo 调。

### 2. 客户现场 FDE Demo 的「5 分钟搭一个 AI 应用」工具箱
- **业务场景**：FDE 进客户现场，最常被问的是「能不能先让我们看看你们的能力」。需要快速搭一个可演示的小应用。
- **怎么做**：封装一个内部 SDK，封装好 LangChain 的模型封装 + Prompt 模板 + 输出解析 + LCEL。FDE 只需要：选业务场景模板 → 填客户专属数据 → 一键启动 LangServe。5 分钟内出可交互 Demo。
- **产出**：FDE Demo 工具包 v1。

### 3. 获客系统的「AI 顾问」对话引擎
- **业务场景**：获客系统里的 AI 顾问要和潜在客户多轮对话，要识别客户意图、推荐合适服务、引导留资。
- **怎么做**：用 `RunnableWithMessageHistory` 实现多用户并发对话历史管理 → 用 `OutputFixingParser` + Pydantic 把客户意图解析成结构化（行业、痛点、预算、决策角色）→ 用 `with_structured_output` 约束大模型按业务字段输出。session_id 用客户 ID，存储用 Redis。
- **产出**：AI 顾问后端服务，第一版支持 3-5 个核心对话场景。

### 4. Prompt 模板库：从「代码里散落」到「集中外置」
- **业务场景**：现在团队每个 FDE 都在代码里硬编码自己写 Prompt，散落各处，质量和复用率都低。
- **怎么做**：建一个内部 Prompt 仓库（Git 仓库 + YAML 文件），所有 Prompt 用 LangChain `from_file` 加载。文件命名规范：`场景_业务线_版本.yaml`，例：`leads_intent_recognition_v3.yaml`。配合 LangSmith 或自建 Callback 做线上效果监控。
- **产出**：Prompt 仓库 v1 + 加载 SDK。

### 5. 「可配置底层模型」：避免单一厂商绑定
- **业务场景**：客户有数据合规要求，部分场景必须用国内大模型（文心 / 通义 / 智谱），部分场景可以用 GPT。
- **怎么做**：所有业务链路里的模型节点用 `configurable_alternatives`，运行时根据客户配置决定调哪家。**业务代码一次写，多家模型无缝切换**。
- **产出**：底层模型可配置框架 + 客户级模型路由策略。

### 6. 给客户交付的「可观测性」包装
- **业务场景**：客户用我们的 AI 服务，出问题时需要看完整链路日志——哪个环节慢、哪个环节失败了、为什么大模型给出了那个回答。
- **怎么做**：在 LCEL 链路上统一挂 Callback：记录每一步的输入、输出、耗时、Token 数、错误信息。对接客户的日志系统（ELK / 自家看板）。
- **产出**：可观测性 SDK，集成到交付包里。

### 7. Agent 化：从「单步问答」到「多步任务」
- **业务场景**：当前 AI 服务都是「问一答一」，客户开始问「能不能让它帮我自动做这件事」（比如自动查 8895 知识库 + 自动生成方案 + 自动发给销售）。
- **怎么做**：基于 ReAct Agent 模式，把 8895 检索、客户档案查询、方案模板填充这些能力包装成工具，让 Agent 自己规划多步。**短期做玩具版做展示，中期沉淀 Agent Prompt 设计规范，长期考虑微调 Agent 底模**。
- **产出**：8895 智能助理 Agent v0.1（玩具版）+ 设计规范文档。

### 8. LangServe 部署 + 流式交互的取舍
- **业务场景**：客户对「实时打字机效果」有强需求，但 LangServe Python 版流式不可中断是个坑。
- **怎么做**：如果是大段流式输出场景（AI 顾问长文本回答、8895 长方案生成），**用 JS 版 LangServe** 或自己基于 FastAPI + LangChain 写轻量部署层加停流控制。短文本场景（结构化解析、关键词抽取）继续用 Python 版 LangServe。
- **产出**：流式服务部署规范。

---

**金句收尾**：LangChain 是一把瑞士军刀——什么都能干，但每样都不一定是最好。真正的工程能力不是「用 LangChain 写代码」，而是「**理解 LangChain 在解决什么问题，然后把它的设计思想移植到自己的业务架构里**」。框架会过时，设计模式不会。
