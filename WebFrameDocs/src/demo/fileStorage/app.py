from fastapi import FastAPI
import uvicorn
from APIResource import v1
from models.database import Base, engine


Base.metadata.create_all(bind=engine)
app = FastAPI()


app.include_router(v1.route, prefix="/v1", tags=["文件上传下载API"])


if __name__ == "__main__":
    uvicorn.run("app:app", debug=True, reload=True, workers=1)
