"""
d
"""
from abc import ABC, abstractmethod


class Communication(ABC):
    """
    d
    """
    def __init__(self):
        self.ip_address = "10.10.15.58"
        self.img_port = 5555
        self.str_port = 6666
        self.wav_port = 7777
        self.tmp_port = 8888
    
    @abstractmethod
    def receive(self):
        """d"""
        pass
