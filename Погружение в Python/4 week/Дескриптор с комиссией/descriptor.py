class Value:

    def __init__(self, amount=None):
        self.amount = amount or 0

    def __get__(self, instance, owner):
        return self.amount

    def __set__(self, instance, value):
        self.amount = value * (1.0 - instance.commission)


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission
