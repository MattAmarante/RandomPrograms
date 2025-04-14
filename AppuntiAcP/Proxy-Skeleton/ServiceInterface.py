from abc import ABC,abstractmethod

class ServiceInterface(ABC):

    @abstractmethod
    def sendCmd(self,CommandID:int) -> None:
        pass

    @abstractmethod
    def getCmd(self) -> int:
        pass