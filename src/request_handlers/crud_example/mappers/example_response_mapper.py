from typing import List

from src.model.example_resource import ExampleResource


class ExampleResponseMapper:

    @classmethod
    def map_many(cls, resources: List[ExampleResource]) -> list:
        return [cls.map(resource) for resource in resources]

    @staticmethod
    def map(resource: ExampleResource) -> dict:
        return {
            'id': resource.id,
            'name': resource.name,
            'value': resource.value,
        }
