from fastapi import FastAPI, Security
from fastapi.middleware.cors import CORSMiddleware
from infrastructure import Base, engine
from dotenv import load_dotenv
import dtos
import service
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

@app.post("/posts/", response_model=dtos.CreatePostResponseDto)
async def create_post(create_post: dtos.CreatePostRequestDto, current_user: str = Security(security.verify_jwt, scopes=["create-post"])):
    posts_service = service.PostsService()
    return await posts_service.create(create_post, current_user)

@app.get("/posts/")
async def get_post(current_user: str = Security(security.verify_jwt, scopes=["read-post"])):
    posts_service = service.PostsService()
    return await posts_service.read_all()

@app.get("/posts/{post_id}")
async def get_post(post_id, current_user: str = Security(security.verify_jwt, scopes=["read-post"])):
    posts_service = service.PostsService()
    return await posts_service.read(post_id)