# Nekro Agent 插件 - 呼叫管理员 (nekro-plugin-report)

[![Version](https://img.shields.io/badge/version-0.1.0-blue)](pyproject.toml)
[![Author](https://img.shields.io/badge/author-Zaxpris-brightgreen)](https://github.com/zxjwzn)
[![License](https://img.shields.io/badge/license-MIT-orange)](LICENSE) <!-- 如果您有 LICENSE 文件，请取消注释 -->
[![Repo](https://img.shields.io/badge/repository-GitHub-blue)](https://github.com/zxjwzn/nekro-plugin-report)

一个为 [Nekro Agent](https://github.com/KroMiose/nekro-agent) 设计的插件，允许 Agent 在遇到紧急情况或需要人工干预时，向预先配置好的管理员发送消息。

## 功能特性

*   **消息推送**: 可以将指定内容发送给一个或多个管理员 QQ 或指定的管理群组。
*   **简单配置**: 通过配置文件轻松添加或移除接收报告的管理员 QQ 和群组。
*   **错误处理**: 对发送失败的情况进行记录和报告。

## 安装

1.  确保已安装 Nekro Agent。
2.  通过 Nekro Agent 的 WebUI 或其他插件管理方式安装本插件。

## 配置

插件提供以下配置项 (`ReportConfig`)：

*   `admin_qqs` (List[str]): 需要接收报告的管理员 QQ 号列表 (例如: `["10001", "10002"]`)。
*   `admin_groups` (List[str]): 需要接收报告的管理群号列表 (例如: `["123456", "789012"]`)。

请在 Nekro Agent 的 WebUI 中插件配置部分找到 "呼叫管理员" 插件并设置这些参数。

## 内置方法

该插件向 Agent 提供了以下可调用的工具 (Tool):

*   **`呼叫管理员` (Tool)**
    *   **描述**: 向管理员打小报告! 遇到突发事件时可向管理员发送消息。
    *   **参数**:
        *   `msg` (str): 需要发送给管理员的内容。 **重要**: 在调用此工具时，请保持当前扮演的人设，并在消息中清晰说明事件发生的 `chat_key` (会话标识)、涉及人员以及事情的经过。
    *   **返回**: 无显式返回，操作成功或失败会记录在日志中。如果部分或全部发送失败，可能会记录警告或引发异常。
    *   **示例**: `呼叫管理员("报告管理员，用户 Nekro (QQ: 114514) 在群聊 group_123456 中发送了不当内容，请尽快处理。")`

## 注意事项

*   请确保填写的管理员 QQ 号和群号正确无误。
*   Agent 需要有向对应 QQ 或群聊发送消息的权限。

## 贡献

欢迎提交 Issues 和 Pull Requests。

## 作者

Zaxpris ([https://github.com/zxjwzn](https://github.com/zxjwzn))
