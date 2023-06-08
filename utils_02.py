# coding: utf-8


import traceback

import openai
import tiktoken

from config import logger

openai.api_key = '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'


class Conversation(object):

    def __init__(self, prompt, model="gpt-3.5-turbo-0301"):
        self.prompt = prompt
        self.model = model
        self.data_length = 2000
        self.messages = []
        self.messages.append({"role": 'system', "content": self.prompt})

    def get_answer(self, message):
        self.messages.append({"role": 'user', "content": message})
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
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

    def ask_question(self, message):
        request_tokens = self.check_data_length()
        logger.info(f"request tokens num: {request_tokens}")

        if request_tokens > self.data_length:
            return 24003, "data too long"

        try:
            response = self.get_answer(message)
        except openai.error.RateLimitError:
            logger.info("request open ai rate limit, retry again ... ")

            try:
                response = self.get_answer(message)
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
            return 24001, "system error"

        resp_data = dict()
        resp_data["answer"] = ''
        resp_data["request_tokens"] = request_tokens
        resp_data["cost_tokens"] = response.get("usage", {}).get("total_tokens")

        choices = response.get("choices")
        if choices and choices[0]:
            message = choices[0].get("message", {})
            finish_reason = choices[0].get("finish_reason")
            if finish_reason == "stop" and message:
                resp_data["answer"] = message.get("content")
        return 1000, resp_data


class ConversationStream(object):

    def __init__(self, prompt, model="gpt-3.5-turbo-0301"):
        self.prompt = prompt
        self.model = model
        self.data_length = 2000
        self.messages = []
        self.messages.append({"role": 'system', "content": self.prompt})

    def get_answer(self, message):
        self.messages.append({"role": 'user', "content": message})
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=self.messages,
            max_tokens=2000,
            stream=True
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

    def ask_question(self, message):
        request_tokens = self.check_data_length()
        logger.info(f"request tokens num: {request_tokens}")

        if request_tokens > self.data_length:
            return 24003, "data too long"

        try:
            response = self.get_answer(message)
        except openai.error.RateLimitError:
            logger.info("request open ai rate limit, retry again ... ")

            try:
                response = self.get_answer(message)
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
            return 24001, "system error"

        return 1000, response