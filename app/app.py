from fastapi import Request, status, FastAPI, Depends
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routing import todo,auth

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {}
    for error in exc.errors():
        # Get the field name (last element of the error location tuple)
        field_name = str(error["loc"][-1]) if error["loc"] else "body"
        # Store the clean error message directly
        errors[field_name] = error["msg"]
        
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"message":"validation error","detail": errors},
    )

app.include_router(todo.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {
        "message": "hello fast api",
    }