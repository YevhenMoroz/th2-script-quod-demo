from enum import Enum
from abc import ABC, abstractmethod


class RetInstruments(Enum):
    instrument_1 = "RELIANCE"
    instrument_2 = "SPICEJET"
    instrument_3 = "TCS"
    instrument_4 = "T55FD"
    instrument_5 = "SBIN"


class AbstractDataSet(ABC):
    """
    Abstract class that describes the common attributes and methods for all product lines datasets.
    """

    @property
    def instruments(self) -> RetInstruments:
        raise NotImplementedError

    @abstractmethod
    def get_instruments(self) -> list:
        pass

    @abstractmethod
    def get_instrument_by_name(self, name: str) -> str:
        pass


class BaseDataSet(AbstractDataSet):
    """
    Base class that describes the common attributes and methods for all product lines datasets.
    """

    instruments = None

    def get_instruments(self) -> RetInstruments.__members__:
        if self.instruments:
            return self.instruments.__members__

    def get_instrument_by_name(self, name: str) -> str:
        if hasattr(self.instruments, name):
            return getattr(self.instruments, name).value
        raise ValueError(f"{self.instruments} not found!")


class RetDataSet(BaseDataSet):
    """
    Product line dataset class that overrides attributes from BaseDataSet parent class.
    """
    instruments = RetInstruments

    def get_instruments(self) -> str:
        result = super().get_instruments()
        return f'returned from RetDataSet {result}'

    def get_instrument_by_name(self, name: str) -> str:
        result = super().get_instrument_by_name(name)
        return f'returned from RetDataSet {result}'


base_data_set = BaseDataSet()
print(base_data_set.get_instruments())
print(base_data_set.get_instrument_by_name(""))

# ret_data_set = RetDataSet()
# print(ret_data_set.get_instruments())
# print(ret_data_set.get_instrument_by_name('instrument_1'))
#
# assert issubclass(RetDataSet, BaseDataSet)
# assert isinstance(RetDataSet(), BaseDataSet)
