class Foo:
    def __init__(self):
        self._x = 5

    @property
    def x(self):
        return self._x
    
    @x.setter
    def set_x(self, x):
        print('first set')
        self._x = x + 10

        self.x.setter(self.set_x_normal)

    def set_x_normal(self, x):
        print('second set')
        self._x = x
    
    def noop(self):
        print('second')

    def setup(self):
        print("first")

        self.setup = self.noop

f = Foo()
f.setup()
f.setup()

print(f.x)
f.x = 10
print(f.x)
f.x = 7
print(f.x)