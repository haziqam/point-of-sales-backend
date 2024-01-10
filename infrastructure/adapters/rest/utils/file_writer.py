import os
import glob
from fastapi import UploadFile


def write_file(file: UploadFile, path: str) -> None:
    os.makedirs(os.path.split(path)[0], exist_ok=True)
    file_content = file.file.read()
    with open(path, "wb") as f:
        f.write(file_content)


def delete_file(path_without_ext: str) -> None:
    for f in glob.glob(f"{path_without_ext}.*"):
        os.remove(f)
