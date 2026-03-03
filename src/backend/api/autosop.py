from fastapi import APIRouter, UploadFile, File
from utils.response_util import ResponseUtil
from service.friends_service import friends_service

autosop_router = APIRouter()

@autosop_router.post("/upload_friend_list")
async def upload_friend_list(file: UploadFile = File(...)):
    """
    上传好友名单文件，支持 xlsx, xls, csv
    文件格式：有3列（微信号/手机号，备注，标签）
    为什么显式处理首行：实际业务中首行经常为标题，若不额外判断，可能被当作数据导致脏数据进入名单
    """
    try:
        content = await file.read()
        filename = file.filename
        
        try:
            data = friends_service.parse_friend_list_file(content, filename)
            return ResponseUtil.success(msg="上传成功", data=data)
        except ValueError as ve:
            return ResponseUtil.failure(msg=str(ve))
            
    except Exception as e:
        return ResponseUtil.error(msg=f"处理文件失败: {str(e)}")
