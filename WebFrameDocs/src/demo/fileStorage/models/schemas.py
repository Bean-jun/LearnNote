from pydantic import BaseModel


class ItemCreate(BaseModel):
    # 创建记录
    real_name: str
    facker_name: str
    date_path: str

    class Config:
        orm_mode = True


class GetItem(ItemCreate):
    # 获取文件记录
    pass
