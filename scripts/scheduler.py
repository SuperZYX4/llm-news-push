"""
定时调度脚本 - 每天早上8点自动推送新闻
使用方法: python scripts/scheduler.py
"""
import schedule
import time
import logging
import sys
import os
import asyncio
import json

# 添加项目路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from coze_coding_utils.runtime_ctx.context import new_context
from coze_coding_utils.helper.graph_helper import get_graph_instance

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def run_news_workflow():
    """执行新闻推送工作流"""
    try:
        logger.info("=" * 50)
        logger.info("开始执行新闻推送工作流...")
        
        # 获取工作流实例
        graph = get_graph_instance("graphs.graph")
        
        # 创建上下文
        ctx = new_context(method="scheduler")
        
        # 构造输入
        payload = {
            "trigger_time": "08:00"
        }
        
        # 执行工作流
        result = asyncio.run(graph.ainvoke(payload, config={"configurable": {"thread_id": f"schedule_{int(time.time())"}}}))
        
        logger.info(f"工作流执行完成: {result}")
        return result
        
    except Exception as e:
        logger.error(f"工作流执行失败: {e}")
        raise


def main():
    """主函数"""
    logger.info("定时调度器启动")
    logger.info("每天 08:00 将自动执行新闻推送工作流")
    
    # 每天早上8点执行
    schedule.every().day.at("08:00").do(run_news_workflow)
    
    logger.info("调度器已配置，等待下次执行时间...")
    
    # 持续运行
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次


if __name__ == "__main__":
    main()
