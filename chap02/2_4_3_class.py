class MyClass:

    def __init__(self, value):
        self.value = value

    def incValue(self):
        self.value += 1


myClass = MyClass(10)
myClass.incValue()
print(myClass.value)
