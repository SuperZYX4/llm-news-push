# 大模型新闻热点推送系统

一个利用Coze平台通过AI codings实现的基于LangChain和LangGraph构建的智能新闻热点推送系统，使用大模型自动搜索、整理和推送热点新闻。

## 项目特点

- 🤖 基于大模型智能分析新闻热点
- 📰 自动化新闻搜索与整理
- 📤 多渠道消息推送
- 📊 流式处理与实时响应
- 📝 结构化日志与错误处理
- 🛡️ 完善的错误分类与恢复机制

## 技术栈

- **核心框架**: LangChain 1.0.3, LangGraph 1.0.2
- **大模型**: OpenAI (通过LangChain集成)
- **Web框架**: FastAPI 0.121+
- **数据库**: PostgreSQL + SQLAlchemy
- **存储**: S3 (AWS) + 本地存储
- **其他依赖**: 
  - uvicorn (ASGI服务器)
  - Jinja2 (模板引擎)
  - pandas (数据处理)
  - Pillow (图像处理)
  - OpenCV (计算机视觉)
  - rich (富文本输出)

## 项目结构

```
大模型新闻热点推送-projects/
├── src/                 # 源代码目录
│   ├── agents/         # Agent相关代码
│   ├── graphs/         # 工作流定义
│   │   ├── nodes/     # 节点实现
│   │   ├── state.py   # 状态定义
│   │   └── graph.py   # 主图编排
│   ├── storage/       # 存储相关
│   │   ├── database/  # 数据库操作
│   │   └── memory/    # 内存存储
│   ├── tools/         # 工具函数
│   └── utils/         # 通用工具
├── scripts/           # 运行脚本
│   ├── local_run.sh   # 本地运行脚本
│   ├── http_run.sh   # HTTP服务启动脚本
│   └── scheduler.py  # 调度器
├── config/           # 配置文件
└── assets/           # 资源文件
```

## 工作流程

1. **新闻搜索** - 使用大模型搜索热点新闻
2. **新闻格式化** - 整理新闻内容，生成易读格式
3. **消息推送** - 将整理后的新闻推送到指定渠道

## 运行方式

### 本地运行完整流程

```bash
bash scripts/local_run.sh -m flow
```

### 运行单个节点

```bash
bash scripts/local_run.sh -m node -n node_name
```

### 启动HTTP服务

```bash
bash scripts/http_run.sh -m http -p 5000
```

## 配置说明

- `config/news_format_llm_cfg.json` - 新闻格式化LLM配置
- 环境变量配置通过 `.env` 文件管理

## 部署

1. 安装依赖: `pip install -r requirements.txt`
2. 配置环境变量
3. 启动服务: `uvicorn src.main:app --host 0.0.0.0 --port 5000`

## 贡献

欢迎提交Issue和Pull Request来改进这个项目。

## 许可证

本项目采用MIT许可证。
