# coding: utf-8


import json
import tornado.websocket

from config import logger
from utils import ConversationStream


class ProjectAnalysisWebsocket(tornado.websocket.WebSocketHandler):

    def open(self):
        logger.info("WebSocket opened ...")

    def on_message(self, message):
        logger.info("request message info: ", message)

        message = json.loads(message)
        prompt = message.get("prompt")
        con = ConversationStream(prompt)
        code, response = con.ask_question()

        if code != 1000:
            self.write(json.dumps({"code": code, "text": ''}))
            self.on_close()

        if code == 1000:
            for resp in response:
                self.write_message(resp['choices'][0]['text'])
            self.write_message("text end")
            self.on_close()

    def on_close(self):
        logger.info("WebSocket closed ...")
