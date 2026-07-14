def decorator(func):
    print("Decorator is executing")
    return func

@decorator
def home():
    print("inside Home")

print("Program finished")