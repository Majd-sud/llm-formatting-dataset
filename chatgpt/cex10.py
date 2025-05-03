from json import load
from dataclasses import dataclass
from typing import Set


@dataclass
class Config:
    """Configuration model for supported algorithms."""
    ALGORITHMS: Set[str]


def load_config(config_file_path: str = "./Config.json") -> Config:
    """
    Load the configuration file and return a Config instance.

    Args:
        config_file_path: Path to the JSON config file.

    Returns:
        A Config object with algorithm settings.
    """
    with open(config_file_path, 'r', encoding='utf-8') as fp:
        data = load(fp)
        return Config(**data)


# Optional test function (currently does nothing)
def test_function() -> None:
    pass

    # Uncomment below to test all encode/decode algorithms
    #
    # from shell.api import ENCODE, DECODE
    # from shell.algorithms import ENCODING_ALGORITHMS as ALGO
    #
    # did_not_work = {}
    # for algo_name in ALGO:
    #     try:
    #         encoded = ALGO[algo_name][ENCODE]("String_")
    #     except Exception as e:
    #         print(f"ENCODE ERROR [{algo_name}]:", e)
    #         did_not_work[algo_name] = [ENCODE]
    #
    #     try:
    #         decoded = ALGO[algo_name][DECODE](encoded)
    #     except Exception as e:
    #         print(f"DECODE ERROR [{algo_name}]:", e)
    #         if algo_name in did_not_work:
    #             did_not_work[algo_name].append(DECODE)
    #         else:
    #             did_not_work[algo_name] = [DECODE]
    #
    # if did_not_work:
    #     print("Failures:", did_not_work)
    # else:
    #     print("Success: All algorithms worked as expected!")
