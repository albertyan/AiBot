from fastapi import APIRouter, UploadFile, File
from utils.response_util import ResponseUtil
import pandas as pd
import io

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
        
        df = None
        # 显式关闭头部推断（header=None），避免 pandas 将首行直接当作列名
        # 这么做的原因是：数据来源复杂，自动推断容易导致首行标题被丢失或错判
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(io.BytesIO(content), header=None)
        elif filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content), header=None)
        else:
            return ResponseUtil.failure(msg="不支持的文件格式")

        if df is None:
             return ResponseUtil.failure(msg="文件读取失败")
             
        # 确保至少有3列
        if len(df.columns) < 3:
            return ResponseUtil.failure(msg="文件格式错误，至少需要3列（微信号/手机号，备注，标签）")

        # 首行是否为标题的判断逻辑
        # 为什么需要判断：首行常见包含“微信号/手机号/备注/标签”等字样，直接纳入会污染数据
        def is_header_row(row_vals):
            header_keywords = ['微信号', '帐号', '账号', '手机号', '手机', '备注', '标签', '昵称']
            for v in row_vals:
                s = str(v).strip().lower()
                if not s:
                    continue
                # 命中常见中文字段或包含“号/名/标签”等明显非数据词
                if any(k in s for k in header_keywords):
                    return True
            return False

        start_idx = 0
        if df.shape[0] > 0:
            first_row_vals = df.iloc[0, :3].tolist()
            if is_header_row(first_row_vals):
                start_idx = 1  # 跳过标题行

        # 提取数据：前三列分别映射为 account / remark / tags
        # 为什么不依赖列名：来源文件列名不稳定，使用位置映射更稳健
        data = []
        for _, row in df.iloc[start_idx:, :3].iterrows():
            # 处理 NaN 值
            item = {
                "account": str(row[0]) if pd.notna(row[0]) else "",
                "remark": str(row[1]) if pd.notna(row[1]) else "",
                "tags": str(row[2]) if pd.notna(row[2]) else ""
            }
            # 过滤掉账号为空的行
            if item["account"].strip():
                data.append(item)
                
        return ResponseUtil.success(msg="上传成功", data=data)

    except Exception as e:
        return ResponseUtil.error(msg=f"处理文件失败: {str(e)}")
