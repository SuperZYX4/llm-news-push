"""
大模型Agent新闻消息推送节点
"""
import re
import json
import logging
import requests
from coze_workload_identity import Client
from cozeloop.decorator import observe
from langchain_core.runnables import RunnableConfig
from langgraph.runtime import Runtime
from coze_coding_utils.runtime_ctx.context import Context
from graphs.state import PushMessageInput, PushMessageOutput

logger = logging.getLogger(__name__)


def get_webhook_key() -> str:
    """获取企业微信webhook key"""
    try:
        client = Client()
        wechat_bot_credential = client.get_integration_credential("integration-wechat-bot")
        logger.info(f"获取到的集成凭证类型: {type(wechat_bot_credential)}")
        logger.info(f"获取到的集成凭证内容: {wechat_bot_credential}")
        
        # 尝试解析
        if isinstance(wechat_bot_credential, str):
            credential_dict = json.loads(wechat_bot_credential)
        elif isinstance(wechat_bot_credential, dict):
            credential_dict = wechat_bot_credential
        else:
            raise ValueError(f"未知的凭证类型: {type(wechat_bot_credential)}")
        
        # 尝试获取 webhook_key 或 webhook_url
        webhook_key = credential_dict.get("webhook_key", "")
        webhook_url = credential_dict.get("webhook_url", "")
        
        if webhook_key:
            key = webhook_key
        elif webhook_url:
            # 如果是完整URL，提取key
            if "key=" in webhook_url:
                key = re.search(r"key=([a-zA-Z0-9-]+)", webhook_url).group(1)
            else:
                key = webhook_url
        else:
            raise ValueError(f"webhook_key为空，凭证内容: {credential_dict}")
            
        logger.info(f"成功获取webhook_key: {key[:10]}...")
        return key
        
    except Exception as e:
        logger.error(f"获取webhook_key失败: {e}")
        raise


@observe
def send_markdown_message(content: str) -> dict:
    """发送markdown消息"""
    webhook_key = get_webhook_key()
    SEND_URL = f"https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={webhook_key}"

    payload = {
        "msgtype": "markdown",
        "markdown": {
            "content": content
        }
    }

    try:
        response = requests.post(SEND_URL, json=payload, headers={"Content-Type": "application/json"}, timeout=15)
        response.raise_for_status()
        result = response.json()
        if result.get("errcode") == 0:
            logger.info("Markdown消息发送成功")
        else:
            logger.error(f"消息发送失败: {result.get('errmsg')}")
        return result
    except Exception as e:
        logger.error(f"消息发送异常: {e}")
        raise


def push_message_node(
    state: PushMessageInput,
    config: RunnableConfig,
    runtime: Runtime[Context]
) -> PushMessageOutput:
    """
    title: 消息推送
    desc: 将整理好的新闻资讯通过企业微信机器人推送给用户
    integrations: wechat-bot
    """
    try:
        # 构建推送消息
        from datetime import datetime
        today = datetime.now().strftime("%Y年%m月%d日")

        push_content = f"""🤖 **大模型Agent早间资讯** 
📅 {today}

{state.formatted_news}

---
💡 由AI工作流自动生成推送"""

        # 发送消息
        result = send_markdown_message(push_content)

        if result.get("errcode") == 0:
            push_result = "推送成功"
        else:
            push_result = f"推送失败: {result.get('errmsg')}"

        logger.info(f"推送结果: {push_result}")
        return PushMessageOutput(push_result=push_result)

    except Exception as e:
        logger.error(f"消息推送失败: {e}")
        return PushMessageOutput(push_result=f"推送失败: {str(e)}")
