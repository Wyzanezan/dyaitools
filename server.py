# coding: utf-8


import tornado.web
from tornado import ioloop, httpserver

import config
from urls import urls
from config import logger


if __name__ == '__main__':
    app = tornado.web.Application(urls, **config.settings)

    http_server = httpserver.HTTPServer(app)
    http_server.listen(config.options.get("port"))

    logger.info("server start ...")
    ioloop.IOLoop.current().start()
