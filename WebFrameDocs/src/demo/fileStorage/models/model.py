from sqlalchemy import Boolean, Column, Integer, String


from models.database import Base


class FileItem(Base):

    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    facker_name = Column(String, nullable=False, index=True)
    real_name = Column(String, nullable=False)
    date_path = Column(String, nullable=False)
    is_delete = Column(Boolean, default=False)
