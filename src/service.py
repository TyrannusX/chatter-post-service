from abc import ABC, abstractmethod
from dotenv import load_dotenv
import domain
import dtos
import infrastructure
from uuid import uuid4
from datetime import datetime, timezone

load_dotenv()

def get_posts_repository():
    return infrastructure.PostsRepository()

class IPostsService(ABC):
    @abstractmethod
    async def create(self, dto, current_user):
        pass
    
    @abstractmethod
    async def read_all(self):
        pass
    
    @abstractmethod
    async def read(self, id):
        pass


class PostsService(IPostsService):
    def __init__(self) -> None:
        super().__init__()
        self.posts_repository = get_posts_repository()
        
    async def create(self, dto: dtos.CreatePostRequestDto, current_user: str) -> dtos.CreatePostResponseDto:
        new_post_id = str(uuid4())
        
        domain_post = domain.Post(
            id=new_post_id,
            author=current_user,
            title=dto.title,
            description=dto.description,
            votes=0,
            created_at=datetime.now(timezone.utc),
            created_by=current_user,
            updated_at=datetime.now(timezone.utc),
            updated_by=current_user
        )

        await self.posts_repository.create(domain_post)
        
        return dtos.CreatePostResponseDto(id=new_post_id)
    
    async def read_all(self) -> dtos.GetPostsResponseDto:
        domain_posts = await self.posts_repository.read_all()
        return_dtos: list[dtos.GetPostResponseDto] = []
        
        for entry in domain_posts:
            return_dtos.append(dtos.GetPostResponseDto(
            id=entry.id,
            author=entry.author,
            title=entry.title,
            description=entry.description,
            votes=entry.votes,
            created_at=str(entry.created_at),
            created_by=entry.created_by,
            updated_at=str(entry.updated_at),
            updated_by=entry.updated_by
        ))
        
        return dtos.GetPostsResponseDto(
            posts=return_dtos
        )
    
    async def read(self, id: str) -> dtos.GetPostResponseDto:
        domain_post = await self.posts_repository.read(id)
        
        return dtos.GetPostResponseDto(
            id=domain_post.id,
            author=domain_post.author,
            title=domain_post.title,
            description=domain_post.description,
            votes=domain_post.votes,
            created_at=str(domain_post.created_at),
            created_by=domain_post.created_by,
            updated_at=str(domain_post.updated_at),
            updated_by=domain_post.updated_by
        )
        