from fastapi import APIRouter

router = APIRouter()


@router.get("/license")
def get_license():
    return {"license": "This is the license information."}