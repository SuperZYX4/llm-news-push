## 项目概述
- **名称**: 热点新闻推送工作流
- **功能**: 每天早上8点自动推送大模型Agent领域的最新前沿热点新闻

### 节点清单
| 节点名 | 文件位置 | 类型 | 功能描述 | 分支逻辑 | 配置文件 |
|-------|---------|------|---------|---------|---------|
| news_search | `nodes/news_search_node.py` | task | 搜索大模型Agent领域最新新闻 | - | - |
| format_news | `nodes/format_news_node.py` | agent | AI整理新闻成4条精炼摘要 | - | `config/news_format_llm_cfg.json` |
| push_message | `nodes/push_message_node.py` | task | 微信机器人推送消息 | - | - |

**类型说明**: task(task节点) / agent(大模型) / condition(条件分支) / looparray(列表循环) / loopcond(条件循环)

## 技能使用
- 节点`news_search`使用技能`web-search`
- 节点`format_news`使用技能`大语言模型`
- 节点`push_message`使用技能`wechat-bot`

## 定时触发配置
- 触发时间: 每天 08:00 (Asia/Shanghai)
- 配置位置: `.coze` 文件的 `[trigger]` 节
- cron表达式: `0 8 * * *`
