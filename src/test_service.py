import unittest
import unittest.async_case
import unittest.mock
import infrastructure
import service
import dtos
import domain
import datetime

class PostsServiceTests(unittest.async_case.IsolatedAsyncioTestCase):
    async def test_create_throws_when_dto_is_none(self):
        #arrange
        posts_repository = infrastructure.PostsRepository(db=None)
        posts_service = service.PostsService(posts_repository=posts_repository)
        
        #act
        with self.assertRaises(AssertionError):
            #assert
            await posts_service.create(None, "user")
    
    async def test_create_throws_when_user_is_none(self):
        #arrange
        posts_repository = infrastructure.PostsRepository(db=None)
        posts_service = service.PostsService(posts_repository=posts_repository)
        
        #act
        with self.assertRaises(AssertionError):
            #assert
            await posts_service.create(dtos.CreatePostRequestDto(title="title", description="desc"), None)
    
    async def test_create_throws_when_user_is_empty(self):
        #arrange
        posts_repository = infrastructure.PostsRepository(db=None)
        posts_service = service.PostsService(posts_repository=posts_repository)
        
        #act
        with self.assertRaises(AssertionError):
            #assert
            await posts_service.create(dtos.CreatePostRequestDto(title="title", description="desc"), " ")
    
    async def test_create_successful(self):
        #arrange
        posts_repository = infrastructure.PostsRepository(db=None)
        posts_repository.create = unittest.mock.AsyncMock()
        posts_service = service.PostsService(posts_repository=posts_repository)
        
        #act
        await posts_service.create(dtos.CreatePostRequestDto(title="title", description="desc"), "user")
        
        #assert
        posts_repository.create.assert_called_once()
    
    async def test_read_all_successful(self):
        #arrange
        posts_repository = infrastructure.PostsRepository(db=None)
        posts_repository.read_all = unittest.mock.AsyncMock()
        posts_repository.read_all.return_value = [
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
        ]
        posts_service = service.PostsService(posts_repository=posts_repository)
        
        #act
        result: dtos.GetPostsResponseDto = await posts_service.read_all()
        
        #assert
        self.assertEqual(result, dtos.GetPostsResponseDto(posts=[
            dtos.GetPostResponseDto(
                id="id",
                author="user",
                title="title",
                description="desc",
                votes=1,
                created_at="2024-01-01 00:00:00",
                updated_at="2024-01-01 00:00:00",
                updated_by="user",
                created_by="user"
            )
        ]))
        posts_repository.read_all.assert_called_once()
    
    async def test_read_throws_when_id_is_none(self):
        #arrange
        posts_repository = infrastructure.PostsRepository(db=None)
        posts_service = service.PostsService(posts_repository=posts_repository)
        
        #act
        with self.assertRaises(AssertionError):
            #assert
            await posts_service.read(None)
    
    async def test_read_throws_when_id_is_whitespace(self):
        #arrange
        posts_repository = infrastructure.PostsRepository(db=None)
        posts_service = service.PostsService(posts_repository=posts_repository)
        
        #act
        with self.assertRaises(AssertionError):
            #assert
            await posts_service.read(" ")
        
    async def test_read_successful(self):
        #arrange
        posts_repository = infrastructure.PostsRepository(db=None)
        posts_repository.read = unittest.mock.AsyncMock()
        posts_repository.read.return_value = domain.Post(
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
        posts_service = service.PostsService(posts_repository=posts_repository)
        
        #act
        result: dtos.GetPostResponseDto = await posts_service.read("id")
        
        #assert
        self.assertEqual(result, dtos.GetPostResponseDto(
            id="id",
            author="user",
            title="title",
            description="desc",
            votes=1,
            created_at="2024-01-01 00:00:00",
            updated_at="2024-01-01 00:00:00",
            updated_by="user",
            created_by="user"
        ))
        posts_repository.read.assert_awaited_once_with("id")