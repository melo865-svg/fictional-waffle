import uuid
import random
from typing import Any, get_type_hints, get_origin, Annotated, get_args

import rstr


class RandomModelGenerator:
    @staticmethod
    def generate(cls: type, **overrides) -> Any:
        type_hints = get_type_hints(cls, include_extras=True)
        init_data = {}

        for field_name in type_hints:
            if field_name in overrides:
                init_data[field_name] = overrides[field_name]
            else:
                init_data[field_name] = RandomModelGenerator.generate_field(cls, field_name)

        return cls(**init_data)

    @staticmethod
    def _generate_from_regex(regex: str, field_type:type) -> Any:
        generated = rstr.xeger(regex)
        if field_type is int:
            return int(generated)
        elif field_type is float:
            return float(generated)
        return generated

    @staticmethod
    def _generate_value(field_type: type) -> Any:
        if field_type is str:
            return str(uuid.uuid4())[:8]
        elif field_type is int:
            return random.randint(1, 9999)
        elif field_type is float:
            return round(random.uniform(0, 100), 2)
        elif field_type is bool:
            return random.choice([True, False])
        elif field_type is list:
            return [str(uuid.uuid4())[:5]]
        elif isinstance(field_type, type):
            return RandomModelGenerator.generate(field_type)
        return None

    @staticmethod
    def generate_field(cls: type, field_name: str) -> Any:
        type_hints = get_type_hints(cls, include_extras=True)
        annotated_type = type_hints[field_name]

        rule = None
        actual_type = annotated_type

        if get_origin(annotated_type) is Annotated:
            actual_type, *annotations = get_args(annotated_type)

            for ann in annotations:
                from src.main.api.generators.creation_rule import CreationRule
                if isinstance(ann, CreationRule):
                    rule = ann

        if rule and rule.regex:
            return RandomModelGenerator._generate_from_regex(rule.regex, actual_type)

        if rule and rule.min_value is not None and rule.max_value is not None:
            if actual_type is int:
                return random.randint(rule.min_value, rule.max_value)
            elif actual_type is float:
                return round(random.uniform(rule.min_value, rule.max_value), 2)

            raise TypeError(f"Unsupported type for range generation: {actual_type}")

        return RandomModelGenerator._generate_value(actual_type)