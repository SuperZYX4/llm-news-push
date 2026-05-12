"""
大模型Agent新闻搜索节点
"""
import json
import logging
from typing import List
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from coze_coding_dev_sdk import SearchClient
from coze_coding_utils.runtime_ctx.context import new_context
from graphs.state import NewsSearchInput, NewsSearchOutput

logger = logging.getLogger(__name__)


def news_search_node(
    state: NewsSearchInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> NewsSearchOutput:
    """
    title: 新闻搜索
    desc: 搜索大模型Agent应用领域的最新前沿热点新闻
    integrations: web-search
    """
    try:
        ctx = new_context(method="search.news")
        client = SearchClient(ctx=ctx)

        # 搜索多个关键词，覆盖大模型Agent领域热点
        all_results: List[dict] = []
        search_queries = [
            "大模型Agent最新进展 2024",
            "AI Agent应用热点新闻",
            "LLM Agent技术突破",
            "多模态大模型最新动态",
            "Agent框架技术趋势"
        ]

        for query in search_queries:
            try:
                response = client.search(
                    query=query,
                    search_type="web",
                    count=5,
                    need_summary=True,
                    time_range="1w"  # 搜索最近一周的内容
                )

                if response.web_items:
                    for item in response.web_items:
                        news_item = {
                            "title": item.title,
                            "url": item.url,
                            "site_name": item.site_name,
                            "snippet": item.snippet,
                            "summary": item.summary,
                            "publish_time": item.publish_time
                        }
                        # 去重：避免重复添加相同新闻
                        if not any(r["url"] == news_item["url"] for r in all_results):
                            all_results.append(news_item)

                logger.info(f"关键词 '{query}' 搜索到 {len(response.web_items)} 条结果")
            except Exception as e:
                logger.warning(f"搜索 '{query}' 失败: {e}")
                continue

        logger.info(f"总共获取到 {len(all_results)} 条新闻")
        return NewsSearchOutput(search_results=all_results)

    except Exception as e:
        logger.error(f"新闻搜索失败: {e}")
        return NewsSearchOutput(search_results=[])
