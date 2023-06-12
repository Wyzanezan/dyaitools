# coding: utf-8


from AnalysisHandler import ProjectAnalysisHandler
from AnalysisStreamHandler import ProjectAnalysisStreamHandler


urls = [
    (r'/vis/ai/analysis/', ProjectAnalysisHandler),
    (r'/vis/ai/analysis/stream', ProjectAnalysisStreamHandler),
]
