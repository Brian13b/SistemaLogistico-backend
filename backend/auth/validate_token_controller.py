from fastapi import APIRouter, Depends, HTTPException
from auth.dependencies import get_current_user

router = APIRouter()

@router.get("/validate-token")
def validate_token(current_user = Depends(get_current_user)):
    return {"detail": "Token is valid"}