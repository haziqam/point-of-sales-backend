from fastapi import FastAPI

from adapters.http.controllers.example import ExampleController, ExampleService

app = FastAPI()

@app.get("/")
def health():
    return {"Hello": "World"}

example_controller = ExampleController()
example_controller.set_example_service(ExampleService(10))
app.include_router(example_controller)




