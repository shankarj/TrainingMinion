import abc
from abc import ABCMeta


class AbstractElement:
    __metaclass__ = ABCMeta

    @abc.abstractmethod
    def init_element(self):
        raise NotImplementedError

    @abc.abstractmethod
    def train_forward_pass(self):
        raise NotImplementedError

    @abc.abstractmethod
    def train_backward_pass(self):
        raise NotImplementedError

    @abc.abstractmethod
    def execute(self, **args):
        raise NotImplementedError

    @abc.abstractmethod
    def on_train_done(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_prop_interfaces(self):
        raise NotImplementedError
