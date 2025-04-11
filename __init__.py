"""这是一个示例天气查询插件

提供指定城市的天气查询功能。
使用 wttr.in API 获取天气数据。
"""

from typing import Dict, List

import httpx
from pydantic import Field

from nekro_agent.api import message
from nekro_agent.api.schemas import AgentCtx
from nekro_agent.core import logger
from nekro_agent.services.plugin.base import ConfigBase, NekroPlugin, SandboxMethodType

# TODO: 插件元信息，请修改为你的插件信息
plugin = NekroPlugin(
    name="呼叫管理员",
    module_name="nekro_plugin_report",
    description="向管理员打小报告! 遇到突发事件时可向管理员发送消息", 
    version="0.1.0",
    author="Zaxpris",
    url="https://github.com/zxjwzn/nekro-plugin-report", 
)


@plugin.mount_config()
class ReportConfig(ConfigBase):
    """呼叫管理员配置"""

    admin_qqs: List[str] = Field(
        default=[],
        title="管理员QQ号列表",
        description="需要接收报告的管理员QQ号列表",
    )
    admin_groups: List[str] = Field(
        default=[],
        title="管理群号列表",
        description="需要接收报告的管理群号列表",
    )


# 获取配置实例
config: ReportConfig = plugin.get_config(ReportConfig)


@plugin.mount_sandbox_method(SandboxMethodType.TOOL, name="呼叫管理员", description="向管理员打小报告! 遇到突发事件时可向管理员发送消息")
async def report(_ctx: AgentCtx, msg: str):
    """向管理员打小报告! 遇到突发事件时可向管理员发送消息

    Args:
        msg: 要报告的内容
    """
    sent_to = []
    errors = []

    # 发送给管理员QQ
    for qq in config.admin_qqs:
        chat_key = f"private_{qq}"
        try:
            await message.send_text(chat_key, msg, _ctx)
            logger.info(f"已向管理员QQ '{qq}' 发送报告")
            sent_to.append(chat_key)
        except Exception as e:
            error_msg = f"向管理员QQ '{qq}' ({chat_key}) 发送报告时发生错误: {e}"
            logger.error(error_msg)
            errors.append(error_msg)

    # 发送给管理群
    for group in config.admin_groups:
        chat_key = f"group_{group}"
        try:
            await message.send_text(chat_key, msg, _ctx)
            logger.info(f"已向管理群 '{group}' 发送报告")
            sent_to.append(chat_key)
        except Exception as e:
            error_msg = f"向管理群 '{group}' ({chat_key}) 发送报告时发生错误: {e}"
            logger.error(error_msg)
            errors.append(error_msg)

    if not sent_to and errors:
        # 如果所有发送都失败了，则抛出异常
        raise Exception(f"发送报告失败，错误详情: {'; '.join(errors)}")
    if errors:
        # 如果部分发送失败，记录警告但认为操作部分成功
        logger.warning(f"部分报告发送失败: {'; '.join(errors)}")

    logger.info(f"报告已成功发送给: {', '.join(sent_to)}")


@plugin.mount_cleanup_method()
async def clean_up():
    """清理插件资源"""
