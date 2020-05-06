from typing import List

from src.database.daos.example_dao import ExampleDAO
from src.model.errors.business_error import BusinessError
from src.model.example_resource import ExampleResource


class ExampleCRUDService:

    @classmethod
    async def add(cls, resource: ExampleResource):
        # Check if resource with given id exists
        if await ExampleDAO.find(resource.id):
            raise BusinessError(f'Resource with ID {resource.id} already exists.', 409)
        # Store new resource
        await ExampleDAO.store(resource)

    @classmethod
    async def remove(cls, resource_id: str):
        # Check if doctor with given id exists
        if not await ExampleDAO.find(resource_id):
            raise BusinessError(f'There is no resource with id {resource_id}.', 404)
        await ExampleDAO.delete(resource_id)

    @classmethod
    async def update(cls, resource: ExampleResource):
        # Check if the resource to be modified exists
        if not await ExampleDAO.find(resource.id):
            raise BusinessError(f'There is no resource with id {resource.id}.', 404)
        # Modify resource
        await ExampleDAO.store(resource)

    @classmethod
    async def retrieve(cls, resource_id: str) -> ExampleResource:
        """ Returns the doctor object associated to the given ID, if existent. """
        resource = await ExampleDAO.find(resource_id)
        if not resource:
            raise BusinessError(f'There is no resource with id {resource_id}.', 404)
        return resource

    @classmethod
    async def retrieve_all(cls) -> List[ExampleResource]:
        """ Returns all doctors stored in the database. """
        return await ExampleDAO.all()

