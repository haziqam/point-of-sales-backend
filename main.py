from fastapi import FastAPI

from adapters.http.controllers.AuthController import AuthController, AuthService

app = FastAPI()

@app.get("/")
def health():
    return {"Hello": "World"}

auth_controller = AuthController()
auth_controller.set_auth_service(AuthService(10))
app.include_router(auth_controller)




