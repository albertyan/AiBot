from fastapi import APIRouter
from utils.response_util import ResponseUtil

router = APIRouter()


@router.get("/license")
def get_license():
    return ResponseUtil.success(data={"license": "This is the license information."})