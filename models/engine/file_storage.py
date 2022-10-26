#!/usr/bin/python3
"""This module contains the FileStorage class."""

import os
import json
from importlib import import_module
from pathlib import Path


class FileStorage:
    """This class handles object serialization and saving to file, file
    loading and deserialization to object.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """returns the dictionary `__objects`"""

        return self.__objects

    def new(self, obj):
        """sets in `__objects` the `obj` with key `<obj class name>.id`

        Args:
            obj(Object): The object to be added to `__objects`
        """

        if not isinstance(obj, self.get_class("BaseModel")):
            return

        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """serializes `__objects` to the JSON file `(path: __file_path)`"""

        objects = {}
        for key in self.__objects:
            obj = self.__objects[key]

            if obj is not None:
                objects[key] = obj.to_dict()
        raw = json.dumps(objects)
        with open(self.__file_path, mode="w", encoding="utf-8") as fp:
            fp.write(raw)

    def get_class(self, name):
        """Returns class of a given name"""

        models_path = os.path.dirname(os.path.realpath(__file__))
        for filename in os.listdir(Path(models_path).parent.absolute()):
            if (not filename.startswith("__")):
                module_name = filename.split(".")[0]
                module = import_module("models.{}".format(module_name))
                try:
                    return getattr(module, name)
                except AttributeError as ex:
                    pass

    def reload(self):
        """deserializes the JSON file to `__objects`"""

        if not os.path.isfile(self.__file_path):
            return
        raw = {}
        with open(self.__file_path, encoding="utf-8") as fp:
            raw = json.load(fp)
        if type(raw) is dict:
            self.__objects = {}
            for key in raw:
                attributes = raw[key]
                className = attributes['__class__']
                del attributes['__class__']
                obj_class = self.get_class(className)
                obj = obj_class(**attributes)
                self.__objects[key] = obj
