from dataclasses import dataclass


@dataclass
class User:
    is_premium: bool
    is_admin: bool
    is_trial: bool
    region: str
