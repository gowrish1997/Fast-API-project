from pydantic import BaseModel,Field,EmailStr, field_validator

class Login(BaseModel):
    email:EmailStr=Field(...,description="The email of the user")
    password:str=Field(...,description="The password of the user",min_length=8,max_length=100)

class Register(BaseModel):
    username:str=Field(...,description="The username of the user",min_length=3,max_length=50)
    email:EmailStr=Field(...,description="The email of the user")
    password:str=Field(...,description="The password of the user",min_length=8,max_length=100)
    confirm_password:str=Field(...,description="The confirm password of the user",min_length=8,max_length=100)

    @field_validator("confirm_password")
    @classmethod
    def validate_confirm_password(cls, value, values):
        if "password" in values and value != values["password"]:
            raise ValueError("Passwords do not match")
        return value