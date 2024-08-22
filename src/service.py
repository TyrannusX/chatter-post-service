from abc import ABC, abstractmethod
from dotenv import load_dotenv
import domain
import dtos
from uuid import uuid4
from datetime import datetime, timezone
import logging
import unit_of_work

load_dotenv()

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
    def __init__(self, uow: unit_of_work.UnitOfWork) -> None:
        super().__init__()
        self.uow = uow
        
    async def create(self, dto: dtos.CreatePostRequestDto, current_user: str) -> dtos.CreatePostResponseDto:
        assert dto is not None
        assert current_user is not None and not current_user.isspace()
        
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

        with self.uow:    
            await self.uow.posts.create(domain_post)
            self.uow.commit()

        return dtos.CreatePostResponseDto(id=new_post_id)
    
    async def read_all(self) -> dtos.GetPostsResponseDto:
        with self.uow:
            domain_posts = await self.uow.posts.read_all()
            
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
        assert id is not None and not id.isspace()
        
        with self.uow:
            domain_post = await self.uow.posts.read(id)
        
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
        