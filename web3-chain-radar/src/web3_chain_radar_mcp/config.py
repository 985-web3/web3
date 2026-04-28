from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _load_dotenv() -> None:
    env_path = Path.cwd() / ".env"
    if not env_path.exists():
        return

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def _float_env(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        return default


@dataclass(frozen=True)
class Settings:
    default_chains: tuple[str, ...] = ("eth", "bsc", "base", "sol")
    min_market_cap: float = 1_000
    max_market_cap: float = 10_000_000
    min_liquidity: float = 500
    request_timeout: float = 15


def load_settings() -> Settings:
    _load_dotenv()
    chains = tuple(
        chain.strip().lower()
        for chain in os.getenv("WEB3_RADAR_DEFAULT_CHAINS", "eth,bsc,base,sol").split(",")
        if chain.strip()
    )
    return Settings(
        default_chains=chains or ("eth", "bsc", "base", "sol"),
        min_market_cap=_float_env("WEB3_RADAR_MIN_MARKET_CAP", 1_000),
        max_market_cap=_float_env("WEB3_RADAR_MAX_MARKET_CAP", 10_000_000),
        min_liquidity=_float_env("WEB3_RADAR_MIN_LIQUIDITY", 500),
    )

