"""
大模型Agent新闻推送主图编排
"""
from langgraph.graph import StateGraph, END
from graphs.state import (
    GlobalState,
    GraphInput,
    GraphOutput
)
from graphs.nodes.news_search_node import news_search_node
from graphs.nodes.format_news_node import format_news_node
from graphs.nodes.push_message_node import push_message_node

# 创建状态图
builder = StateGraph(GlobalState, input_schema=GraphInput, output_schema=GraphOutput)

# 添加节点
builder.add_node("news_search", news_search_node, metadata={"type": "task"})
builder.add_node("format_news", format_news_node, metadata={"type": "agent", "llm_cfg": "config/news_format_llm_cfg.json"})
builder.add_node("push_message", push_message_node, metadata={"type": "task"})

# 设置入口点
builder.set_entry_point("news_search")

# 添加边
builder.add_edge("news_search", "format_news")
builder.add_edge("format_news", "push_message")
builder.add_edge("push_message", END)

# 编译图
main_graph = builder.compile()
