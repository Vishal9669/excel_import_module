import re
from typing import List

def validate_enum_value(column_name: str, value: str, valid_values: List[str]) -> str:
   if value in valid_values:
      return value
   else:
      raise ValueError(f"Invalid value '{value}' for column '{column_name}'. Valid options are: {valid_values}")

def is_valid_email(email: str) -> bool:
   email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
   return re.match(email_regex, email) is not None
