from sqlalchemy import Column, Integer, String, Date, Text, Enum, ForeignKey
from sqlalchemy.orm import relationship, deferred
from datetime import datetime
from .database import Base
from .utils.enums import UserStatus

class ModUser(Base):
   __tablename__ = "mod_user"
   id = Column(Integer, primary_key=True, index=True)
   email = Column(String(255), unique=True, nullable=False)
   password_hash = Column(String(255), nullable=False)
   auth_key = Column(String(255))
   password_reset_token = Column(String(255))
   access_token = Column(String(255))
   role_id = Column(Integer, ForeignKey("mod_user_role.id"))
   site_id = Column(Integer)
   user_metadata = deferred(Column('metadata', Text))  # Renamed for clarity
   created_by = Column(Integer)
   updated_by = Column(Integer)
   created_at = Column(Date, default=datetime.now)
   updated_at = Column(Date, default=datetime.now)
   status = Column(Enum(UserStatus))
   profile = relationship("ModUserProfile", back_populates="user")

class ModUserProfile(Base):
   __tablename__ = "mod_user_profile"
   id = Column(Integer, primary_key=True, index=True)
   user_id = Column(Integer, ForeignKey("mod_user.id"))
   first_name = Column(String(255))
   last_name = Column(String(255))
   gender = Column(String(50))
   date_of_birth = Column(Date)
   avatar = Column(String(255))
   ba_address = Column(String(255))
   ba_city = Column(String(255))
   ba_country = Column(String(255))
   ba_zip_code = Column(String(20))
   sa_address = Column(String(255))
   sa_city = Column(String(255))
   sa_country = Column(String(255))
   sa_zip_code = Column(String(20))
   phone = Column(String(20))
   newsletters = Column(String(10))
   profile_metadata = deferred(Column('metadata', Text))  # Renamed for clarity
   created_by = Column(Integer)
   updated_by = Column(Integer)
   created_at = Column(Date, default=datetime.now)
   updated_at = Column(Date, default=datetime.now)
   status = Column(Enum(UserStatus))
   user = relationship("ModUser", back_populates="profile")

class ModUserRole(Base):
   __tablename__ = "mod_user_role"
   id = Column(Integer, primary_key=True, index=True)
   name = Column(String(255))
   description = Column(Text)
   created_by = Column(Integer)
   updated_by = Column(Integer)
   created_at = Column(Date, default=datetime.now)
   updated_at = Column(Date, default=datetime.now)
   status = Column(Enum(UserStatus))