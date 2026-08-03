from py_jsonlogger import *

def test_logs():
    logger = Logger(path="test.log", programName="test", printToConsole="simple", overwrite=True)
