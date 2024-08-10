import datetime
import unittest.mock
import sqlalchemy
from sqlalchemy.orm import sessionmaker
import unittest

import sqlalchemy.orm
import infrastructure
import unittest.async_case
import domain


class PostsRepositoryTests(unittest.async_case.IsolatedAsyncioTestCase):
    async def test_create_throws_when_model_is_none(self):
        #arrange
        session = sessionmaker()
        session_instance = session()
        session_instance.add = unittest.mock.MagicMock()
        session_instance.commit = unittest.mock.MagicMock()
        posts_repository = infrastructure.PostsRepository(db=session_instance)
        
        #act
        with self.assertRaises(AssertionError):
            #assert
            await posts_repository.create(None)
    
    async def test_create_successful(self):
        #arrange
        session = sessionmaker()
        session_instance = session()
        session_instance.add = unittest.mock.MagicMock()
        session_instance.commit = unittest.mock.MagicMock()
        posts_repository = infrastructure.PostsRepository(db=session_instance)
        
        #act
        await posts_repository.create(domain.Post(
            id="id",
            author="user",
            title="title",
            description="desc",
            votes=1,
            created_at=datetime.datetime(year=2024,month=1,day=1),
            updated_at=datetime.datetime(year=2024,month=1,day=1),
            updated_by="user",
            created_by="user"
        ))
        
        #assert
        session_instance.add.assert_called_once() 
        session_instance.add.call_args[0][0].id == "id"
        session_instance.commit.assert_called_once()
    
    async def test_read_all_successful(self):
        #arrange
        session = sessionmaker()
        session_instance = session()
        session_instance.query = unittest.mock.MagicMock()
        session_instance.query.return_value = [
            infrastructure.PersistedPost(
                id="id",
                author="user",
                title="title",
                description="desc",
                votes=1,
                created_at=datetime.datetime(year=2024,month=1,day=1),
                updated_at=datetime.datetime(year=2024,month=1,day=1),
                updated_by="user",
                created_by="user"
            )
        ]
        posts_repository = infrastructure.PostsRepository(db=session_instance)
        
        #act
        result: list[domain.Post] = await posts_repository.read_all()
        
        #assert
        self.assertEqual(result, [
            domain.Post(
                id="id",
                author="user",
                title="title",
                description="desc",
                votes=1,
                created_at=datetime.datetime(year=2024,month=1,day=1),
                updated_at=datetime.datetime(year=2024,month=1,day=1),
                updated_by="user",
                created_by="user"
            )
        ])
        session_instance.query.assert_called_once()
    
    async def test_read_throws_when_id_is_none(self):
        #arrange
        session = sessionmaker()
        session_instance = session()
        posts_repository = infrastructure.PostsRepository(db=session_instance)
        
        #act
        with self.assertRaises(AssertionError):
            #assert
            await posts_repository.read(None)
    
    async def test_read_throws_when_id_is_whitespace(self):
        #arrange
        session = sessionmaker()
        session_instance = session()
        posts_repository = infrastructure.PostsRepository(db=session_instance)
        
        #act
        with self.assertRaises(AssertionError):
            #assert
            await posts_repository.read(" ")
    
    async def test_read_successful(self):
        #arrange
        session = sessionmaker()
        session_instance = session()
        session_instance.query = unittest.mock.MagicMock()
        session_instance.query.return_value.filter.return_value.first.return_value = infrastructure.PersistedPost(
            id="id",
            author="user",
            title="title",
            description="desc",
            votes=1,
            created_at=datetime.datetime(year=2024,month=1,day=1),
            updated_at=datetime.datetime(year=2024,month=1,day=1),
            updated_by="user",
            created_by="user"
        )
        
        posts_repository = infrastructure.PostsRepository(db=session_instance)
        
        #act
        result: domain.Post = await posts_repository.read(id="id")
        
        #assert
        self.assertEqual(result, domain.Post(
            id="id",
            author="user",
            title="title",
            description="desc",
            votes=1,
            created_at=datetime.datetime(year=2024,month=1,day=1),
            updated_at=datetime.datetime(year=2024,month=1,day=1),
            updated_by="user",
            created_by="user"
        ))
        session_instance.query.assert_called_once()