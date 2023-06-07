# coding: utf-8


from AnalysisHandler import ProjectAnalysisHandler
from AnalysisWebsocket import ProjectAnalysisWebsocket


urls = [
    (r'/vis/ai/analysis/', ProjectAnalysisHandler),
    (r'/ai/analysis/websocket/', ProjectAnalysisWebsocket),
]
