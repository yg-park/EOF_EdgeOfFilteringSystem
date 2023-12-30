from abc import ABC, abstractmethod

class Communication(ABC):
    
    @abstractmethod
    def receive(self):
        pass