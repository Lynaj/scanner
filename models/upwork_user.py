import json
from pydantic import BaseModel, validator, constr, parse_obj_as
from typing import List

def length_validation(v: str) -> str:
    if(len(v) == 0):
      raise ValueError('can not be an empty value')
    return v.title()

def must_not_contain_space(v: str) -> str:
    if ' ' in v:
        raise ValueError('must not contain a space')
    return v.title()

class UpWorkUserRecord(BaseModel):
  username: constr(min_length=2, strip_whitespace=True)
  password: constr(min_length=2)
  secret: constr(min_length=2)
  opt_secret: str
  # validators
  _must_not_contain_space_username = validator('username', allow_reuse=True)(must_not_contain_space)

  @classmethod
  def parse_accounts_from_the_file(cls, path):
    # Make sure that it does not fail when file is missing
    try:
        with open(path) as json_file:
          data = json.load(json_file)
          account_list = parse_obj_as(List[cls], data)
          return account_list
    except:
        pass
