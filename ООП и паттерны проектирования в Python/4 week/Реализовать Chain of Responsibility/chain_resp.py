class EventGet:

    def __init__(self, type_value):
        self.type_value = type_value


class EventSet:

    def __init__(self, value):
        self.value = value


class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""


class NullHandler:

    def __init__(self, successor=None):
        self.__successor = successor

    def handle(self, obj, event):
        if self.__successor is not None:
            return self.__successor.handle(obj, event)


class IntHandler(NullHandler):

    def handle(self, obj, event):
        if isinstance(event, EventGet) and event.type_value == int:
            return obj.integer_field
        elif isinstance(event, EventSet) and type(event.value) == int:
            obj.integer_field = event.value
        else:
            return super().handle(obj, event)


class FloatHandler(NullHandler):

    def handle(self, obj, event):
        if isinstance(event, EventGet) and event.type_value == float:
            return obj.float_field
        elif isinstance(event, EventSet) and type(event.value) == float:
            obj.float_field = event.value
        else:
            return super().handle(obj, event)


class StrHandler(NullHandler):

    def handle(self, obj, event):
        if isinstance(event, EventGet) and event.type_value == str:
            return obj.string_field
        elif isinstance(event, EventSet) and type(event.value) == str:
            obj.string_field = event.value
        else:
            return super().handle(obj, event)
