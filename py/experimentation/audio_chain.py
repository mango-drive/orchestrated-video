from abc import ABC, abstractmethod

class AudioProcessingHandler(ABC):
    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def process(self, samples):
        pass


muted = False

class AbstractAudioProcessingHandler(AudioProcessingHandler):
    _next_handler : AudioProcessingHandler = None

    def set_next(self, handler):
        self._next_handler = handler
        # Returning a handler from here will let us link handlers in a
        # convenient way like this:
        # monkey.set_next(squirrel).set_next(dog)
        return handler

    @abstractmethod
    def process(self, samples):
        if self._next_handler:
            print("Abstract process called")
            return self._next_handler.process(samples)
        
        return samples

class Filter(AbstractAudioProcessingHandler):
    def __init__(self, name):
        self.name = name

    def process(self, samples):
        print("filter ", self.name, "processed audio" )
        samples += self.name
        return super().process(samples)


