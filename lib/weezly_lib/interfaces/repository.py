from abc import ABC, abstractmethod

class BaseRepository(ABC):
    @abstractmethod
    def list(self, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, entity_id, *args, **kwargs):
        pass

    @abstractmethod
    def create(self, entity, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, entity):
        pass

    @abstractmethod
    def delete(self, entity_id, *args, **kwargs):
        pass