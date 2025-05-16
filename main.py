from datetime import timedelta
from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import badminton_model
from deps import fake_users_db, get_current_active_user
from models import Token, User
from security import ACCESS_TOKEN_EXPIRE_MINUTES, authenticate_user, create_access_token

app = FastAPI()

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="token")


def is_playable(weather: badminton_model.Weather):
    model = badminton_model.BadmintonModel("model/model.pkl")
    return {"playability": model.predict(weather)}


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.post("/playability")
def playability(weather: badminton_model.Weather, current_user: Annotated[str, Depends(get_current_active_user)]):
    playability = is_playable(weather)
    return playability


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
