import json
import os
from io import BufferedReader

from . import client


class OpenAiFiles:
    __client = client

    def __init__(self, to_dict=False):
        self.to_dict = to_dict

    def get_files(self):
        response = self.__client.files.list()
        if self.to_dict:
            return json.loads(response.model_dump_json())
        return response.data

    def get_file_content(self, file_id):
        response = self.__client.files.content(file_id=file_id)
        return response

    def get_file(self, id):
        response = self.__client.files.retrieve(id)
        if self.to_dict:
            return json.loads(response.model_dump_json())
        return response

    def upload_file(self, file: BufferedReader | str, purpose="assistant"):
        if isinstance(file, str):
            if os.path.exists(file):
                _file = open(file, "rb")
            else:
                raise ValueError("File Does not exists.")
        elif isinstance(file, BufferedReader):
            _file = file
        else:
            raise ValueError("Invalid File type.")
        response = self.__client.files.create(file=_file, purpose=purpose)
        if self.to_dict:
            return json.loads(response.model_dump_json())
        return response

    
    def delete_file(self, id):
        response = self.__client.files.delete(id)
        self.get_files()
        if self.to_dict:
            return json.loads(response.model_dump_json())
        return response

    def set_dict(self, to_dict):
        self.to_dict = to_dict
