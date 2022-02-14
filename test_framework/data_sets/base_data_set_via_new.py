class BaseDataSet:
    """
    Base class that describes the common attributes and methods for all product lines datasets.
    """

    def __new__(cls, *args, **kwargs):
        if cls is BaseDataSet:
            raise TypeError(f"Only children of '{cls.__name__}' may be instantiated!")
        return object.__new__(cls)

    instruments = None

    def get_instruments(self):
        if self.instruments:
            return self.instruments.__members__

    def get_instrument_by_name(self, name: str):
        if hasattr(self.instruments, name):
            return getattr(self.instruments, name).value
        raise ValueError(f"{self.instruments} not found!")


base_data_set_instance = BaseDataSet()
