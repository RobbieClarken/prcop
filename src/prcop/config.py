from dataclasses import dataclass


@dataclass
class Config:
    database: str = "/tmp/prcopdb.json"
    verify_https: bool = True
