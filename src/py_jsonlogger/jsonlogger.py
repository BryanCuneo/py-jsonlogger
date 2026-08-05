import inspect
import json
import platform
import traceback
from datetime import UTC, datetime, timezone
from enum import IntEnum, StrEnum
from pathlib import Path


class Levels(IntEnum):
    DEBUG = 10
    INFO = 20
    SUCCESS = 25
    WARNING = 30
    ERROR = 40
    FATAL = 50
    VERBOSE = 60


class ConsoleStyles(StrEnum):
    SIMPLE = "simple"
    TIMESPAN = "timespan"
    TIMESTAMP = "timestamp"


_Loggers = {}


class Logger:
    JsonLoggerVersion = "1.3.0a"

    def __init__(
        self,
        path: str,
        programName: str,
        printToConsole: ConsoleStyles | str | None = None,
        encoding: str = "utf-8",
        overwrite=False,
    ) -> None:

        self.start_time = datetime.now(UTC).astimezone().isoformat()
        self.path = Path(path)
        self.program_name = programName
        self.encoding = encoding
        self.overwrite = overwrite

        if isinstance(printToConsole, str):
            printToConsole = printToConsole.lower()

        try:
            self.print_to_console = ConsoleStyles(printToConsole)
        except ValueError:
            raise ValueError(
                f"Invalid console style: {printToConsole}. Allowed: {[s.value for s in ConsoleStyles]}"
            ) from None

        if self.overwrite or not self.path.is_file():
            with open(self.path, "w", encoding=self.encoding):
                pass
        elif self.path.is_file():
            raise FileExistsError(
                f"The file {self.path} already exists. use overwrite=True to overwrite it."
            )
        elif self.path.exists() and not self.path.is_file():
            raise IsADirectoryError(f"The file {self.path} is not a valid file.")

        initial_entry: dict[str, str] = {
            "timestamp": self.start_time,
            "level": "START",
            "programName": self.program_name,
            "pythonVersion": platform.python_version(),
            "jsonLoggerVersion": self.JsonLoggerVersion,
        }

        try:
            initial_entry_json = json.dumps(initial_entry, indent=None)
            with open(self.path, "a", encoding=self.encoding) as f:
                f.write(initial_entry_json)

            if self.print_to_console is not None:
                print(
                    f"{initial_entry['level']} {datetime.fromisoformat(self.start_time).strftime('%Y-%m-%d %H:%M:%S')} {self.program_name}"
                )
        except Exception as e:  # noqa: BLE001
            print(f"Error writing initial log entry: {e}")

    def _add_to_initial_entry(self, newFieldName: str, value) -> None:
        pass

    def _log(
        self,
        level: Levels,
        message: str,
        called_from: str,
        context: list[object],
        include_call_stack: bool,
    ) -> None:
        pass

    def close(self, message: str | None = None) -> None:
        pass


class LogEntry:
    def __init__(
        self,
        level: Levels,
        message: str,
        called_from: str,
        context: list[object] | None = None,
        include_call_stack: bool = False,
    ) -> None:
        self.timestamp: str = datetime.now(UTC).astimezone().isoformat()
        self.level: Levels = level
        self.message: str = message
        self.called_from: str = called_from

        try:
            self.called_from: str = inspect.currentframe().f_back.f_code.co_name  # type: ignore
        except AttributeError:
            self.called_from = "unknown"

        if context is not None or not []:
            self.context = context

        if include_call_stack or self.level in [Levels.FATAL, Levels.VERBOSE]:
            self.call_stack = traceback.extract_stack()
        else:
            self.call_stack = None

    def __str__(self) -> str:
        str = f"Timestamp:\n\t{self.timestamp}\nLevel:\n\t{self.level.name}\nMessage:\n\t{self.message}\nCalled From:\n\t{self.called_from}\n"
        if self.context is not None:
            str += f"Context:\n\t{self.context}\n"
        if self.call_stack is not None:
            str += f"Call Stack:\n\t{self.call_stack}\n"
        return str

    def __repr__(self) -> str:
        return self.__str__()
