from typing import Iterable, Optional

RESET_PENALTY = 5


def compute_score(
    removed_items: Iterable[str],
    random_item_mode: bool,
    random_item: Optional[str],
) -> int:
    if random_item_mode:
        return sum(1 for i in removed_items if i == random_item)
    return sum(1 for _ in removed_items)


def apply_reset_penalty(score: int) -> int:
    return max(0, score - RESET_PENALTY)
