from pydantic import BaseModel

class VendorSchema(BaseModel):
    id: int
    name: str
    description: str

    class Config:
        from_attributes = True  # Enables the use of ORM mode in Pydantic v2
