"""
Scout Runner Provider.

Provides a singleton ScoutRunner instance.
"""

from backend.execution.runner import ScoutRunner


_runner: ScoutRunner | None = None


def get_runner() -> ScoutRunner:
    """
    Return the singleton ScoutRunner instance.
    """

    global _runner

    if _runner is None:
        _runner = ScoutRunner()

    return _runner