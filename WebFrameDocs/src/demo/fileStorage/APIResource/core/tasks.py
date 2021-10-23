from datetime import date
from pathlib import Path
from fastapi import UploadFile


def _mkdir(path):
    try:
        p = Path(path)
        p.mkdir(parents=True)
    except FileExistsError:
        pass


async def save_file(file: UploadFile, facker_filename: str, path: Path):
    # 文件路径
    date_path = date.today().strftime("%Y/%m/%d")
    prefix_path = "{}/{}".format(str(path), date_path)

    _mkdir(prefix_path)

    all_path = "{}/{}".format(prefix_path, facker_filename)

    with open(all_path, "wb") as f:
        content = await file.read()
        f.write(content)
