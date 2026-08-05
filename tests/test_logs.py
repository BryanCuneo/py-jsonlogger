from py_jsonlogger import *

# def test_logs():
#    logger = Logger(path="test.log", programName="test", printToConsole="simple", overwrite=True)

logger = Logger(
    path="test.log",
    programName="test",
    printToConsole=ConsoleStyles.SIMPLE,
    overwrite=True,
)

log_entry = LogEntry(level=Levels.DEBUG, message="This is a test", called_from="test")
print(log_entry)
