from typing import List

from src.database.generic_dao import GenericDAO
from src.database.mongo import Mongo
from src.model.example_resource import ExampleResource


class ExampleDAO(GenericDAO):

    @classmethod
    async def find(cls, resource_id: str) -> ExampleResource:
        """ Return resource with given id if existent. """
        document = await cls.get_first({'_id': resource_id})
        # Get instance directly from its name
        return None if not document else cls.__to_object(document)

    @classmethod
    async def all(cls) -> List[ExampleResource]:
        """ Returns all resources stored in the database. """
        documents = await cls.get_all()
        return [cls.__to_object(document) for document in documents]

    @classmethod
    async def store(cls, resource: ExampleResource):
        """ Creates if non existent, updates otherwise. """
        await cls.upsert(
            {'_id': resource.id},
            {'$set': cls.__to_document(resource)}
        )

    @classmethod
    async def delete(cls, resource_id: str):
        await cls.delete_first({'_id': resource_id})

    @classmethod
    def __to_object(cls, document: dict) -> ExampleResource:
        return ExampleResource(
            id=document['_id'],
            name=document['name'],
            value=document['value']
        )

    @classmethod
    def __to_document(cls, resource: ExampleResource) -> dict:
        document = dict()
        # Add only existent fields to the document. This way we can create and update with the same code
        if resource.name: document['name'] = resource.name
        if resource.value: document['value'] = resource.value
        # Return create/update document
        return document

    @classmethod
    def collection(cls):
        return Mongo.get().example
