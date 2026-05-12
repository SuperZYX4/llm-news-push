"""
使用大模型将搜索到的新闻整理成4条精炼的早间资讯节点
"""
import os
import json
import logging
from jinja2 import Template
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context, new_context
from coze_coding_dev_sdk import LLMClient
from graphs.state import FormatNewsInput, FormatNewsOutput

logger = logging.getLogger(__name__)


def format_news_node(
    state: FormatNewsInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> FormatNewsOutput:
    """
    title: 使用大模型将搜索到的新闻整理成4条精炼的早间资讯
    desc: 使用大模型将搜索到的新闻整理成4条精炼的早间资讯
    integrations: 大语言模型
    """
    try:
        # 从metadata读取LLM配置
        cfg_path = os.path.join(os.getenv("COZE_WORKSPACE_PATH"), config["metadata"]["llm_cfg"])
        with open(cfg_path, 'r') as fd:
            llm_cfg = json.load(fd)

        llm_config = llm_cfg.get("config", {})
        sp = llm_cfg.get("sp", "")
        up = llm_cfg.get("up", "")

        # 渲染用户提示词
        up_tpl = Template(up)
        user_prompt = up_tpl.render({"search_results": state.search_results})

        # 初始化LLM客户端
        ctx = new_context(method="invoke")
        client = LLMClient(ctx=ctx)

        # 构建消息
        messages = [
            SystemMessage(content=sp),
            HumanMessage(content=user_prompt)
        ]

        # 调用大模型
        response = client.invoke(
            messages=messages,
            model=llm_config.get("model", "doubao-seed-1-8-251228"),
            temperature=llm_config.get("temperature", 0.3),
            thinking=llm_config.get("thinking", {}).get("type", "disabled") if isinstance(llm_config.get("thinking"), dict) else "disabled",
            max_completion_tokens=llm_config.get("max_completion_tokens", 8192)
        )

        # 提取响应内容
        formatted_news = ""
        if isinstance(response.content, str):
            formatted_news = response.content
        elif isinstance(response.content, list):
            formatted_news = " ".join([item.get("text", "") if isinstance(item, dict) else str(item) for item in response.content])

        logger.info(f"新闻整理完成，内容长度: {len(formatted_news)}")
        return FormatNewsOutput(formatted_news=formatted_news)

    except Exception as e:
        logger.error(f"新闻整理失败: {e}")
        return FormatNewsOutput(formatted_news="新闻整理失败，请稍后重试")
