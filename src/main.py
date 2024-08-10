from typing import Annotated
from fastapi import FastAPI, Security, Depends
from fastapi.middleware.cors import CORSMiddleware
from infrastructure import Base, engine
from dotenv import load_dotenv
import dtos
import service
import infrastructure
import security

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
    
def get_post_service() -> service.IPostsService:
    return service.PostsService(
        posts_repository=infrastructure.PostsRepository(
            db=infrastructure.SessionLocal()
        ))

@app.post("/posts/", response_model=dtos.CreatePostResponseDto)
async def create_post(create_post: dtos.CreatePostRequestDto, posts_service: Annotated[service.IPostsService, Depends(get_post_service)], current_user: str = Security(security.verify_jwt, scopes=["create-post"])):
    posts_service = service.PostsService()
    return await posts_service.create(create_post, current_user)

@app.get("/posts/")
async def get_post(posts_service: Annotated[service.IPostsService, Depends(get_post_service)], current_user: str = Security(security.verify_jwt, scopes=["read-post"])):
    return await posts_service.read_all()

@app.get("/posts/{post_id}")
async def get_post(post_id, posts_service: Annotated[service.IPostsService, Depends(get_post_service)], current_user: str = Security(security.verify_jwt, scopes=["read-post"])):
    return await posts_service.read(post_id)