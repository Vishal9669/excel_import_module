from fastapi import FastAPI, UploadFile, File, Depends,HTTPException
from app.database import get_db, Base, engine
from app.models import ModUser, ModUserProfile
from .utils.excel_utils import parse_excel_file
from .utils.crud import insert_records
from sqlalchemy.orm import Session

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.post("/upload/")
async def upload_data(file: UploadFile = File(...), db: Session = Depends(get_db)):
   data_frames = parse_excel_file(file)
   insert_records(db, data_frames)
   return {"message": "Data uploaded successfully."}

@app.delete("/delete_user/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
   try:
      user = db.query(ModUser).filter(ModUser.id == user_id).first()
      if not user:
         raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found.")
      db.query(ModUserProfile).filter(ModUserProfile.user_id == user_id).delete()
      db.query(ModUser).filter(ModUser.id == user_id).delete()
      db.commit()
      return {"message": f"User with ID {user_id} deleted successfully."}
   except Exception as e:
      db.rollback()
      raise HTTPException(status_code=500, detail=f"Error deleting user: {str(e)}")