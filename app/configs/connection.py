import os

from sqlalchemy.orm import sessionmaker

from sqlalchemy import create_engine


class DbConnectionHandler:
    def __init__(self) -> None:
        sqlpw = os.environ.get("sqlpw")
        self.__connection_string = \
            f'mysql+pymysql://root:{sqlpw}@localhost:3306/test_bank'
        self.__engine = self.__create_database_engine()
        self.session = None

    def __create_database_engine(self):
        return create_engine(self.__connection_string)

    def get_engine(self):
        return self.__engine
    
    def get_connection_string(self):
        return self.__connection_string
    
    def __enter__(self):
        session_make = sessionmaker(bind=self.get_engine())
        self.session = session_make()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
