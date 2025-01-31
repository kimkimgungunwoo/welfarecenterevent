import uuid
from datetime import time
from typing import List
from fastapi import FastAPI, APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
import schema
import crud
from dep import get_db
import httpx
from dotenv import load_dotenv
import os,uuid,json,time
router = APIRouter()
load_dotenv()
secret_key = os.getenv("secret_key")
api_url=os.getenv("api_url")

if not api_url:
    raise ValueError("API_URL is not set. Please check your environment variables.")

if not secret_key:
    raise ValueError("SECRET_KEY is not set. Please check your environment variables.")

@router.post("", response_model=schema.PostInfo)
def create_post(post: schema.CreatePost, db: Session = Depends(get_db)):
    user_posts = crud.read_post_by_username(post.author_name, db)
    if user_posts and len(user_posts) >= 7:
        raise HTTPException(status_code=403, detail="Too many user's posts")
    new_post = crud.create_post(post, db)
    return new_post

@router.get("", response_model=schema.PostInfoList)
def read_posts(limit:int=9,offset:int=0,db: Session = Depends(get_db)):
    total,posts=crud.read_post(db, limit=limit, offset=offset)
    return {"total": total, "posts": posts}

@router.get("/search", response_model=schema.PostInfoList)
def search(username: str = Query(...),limit:int=9,offset:int=0, db: Session = Depends(get_db)):
    total,posts=crud.search_post_by_username(username, limit, offset,db)
    return {"total": total, "posts": posts}


# @router.get("/users/{username}", response_model=List[schema.PostInfo])
# def userposts(username: str, db: Session = Depends(get_db)):
#     user_posts = crud.read_post_by_username(username, db)
#     return user_posts

@router.get("/{post_id}", response_model=schema.PostDetail)
def read_post(post_id: int, db: Session = Depends(get_db)):
    return crud.find_post_by_id(post_id, db)

@router.delete("/{post_id}/del")
def delete_post(post_id: int, request: schema.DeleteRequest, db: Session = Depends(get_db)):
    if crud.delete_post_by_password(crud.find_post_by_id(post_id, db), request.password, db):
        return {"success": True, "message": "Post deleted successfully"}
    else:
        return {"success": False, "message": "Incorrect password"}

@router.post("/photo")
async def upload_photo(file: UploadFile = File(...)):
    try:
        # 파일 읽기
        content = await file.read()

        # 요청 JSON 생성
        request_json = {
            'images': [
                {
                    'format': 'jpg',
                    'name': 'demo'
                }
            ],
            'requestId': str(uuid.uuid4()),  # UUID 수정
            'version': 'V2',
            'timestamp': int(time.time() * 1000)
        }

        payload = {"message": json.dumps(request_json).encode('utf-8')}
        files = {
            "file": (file.filename, content, "application/octet-stream"),
        }

        headers = {
            "X-OCR-SECRET": secret_key  # 헤더 이름 확인 필요
        }

        # 외부 API 호출
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, headers=headers, data=payload, files=files)

        # 응답 상태 코드 확인
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="OCR API 요청 실패")

        # 결과 처리
        result_data = response.json()
        answer = " ".join(
            field["inferText"] for field in result_data["images"][0]["fields"]
        )

        return {"result": answer.strip()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))