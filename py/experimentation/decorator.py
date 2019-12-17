import abc

class Component(metaclass=abc.ABCMeta):
    """ 
    base component interface for defining operations that can be
    altered by decorators 
    """

    @abc.abstractmethod
    def operation(self):
        pass


class Decorator(Component, metaclass=abc.ABCMeta):
    _component = None

    def __init__(self, component):
        self._component = component


    @abc.abstractmethod
    def operation(self):
        pass

class ConcreteDecoratorA(Decorator):
    def operation(self):
        print("concrete decorator operation: BEFORE")
        # code
        self._component.operation()
        # code
        print("concrete decorator operation: AFTER")

class ConcreteComponentA(Component):
    def operation(self):
        print("concrete component A operation called")
    
class ConcreteComponentB(Component):
    def operation(self):
        print("concrete component B operation called")

if __name__ == '__main__':
    componentA = ConcreteComponentA()
    componentB = ConcreteComponentB()

    decorator = ConcreteDecoratorA(componentA)
    decorator.operation()




