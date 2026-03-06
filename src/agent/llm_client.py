
import json
import requests

# api_base, api_key, model_name来源于环境变量，环境变量文件即设置是团队另外的人在搭建。
class LLMClient:
    def __init__(self, model_name: str, api_key: str, api_base: str):
        self.model_name = model_name
        self.api_key = api_key
        self.api_base = api_base
        self.assistant_prompt = '' # Agent的系统提示词等待Agent示例创建代码完成再编写
        self.context = [] # Agent的上下文短期对话记录等待Message模块完成再编写
        self.history_file_path = '' # Agent的上下文长期对话记录文件路径等待Message模块完成再编写

    def chat(self, user_prompt: str) -> str:
        """
        与大模型进行对话的基础方法，用于与模型进行一次对话，返回模型的回复。
        :param user_prompt: 用户的输入提示词
        :return: 模型的回复
        """
        messages = self._assemble_message(self.assistant_prompt, self.context, user_prompt)
        response = self._send_message(messages)
        return response

    def _send_message(self, messages: list) -> str:
        """
        发送消息给大模型并返回模型的回复。
        :param messages: 要发送的消息列表
        :return: 模型的回复
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        data = {
            "model": self.model_name,
            "messages": messages
        }
        response = requests.post(self.api_base, headers=headers, data=json.dumps(data), timeout=60)
        return response

    def _assemble_message(self, assistant_prompt: str, context: list, user_prompt: str) -> list:
        """
        组装消息，将系统提示词、上下文和用户提示词合并为消息列表。
        :param assistant_prompt: 系统提示词
        :param context: 短期多轮对话记录，格式为 [{"role": "user/assistant", "content": "..."}]
        :param user_prompt: 用户提示词
        :return: 组装后的消息列表
        """
        messages = []
        if assistant_prompt:
            messages.append({"role": "system", "content": assistant_prompt})
        if context:
            context_obj = {
                "type": "context",
                "description": "Short-term conversation history",
                "history": context
            }
            messages.append({"role": "system", "content": json.dumps(context_obj, ensure_ascii=False)})
        if user_prompt:
            messages.append({"role": "user", "content": user_prompt})
        return messages

