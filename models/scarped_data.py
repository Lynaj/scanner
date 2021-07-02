from pydantic import BaseModel

class MetadataDict(BaseModel):
    id: str = None

class AddressDict(BaseModel):
    line1: str = None
    line2: str = None
    city: str = None
    state: str = None
    postal_code: str = None
    country: str = None

class ScarpedData(BaseModel):
    id: str = None
    account: str = None
    employer: str = None
    created_at: str = None
    updated_at: str = None
    first_name: str = None
    last_name: str = None
    full_name: str = None
    email: str = None
    phone_number: str = None
    birth_date: str = None
    picture_url: str = None
    address: AddressDict
    ssn: str = None
    marital_status: str = None
    gender: str = None
    metadata: MetadataDict