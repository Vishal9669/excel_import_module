import enum

class UserStatus(enum.Enum):
   active = "active"
   inactive = "inactive"

class LoginSuccess(enum.Enum):
   yes = "yes"
   no = "no"