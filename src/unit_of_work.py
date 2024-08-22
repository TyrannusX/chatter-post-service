import abc
import infrastructure


class UnitOfWork(abc.ABC):
    posts: infrastructure.ICrudRepository

    def __exit__(self, *args):
        self.rollback()
    
    @abc.abstractmethod
    def commit(self):
        pass
    
    @abc.abstractmethod
    def rollback(self):
        pass


class SqlAlchemyUnitOfWork(UnitOfWork):
    def __init__(self, session_factory=infrastructure.SessionLocal):
        self.session_factory = session_factory
    
    def __enter__(self):
        self.session = self.session_factory()
        self.posts = infrastructure.PostsRepository(self.session)
        
    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()
    
    def commit(self):
        self.session.commit()
    
    def rollback(self):
        self.session.rollback()