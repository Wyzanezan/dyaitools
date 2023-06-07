# coding: utf-8


import traceback

import openai
import tiktoken

from config import logger

openai.api_key = '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'


class Conversation(object):

    def __init__(self, prompt, model="text-davinci-003"):
        self.prompt = prompt
        self.model = model
        self.data_length = 4000

    def get_answer(self):
        response = openai.Completion.create(
            engine=self.model,
            prompt=self.prompt,      # 提示词
            max_tokens=2000,    # 生成结果的最大token数量
            n=1,                # 候选结果，只返回1个结果（如果返回多个结果，则每个结果都会消耗token）
            temperature=0,      # 生成结果时的创造性程度0~1
            stream=True,
        )
        return response

    def check_data_length(self, data):
        try:
            encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            logger.info("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")

        ret = encoding.encode(data)
        return len(ret)

    def ask_question(self):
        request_tokens = self.check_data_length(self.prompt)
        logger.info(f"request tokens num: {request_tokens}")

        if request_tokens > self.data_length:
            return 24003, "data too long"

        try:
            response = self.get_answer()
        except openai.error.RateLimitError:
            logger.info("request open ai rate limit, retry again ... ")

            try:
                response = self.get_answer()
            except Exception as e:
                logger.info(f"request open ai exception: {traceback.format_exc()}")
                response = None
        except openai.error.InvalidRequestError:
            logger.info(f"request open ai exception: {traceback.format_exc()}")
            return 24003, "data too long"
        except Exception as e:
            logger.info(f"request open ai exception: {traceback.format_exc()}")
            response = None

        logger.info(f"openai response info: {response}")
        if not response:
            return -1, "system error"

        resp_data = dict()
        resp_data["request_tokens"] = request_tokens

        completion_text = ''
        for resp in response:
            text = resp['choices'][0]['text']
            completion_text += text

        cost_tokens = self.check_data_length(completion_text)
        resp_data["cost_tokens"] = cost_tokens
        resp_data["answer"] = completion_text

        return 1000, resp_data


class ConversationNoneStream(object):

    def __init__(self, prompt, model="text-davinci-003"):
        self.prompt = prompt
        self.model = model
        self.data_length = 4000

    def get_answer(self):
        response = openai.Completion.create(
            engine=self.model,
            prompt=self.prompt,      # 提示词
            max_tokens=2000,    # 生成结果的最大token数量
            n=1,                # 候选结果，只返回1个结果（如果返回多个结果，则每个结果都会消耗token）
            temperature=0,      # 生成结果时的创造性程度0~1
        )
        return response

    def check_data_length(self):
        try:
            encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            logger.info("Warning: model not found. Using cl100k_base encoding.")
            encoding = tiktoken.get_encoding("cl100k_base")

        ret = encoding.encode(self.prompt)
        return len(ret)

    def ask_question(self):
        request_tokens = self.check_data_length()
        logger.info(f"request tokens num: {request_tokens}")

        if request_tokens > self.data_length:
            return 24003, "data too long"

        try:
            response = self.get_answer()
        except openai.error.RateLimitError:
            logger.info("request open ai rate limit, retry again ... ")

            try:
                response = self.get_answer()
            except Exception as e:
                logger.info(f"request open ai exception: {traceback.format_exc()}")
                response = None
        except openai.error.InvalidRequestError:
            logger.info(f"request open ai exception: {traceback.format_exc()}")
            return 24003, "data too long"
        except Exception as e:
            logger.info(f"request open ai exception: {traceback.format_exc()}")
            response = None

        logger.info(f"openai response info: {response}")
        if not response:
            return -1, "system error"

        resp_data = dict()
        usage = response.get("usage", {})
        resp_data["request_tokens"] = usage.get("prompt_tokens")
        resp_data["cost_tokens"] = usage.get("completion_tokens")
        resp_data["answer"] = ''

        choices = response.get("choices")
        if choices and choices[0]:
            message = choices[0].get("text")
            finish_reason = choices[0].get("finish_reason")
            if finish_reason == "stop" and message:
                resp_data["answer"] = message
        return 1000, resp_data
