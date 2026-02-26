from pydantic import BaseModel,field_validator

class ChatRequest(BaseModel):
    user_input: str
    
    # @field_validator(user_input)
    # def input_validator(cls,user_input):
    #     if user_input.strip()==None:
    #         raise ValueError(f'Input should not be Empty')
    #     return user_input

 

class ChatResponse(BaseModel):
    result: str
