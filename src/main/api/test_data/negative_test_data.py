import random
from typing import get_type_hints, get_origin, get_args, Annotated

from src.main.api.generators.creation_rule import CreationRule


class NegativeTestData:

    @staticmethod
    def _get_rule(cls: type, field_name: str):
        annotated_type = get_type_hints(cls, include_extras=True)[field_name]

        if get_origin(annotated_type) is Annotated:
            _, *annotations = get_args(annotated_type)

            for ann in annotations:
                if isinstance(ann, CreationRule):
                    return ann

        raise ValueError(f"CreationRule not found for {cls.__name__}.{field_name}")

    @staticmethod
    def below_min(cls: type, field_name: str):
        rule = NegativeTestData._get_rule(cls, field_name)
        return random.uniform(0, rule.min_value - 1)

    @staticmethod
    def above_max(cls: type, field_name: str):
        rule = NegativeTestData._get_rule(cls, field_name)
        return random.uniform(rule.max_value + 1, rule.max_value * 2)