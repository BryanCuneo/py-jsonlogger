import json
import sys
from datetime import datetime, timezone
from enum import IntEnum, StrEnum
from pathlib import Path
from typing import Optional


class Levels(IntEnum):
    DEBUG    = 10
    INFO     = 20
    SUCCESS  = 25
    WARNING  = 30
    ERROR    = 40
    FATAL    = 50
    VERBOSE  = 60

class ConsoleStyles(StrEnum):
    Simple    = "simple"
    TimeSpan  = "timespan"
    Timestamp = "timestamp"

_Loggers = {}

class Logger:
    JsonLoggerVersion = "1.3.0a"

    def __init__(self, path: str, programName: str, printToConsole: Optional[str] = None, encoding: str = "utf-8", overwrite = False) -> None:
        self.start_time = datetime.now(timezone.utc).astimezone().isoformat()
        self.path = Path(path)
        self.program_name = programName
        self.print_to_console = printToConsole
        self.encoding = encoding
        self.overwrite = overwrite

        if (self.overwrite or not self.path.is_file()):
            f = open(self.path, "w", encoding=self.encoding)
            f.close()
        elif(self.path.is_file()):
            raise FileExistsError(f"The file {self.path} already exists. use overwrite=True to overwrite it.")
        elif(self.path.exists() and not self.path.is_file()):
            raise IsADirectoryError(f"The file {self.path} is not a valid file.")

        initial_entry: dict[str, str] = {
            "timestamp": self.start_time,
            "level": "START",
            "programName": self.program_name,
            "pythonVersion": sys.version,
            "jsonLoggerVersion": self.JsonLoggerVersion,
        }

        try:
            initial_entry_json = json.dumps(initial_entry, indent=None)
            print("Hello")
            with open(self.path, "a", encoding=self.encoding) as f:
                f.write(initial_entry_json)

            if self.print_to_console is not None:
                print(f"{initial_entry["level"]} {datetime.fromisoformat(self.start_time).strftime('%Y-%m-%d %H:%M:%S')} {self.program_name}")
        except Exception as e:
            print(f"Error writing initial log entry: {e}")