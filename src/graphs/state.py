"""
大模型Agent新闻推送工作流状态定义
"""
from typing import List, Optional
from pydantic import BaseModel, Field


class GlobalState(BaseModel):
    """全局状态定义"""
    search_results: List[dict] = Field(default_factory=list, description="搜索到的新闻结果列表")
    formatted_news: str = Field(default="", description="整理后的新闻内容")
    push_result: str = Field(default="", description="推送结果")


class GraphInput(BaseModel):
    """工作流的输入"""
    trigger_time: str = Field(default="08:00", description="触发时间")


class GraphOutput(BaseModel):
    """工作流的输出"""
    push_result: str = Field(..., description="推送结果")


class NewsSearchInput(BaseModel):
    """新闻搜索节点的输入"""
    pass


class NewsSearchOutput(BaseModel):
    """新闻搜索节点的输出"""
    search_results: List[dict] = Field(..., description="搜索到的新闻结果列表")


class FormatNewsInput(BaseModel):
    """新闻整理节点的输入"""
    search_results: List[dict] = Field(..., description="搜索到的新闻结果列表")


class FormatNewsOutput(BaseModel):
    """新闻整理节点的输出"""
    formatted_news: str = Field(..., description="整理后的新闻内容")


class PushMessageInput(BaseModel):
    """消息推送节点的输入"""
    formatted_news: str = Field(..., description="整理后的新闻内容")


class PushMessageOutput(BaseModel):
    """消息推送节点的输出"""
    push_result: str = Field(..., description="推送结果")
