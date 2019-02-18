from dataclasses import dataclass


@dataclass
class Config:
    verify_https: bool = True
