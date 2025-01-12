from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
import pandas as pd
from app.models import ModUser, ModUserProfile
from app.utils.validation import is_valid_email, validate_enum_value
from app.utils.enums import UserStatus

def insert_records(db: Session, data_frames: dict):
   try:
      for table_name, data in data_frames.items():
         if table_name == "mod_user":
            for index, row in data.iterrows():
               try:
                  email = row.get("email")
                  if not email or not is_valid_email(email):
                     raise HTTPException(status_code=400, detail=f"Invalid email format '{email}' in row {index + 1}.")

                  existing_user = db.query(ModUser).filter(ModUser.email == email).first()
                  if existing_user:
                     continue
                  
                  user = ModUser(
                     email=email,
                     password_hash=row["password_hash"],
                     auth_key=row.get("auth_key", None),
                     role_id=row["role_id"],
                     site_id=row.get("site_id", 1),
                     status=UserStatus.active,
                     created_by=row.get("created_by", 1),
                     updated_by=row.get("updated_by", 1),
                  )
                  db.add(user)
                  db.flush()

               except Exception as e:
                  db.rollback()
                  raise HTTPException(status_code=500, detail=f"Error processing user row {index + 1}: {str(e)}.")

         elif table_name == "mod_user_profile":
            for index, row in data.iterrows():
               try:
                  user_id = user.id
                  if not user_id:
                     raise HTTPException(status_code=400, detail=f"Missing user_id in row {index + 1}.")

                  phone = row.get("phone")
                  if phone:
                     existing_profile = db.query(ModUserProfile).filter(ModUserProfile.phone == phone).first()
                     if existing_profile:
                        continue

                  profile = ModUserProfile(
                     user_id=user_id,
                     first_name=row.get("first_name", None),
                     last_name=row.get("last_name", None),
                     gender=row.get("gender", None),
                     date_of_birth=row.get("date_of_birth", None),
                     avatar=row.get("avatar", None),
                     ba_address=row.get("ba_address", ""),
                     ba_city=row.get("ba_city", ""),
                     ba_country=row.get("ba_country", ""),
                     ba_zip_code=row.get("ba_zip_code", ""),
                     sa_address=row.get("sa_address", ""),
                     sa_city=row.get("sa_city", ""),
                     sa_country=row.get("sa_country", ""),
                     sa_zip_code=row.get("sa_zip_code", ""),
                     phone=phone,
                     newsletters=row.get("newsletters", "no"),
                     metadata=row.get("metadata", ""),
                     created_by=row.get("created_by", 1),
                     updated_by=row.get("updated_by", 1),
                     status=UserStatus.active,
                  )
                  db.add(profile)

               except Exception as e:
                  db.rollback()
                  raise HTTPException(status_code=500, detail=f"Error processing profile row {index + 1}: {str(e)}.")

      db.commit()
   except IntegrityError as e:
      db.rollback()
      raise HTTPException(status_code=500, detail=f"Database integrity error: {str(e)}.")
   except Exception as e:
      db.rollback()
      raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}.")
