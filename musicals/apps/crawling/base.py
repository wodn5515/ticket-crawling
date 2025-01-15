from abc import ABCMeta, abstractmethod


class BaseCrwaling(metaclass=ABCMeta):
    @abstractmethod
    def crawl_data(self):
        pass

    @abstractmethod
    def data_to_db(self):
        pass
