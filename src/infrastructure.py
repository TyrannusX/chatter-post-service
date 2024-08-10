from sqlalchemy import create_engine, String, Integer, DateTime, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from sqlalchemy.sql import func
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv
import domain

load_dotenv()

# The SQL Alchemy engine (required for initialization)
engine = create_engine(os.getenv("SQLALCHEMY_DATABASE_URL"), connect_args={"check_same_thread": False})

# Builds the SQL Alchemy session class (used to create sessions)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQL Alchemy models
Base = declarative_base()


# ORM Models
class PersistedPost(Base):
    __tablename__ = "Posts"
    
    id = Column(String, primary_key=True)
    author = Column(String)
    title = Column(String)
    description = Column(String)
    votes = Column(Integer)
    created_at = Column(DateTime)
    created_by = Column(String)
    updated_at = Column(DateTime)
    updated_by = Column(String)

# Repos
class ICrudRepository(ABC):
    @abstractmethod
    async def create(self, model):
        pass
    
    @abstractmethod
    async def read_all(self):
        pass
    
    @abstractmethod
    async def read(self, id):
        pass
    
    @abstractmethod
    async def update(self, model):
        pass
    
    @abstractmethod
    async def delete(self, id):
        pass


class PostsRepository(ICrudRepository):
    def __init__(self, db) -> None:
        super().__init__()
        self.db = db
        
    async def create(self, model) -> None:
        assert model is not None
        
        db_post = PersistedPost(
            id=model.id,
            author=model.author,
            title=model.title,
            description=model.description,
            votes=model.votes,
            created_at=model.created_at,
            updated_at=model.updated_at,
            created_by=model.created_by,
            updated_by=model.updated_by,
        )
        
        self.db.add(db_post)
        self.db.commit()
        
    async def read_all(self) -> list[domain.Post]:
        db_posts = self.db.query(PersistedPost)
        domain_posts: list[domain.Post] = []
        
        for entry in db_posts:
            domain_posts.append(domain.Post(
            id=entry.id,
            author=entry.author,
            title=entry.title,
            description=entry.description,
            votes=entry.votes,
            created_at=entry.created_at,
            created_by=entry.created_by,
            updated_at=entry.updated_at,
            updated_by=entry.updated_by
        ))
        
        return domain_posts
    
    async def read(self, id: str) -> domain.Post:
        assert id is not None and not id.isspace()
        
        db_post = self.db.query(PersistedPost).filter(PersistedPost.id == id).first()
        
        domain_post = domain.Post(
            id=db_post.id,
            author=db_post.author,
            title=db_post.title,
            description=db_post.description,
            votes=db_post.votes,
            created_at=db_post.created_at,
            created_by=db_post.created_by,
            updated_at=db_post.updated_at,
            updated_by=db_post.updated_by
        )
        
        return domain_post
    
    async def update(self, model):
        pass
    
    async def delete(self, id):
        pass