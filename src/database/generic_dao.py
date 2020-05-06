class GenericDAO:

    @classmethod
    async def get_first(cls, query, projection_dict=None):
        """
        Get first entry matching the given query.
            :returns Full document
        """
        return await cls.collection().find_one(query, projection_dict)

    @classmethod
    async def get_all(cls, query=None, projection_dict=None):
        """
        Get all entries matching the given query. If there is no query, full collection is returned.
            :returns List of full documents
        """
        cursor = cls.collection().find({} if query is None else query, projection_dict)
        documents = []
        while await cursor.fetch_next:
            documents.append(cursor.next_object())
        return documents

    @classmethod
    async def get_all_sorted(cls, query=None, projection_dict=None, sort_list=None):
        """
        Get all entries matching the given query. If there is no query, full collection is returned.
        An example of `sort_list` is [('call_millis', pymongo.ASCENDING)]
            :returns List of full documents
        """
        sort_list = [('_id', 1)] if not sort_list else sort_list
        cursor = cls.collection().find({} if query is None else query, projection_dict).sort(sort_list)
        documents = []
        while await cursor.fetch_next:
            documents.append(cursor.next_object())
        return documents

    @classmethod
    async def insert(cls, element):
        """
        Insert given element into collection.
            :returns An instance of InsertOneResult (ior.inserted_id gives the created id)
        """
        return await cls.collection().insert_one(element)

    @classmethod
    async def insert_many(cls, element):
        """
        Insert all elements from list into collection.
            :returns An instance of InsertManyResult (imr[].inserted_id gives the created id)
        """
        return await cls.collection().insert_many(element)

    @classmethod
    async def upsert(cls, query, update_dict):
        """
        Creates entry if it doesn't exists and updates it if it does.
            :returns Updated document
        """
        return await cls.collection().find_one_and_update(filter=query,
                                                          update=update_dict,
                                                          upsert=True)

    @classmethod
    async def delete_first(cls, query):
        """
        Delete first element matching the given query from collection.
            :returns An instance of DeleteResult (dr.delete_count returns the amount of deleted documents)
        """
        return await cls.collection().find_one_and_delete(query)

    @classmethod
    async def delete_all(cls, query=None):
        """
        Delete all entries matching the given query. If there is no query, collection is cleared.
            :returns An instance of DeleteResult (dr.delete_count returns the amount of deleted documents)
        """
        return await cls.collection().delete_many({} if query is None else query)

    @classmethod
    async def delete_with_ids(cls, ids: list):
        """
        Delete all entries which id is in the given list.
        """
        await cls.collection().delete_many({'_id': {'$in': ids}})

    @classmethod
    async def update_first(cls, query, updated_fields_dict):
        """
        Update first entry matching given query with the given dictionary.
            :returns Updated document
        """
        return await cls.collection().find_one_and_update(filter=query,
                                                          update={'$set': updated_fields_dict})

    @classmethod
    def collection(cls):
        # Subclass responsibility
        pass
