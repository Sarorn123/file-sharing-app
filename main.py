import os
from fastapi import FastAPI, UploadFile, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from sqlmodel import select
from db import create_db_and_tables, SessionDep
from model import ImageTable, UserTable
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.mount("/static", StaticFiles(directory="./uploads"), name="static")

fake_users_db = {
    "johndoe": {
        "id": 1,
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "id": 2,
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}

# Ensure the "uploads" directory exists
UPLOAD_DIRECTORY = "./uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

def fake_decode_token(token):
    user = fake_users_db.get(token)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid token")
    return UserTable(**user)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


# Function to get user by ID
def get_user_by_id(user_id):
    for username, user_info in fake_users_db.items():
        if user_info["id"] == user_id:
            return user_info
    return None  # Return None if no user is found with the given ID


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {"access_token": user_dict["username"], "token_type": "bearer"}

@app.get("/me")
async def read_users_me(current_user: Annotated[UserTable, Depends(get_current_user)]):
    return current_user

@app.get("/")
async def root():
    return {"message": "Welcome to FastAPI File sharing app !"}

@app.get("/images")
async def read_users_me(db: SessionDep, current_user: Annotated[UserTable, Depends(get_current_user)]):
    images = db.exec(select(ImageTable)).all()
    result = []
    for image in images:
        if image.user_id == current_user.id:
            result.append(image)
        else:
            if image.is_public:
                result.append(image)
    
    final = []
    for image in result:
        final.append({
            "id": image.id,
            "filename": image.filename,
            "user_id": image.user_id,
            "is_public": image.is_public,
            "user" : get_user_by_id(image.user_id)["username"]
        })
    return final

@app.post("/upload")
async def upload_image(file: UploadFile, db: SessionDep, current_user: Annotated[UserTable, Depends(get_current_user)]  ) -> ImageTable :
    try:
        # Save file to the "uploads" directory
        filename = file.filename.replace(" ", "-").lower()
        file_path = os.path.join(UPLOAD_DIRECTORY, filename)
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        result = ImageTable(filename=filename, user_id=current_user.id)
        db.add(result)
        db.commit()
        db.refresh(result)
        return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error " + str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="An error occurred during upload") from e
    
@app.get("/set-public/")
async def public_image(id: str, db: SessionDep, current_user: Annotated[UserTable, Depends(get_current_user)]):
    try:
        print("=>", id)
        image = db.get(ImageTable, id)
        if image.user_id == current_user.id:
            if image.is_public:
                image.is_public = False
            else:
                image.is_public = True
            db.commit()
            return image
        else:
            raise HTTPException(status_code=403, detail="Permission denied")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error " + str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=400, detail="Image not found") from e