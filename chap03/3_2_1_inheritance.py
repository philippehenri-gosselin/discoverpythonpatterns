class Computation:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def compute(self):
        pass


class Sum(Computation):
    def compute(self):
        return self.x + self.y


class Product(Computation):
    def compute(self):
        return self.x * self.y


computations = [Sum(3, 2), Product(4, 5)]
for computation in computations:
    print(computation.compute())
