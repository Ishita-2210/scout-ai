from pathlib import Path


# Root backend directory
BACKEND_DIR = Path(__file__).resolve().parent.parent

# Prompt directory
PROMPTS_DIR = BACKEND_DIR / "prompts"


def load_prompt(agent_name: str, filename: str) -> str:
    """
    Load a prompt file for a specific agent.

    Args:
        agent_name: Agent prompt folder.
        filename: Prompt filename.

    Returns:
        Prompt contents.
    """

    prompt_path = PROMPTS_DIR / agent_name / filename

    if not prompt_path.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {prompt_path}"
        )

    return prompt_path.read_text(
        encoding="utf-8"
    )