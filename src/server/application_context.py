from dataclasses import dataclass


@dataclass
class DatabaseData:
    host: str
    port: int
    name: str
    user: str
    password: str


@dataclass
class LoggingData:
    host: str
    port: int


@dataclass
class ApplicationContext:
    port: int
    ssl: bool
    process_number: int
    env: str
    db_data: DatabaseData
    logging_data: LoggingData
