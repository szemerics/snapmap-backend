from fastapi import APIRouter, HTTPException, Request, Response
from app.models.user import UserLogin, UserRegister
from app.utils.auth import auth


router = APIRouter()


@router.post("/login")
async def login_for_access_token(user_data: UserLogin, response: Response):
    try:
        token = await auth.login_auth(user_data, response)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return token


@router.post("/register")
async def register(user_data: UserRegister, response: Response):
    try:
        token = await auth.register_auth(user_data, response)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return token
    

@router.post("/logout")
async def logout(response: Response):
    try:
        await auth.logout_auth(response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "Logged out successfully"}


@router.post("/refresh")
async def refresh(response: Response, request: Request):
    try:
        token = await auth.refresh_auth(response, request)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return token