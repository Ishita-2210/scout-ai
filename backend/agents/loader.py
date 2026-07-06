"""
Prompt Loader.

Loads prompt templates for Scout agents.
"""

from functools import lru_cache
from pathlib import Path
from typing import Final


# ==========================================================
# Constants
# ==========================================================

BACKEND_DIR: Final = Path(__file__).resolve().parent.parent

PROMPTS_DIR: Final = BACKEND_DIR / "prompts"


# ==========================================================
# Prompt Loader
# ==========================================================

@lru_cache(maxsize=None)
def load_prompt(
    agent_name: str,
    filename: str,
) -> str:
    """
    Load a prompt file for a specific agent.

    Parameters
    ----------
    agent_name:
        Name of the agent prompt directory.

    filename:
        Prompt filename.

    Returns
    -------
    str
        Prompt contents.

    Raises
    ------
    FileNotFoundError
        If the prompt file does not exist.

    ValueError
        If the prompt file is empty.
    """

    prompt_path = PROMPTS_DIR / agent_name / filename

    if not prompt_path.exists():

        raise FileNotFoundError(
            f"Prompt file not found: {prompt_path}"
        )

    prompt = prompt_path.read_text(
        encoding="utf-8",
    ).strip()

    if not prompt:

        raise ValueError(
            f"Prompt file is empty: {prompt_path}"
        )

    return prompt