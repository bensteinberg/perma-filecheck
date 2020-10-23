import os
import shutil
import subprocess
from tempfile import NamedTemporaryFile
import filetype
from fastapi import FastAPI, File, UploadFile


# settings
app = FastAPI()
allowed_types = {
    'image/jpeg': {'jpeg', 'jpg'},
    'image/gif': {'gif'},
    'image/png': {'png'},
    'application/pdf': {'pdf'},
}


@app.get("/")
async def home():
    return {"hello": "world"}


@app.post("/scan/")
def scan(file: UploadFile = File(...)):
    with NamedTemporaryFile() as f:
        # write file
        shutil.copyfileobj(file.file, f)
        f.flush()
        os.fsync(f.fileno())
        os.chmod(f.name, 0o644)

        # check file type
        guess = filetype.guess(f.name)
        if not guess:
            return {"safe": False, "reason": "unrecognized file type"}
        if guess.mime not in allowed_types:
            return {"safe": False, "reason": "invalid file type"}
        extension = file.filename.rsplit('.', 1)[-1].lower()
        if extension not in allowed_types[guess.mime]:
            return {"safe": False, "reason": "invalid file extension"}

        # scan with clamav
        clam_result = subprocess.run(["clamdscan", f.name, "--no-summary"], check=False, capture_output=True)
        if clam_result.returncode:
            return {"safe": False, "reason": "clamav"}

    return {"safe": True}
