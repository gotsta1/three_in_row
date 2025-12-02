from domain.game.value_objects import Difficulty, CustomConfig


def preset_for_difficulty(difficulty: Difficulty) -> CustomConfig:
    if difficulty == Difficulty.easy:
        return CustomConfig(
            rows=12,
            cols=12,
            target_score=40,
            items_count=6,
            one_swap_reset=False,
            random_item_mode=False,
        )
    if difficulty == Difficulty.medium:
        return CustomConfig(
            rows=8,
            cols=8,
            target_score=50,
            items_count=6,
            one_swap_reset=True,
            random_item_mode=False,
        )
    if difficulty == Difficulty.hard:
        return CustomConfig(
            rows=8,
            cols=8,
            target_score=25,
            items_count=6,
            one_swap_reset=True,
            random_item_mode=True,
        )
    raise ValueError("No preset for custom difficulty")
