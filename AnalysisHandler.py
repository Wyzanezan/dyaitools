# coding: utf-8


import time
import tornado.web

from config import logger, white_list
from utils_02 import Conversation, ConversationStream


class ProjectAnalysisHandler(tornado.web.RequestHandler):

    def prepare(self):
        ip = self.request.headers.get("X-Real-Ip", self.request.remote_ip)
        ip = self.request.headers.get("X-Forwarded-For", ip)
        ip = ip.split(',')[0].strip()

        logger.info(f"request ip is: {ip}")
        if ip not in white_list:
            self.finish({"code": 24001, "answer": None})

    def post(self):
        """项目数据分析接口
        """
        start_time = time.time()
        prompt = self.get_body_argument("prompt")
        message = self.get_body_argument("message")
        logger.info(f"request prompt info is: {prompt}, message is: {message}")

        # 调用openai接口
        # con = Conversation(prompt)
        con = ConversationStream(prompt)
        response = con.ask_question(message)
        resp_code, answer = response[0], response[1]
        logger.info(f"answer info is: {answer}")

        if resp_code != 1000:
            self.write({"code": resp_code, "answer": answer})

        self.set_header("Content-type", "application/stream")
        for resp in response:
            content = resp["choice"][0]["delta"]["content"]
            logger.info(f"content: {content}")
            self.write({"code": resp_code, "answer": content})


