def add(a:int, b:int):
    return a + b

def subtract(a:int, b:int):
    return a - b

def multiply(a:int, b:int):
    return a * b

def divide(a:int, b:int):
    return a / b

# TEST

def test_add():
    assert add(1,2)==3

def test_subtract():
    assert subtract(1,2)==1

def test_multiply():
    assert multiply(10,10)==  100

def test_divide():
    assert divide(25,100)==4