import abc
from abc import ABCMeta


class AbstractPropertyElement:
    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def init_element(self, prop_name, prop_val):
        raise NotImplementedError

    @abc.abstractmethod
    def set_prop_val(self, prop_name, prop_val):
        raise NotImplementedError

    @abc.abstractmethod
    def get_prop_val(self, prop_name):
        raise NotImplementedError
