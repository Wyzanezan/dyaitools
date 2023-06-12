# coding: utf-8


import time
import tornado.web

from config import logger, white_list
from utils import ConversationStream, get_data_length


class ProjectAnalysisStreamHandler(tornado.web.RequestHandler):

    def initialize(self):
        # 设置响应头部
        self.set_header('Content-Type', 'text/event-stream')
        self.set_header('Cache-Control', 'no-cache')
        self.set_header('Connection', 'keep-alive')

    def prepare(self):
        ip = self.request.headers.get("X-Real-Ip", self.request.remote_ip)
        ip = self.request.headers.get("X-Forwarded-For", ip)
        ip = ip.split(',')[0].strip()

        logger.info(f"request ip is: {ip}")
        # if ip not in white_list:
        #     self.finish({"code": 24001, "answer": None})

    def post(self):
        """项目数据分析接口
        """
        prompt = self.get_body_argument("prompt")
        message = self.get_body_argument("message")
        logger.info(f"request prompt info is: {prompt}, message is: {message}")

        # 调用openai接口
        con = ConversationStream(prompt)
        response = con.ask_question(message)
        resp_code, answer = response[0], response[1]
        if resp_code != 1000:
            self.write(resp_code)

        request_tokens = answer["request_tokens"]
        answer = answer["response"]
        completion = ''
        for ans in answer:
            delta = ans["choices"][0]["delta"]
            if 'content' in delta:
                content = delta["content"]
                print(content)
                completion += content
                self.write(content + "\n\n")
                self.flush()

        cost_tokens = get_data_length(completion)
        self.write("content finish-" + str(request_tokens) + "-" + str(cost_tokens))
