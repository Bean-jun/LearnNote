from datetime import date
from typing import List

from APIResource import core
from config import FILE_PATH
from fastapi import (APIRouter, BackgroundTasks, Depends, File, UploadFile, status)
from fastapi.responses import FileResponse
from models import crud, schemas
from models.database import SessionLocal
from sqlalchemy.orm import Session
from utils.file_save_name import save_facker_name, save_facker_name_plus

route = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@route.get("/")
async def upload_file_test():
    return {"msg": "ok", "code": status.HTTP_200_OK}


@route.post("/upload")
async def upload_file(background_save_tasks: BackgroundTasks, db: Session = Depends(get_db), file: UploadFile = File(...)):
    facker_name = save_facker_name_plus(save_facker_name(file.filename))
    background_save_tasks.add_task(core.save_file, file, facker_name, FILE_PATH)
    dic_item = schemas.ItemCreate(real_name=file.filename,
                                  facker_name=facker_name,
                                  date_path=date.today().strftime("%Y/%m/%d"))
    instance = crud.create_item(db, dic_item)
    return {"msg": "ok", "code": status.HTTP_200_OK, "file_id": instance.facker_name}


@route.post("/uploads")
async def upload_files(background_save_tasks: BackgroundTasks, db: Session = Depends(get_db), file_list: List[UploadFile] = File(...)):
    facker_name_list = []
    date_path = date.today().strftime("%Y/%m/%d")
    for file in file_list:
        facker_name = save_facker_name_plus(save_facker_name(file.filename))
        background_save_tasks.add_task(
            core.save_file, file, facker_name, FILE_PATH)
        dic_item = schemas.ItemCreate(real_name=file.filename,
                                      facker_name=facker_name,
                                      date_path=date_path)
        instance = crud.create_item(db, dic_item)
        facker_name_list.append(instance.facker_name)

    return {"msg": "ok", "code": status.HTTP_200_OK, "file_id": facker_name_list}


@route.get("/download/{filename}")
async def download_file(filename: str, db: Session = Depends(get_db)):
    instance = crud.get_item(db, filename)
    if instance and instance.is_delete is False:
        all_path = "{}/{}/{}".format(FILE_PATH,
                                     instance.date_path, instance.facker_name)
        return FileResponse(all_path, filename=instance.real_name)
    else:
        return {"msg": "fail", "code": status.HTTP_404_NOT_FOUND}


@route.put("/delete/{filename}")
async def delete_file(filename: str, db: Session = Depends(get_db)):
    instance = crud.get_item(db, filename)
    if instance and instance.is_delete is False:
        instance.is_delete = True
        crud.delete_item(db, instance)
        return {"msg": "ok", "code": status.HTTP_200_OK}
    else:
        return {"msg": "fail", "code": status.HTTP_404_NOT_FOUND}
