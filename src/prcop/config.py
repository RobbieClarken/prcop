from dataclasses import dataclass


@dataclass
class Config:
    database: str = "prcopdb.json"
    verify_https: bool = True
