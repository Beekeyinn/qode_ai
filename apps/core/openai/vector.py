import json
from . import client


class OpenAiVectorStore:
    __client = client

    def __init__(self, to_dict=False):
        self.to_dict = to_dict  


    def create_vector_store(self, name: str, metadata: dict[str, str]):
        response = self.__client.beta.vector_stores.create(name=name,metadata=metadata)
        if self.to_dict:
            return json.loads(response.model_dump_json())
        return response
    
    def retrive_vector_store(self, id: str):
        response = self.__client.beta.vector_stores.retrieve(id)
        if self.to_dict:
            return json.loads(response.model_dump_json())
        return response 
    
    def vector_list(self):
        response = self.__client.beta.vector_stores.list()
        if self.to_dict:
            return json.loads(response.model_dump_json())
        return response 
    def delete_vector_store(self, id: str):
        response = self.__client.beta.vector_stores.delete(id)
        if self.to_dict:
            return json.loads(response.model_dump_json())
        return response
    
    def vector_store_file_create(self, id: str, file_id: str):
        response = self.__client.beta.vector_stores.files.create_and_poll(
            vector_store_id=id, file_id=file_id,
            poll_interval_ms=5000
        )
        if self.to_dict:
            return json.loads(response.model_dump_json())
        return response
    
    def vector_store_file_list(self, id: str):
        response = self.__client.beta.vector_stores.files.list(vector_store_id=id)
        if self.to_dict:
            return json.loads(response.model_dump_json())
        return response
    

    def vector_store_file_create_batch(self, id: str, file_ids: list[str]):
        response = self.__client.beta.vector_stores.file_batches.create_and_poll(
            vector_store_id=id, file_ids=file_ids,
            poll_interval_ms=5000
        )
        if self.to_dict:
            return json.loads(response.model_dump_json())
        return response
    