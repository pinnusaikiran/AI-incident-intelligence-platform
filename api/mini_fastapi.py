class MyFastApi:
    def __init__(self):
        self.routes={}
    def get(self,path):
        print(f"creating decorator for {path}.")
        def decorator(func):
            print(f"Registering function {func.__name__}")
            self.routes[path]=func
            
            return func
        return decorator
        return self.routes
app=MyFastApi()

@app.get("/")
def home():
    print("Inside home")

print("Program finished")

print(type(home))
print(callable(home))

print(app.routes)