
import sqlite3
from typing import Any
from sqlite3 import connect

DATABASE_EXTENSIONS = ['.sqlite', '.sqlite3', '.db', '.db3', '.s3db', '.sl3']

class DatabaseConnector:

    def __init__(self, db_name: str)-> None:
        self._db_valid_extensions = DATABASE_EXTENSIONS
        self.db_name = self._validate_db_name(db_name=db_name)

    def _validate_db_name(self, db_name: str) -> str:
        if not db_name:
            raise ValueError('Please input your database name')
        if db_name.split('.')[1] not in self._db_valid_extensions:
            raise ValueError('Your database extension is incorrect')
        return db_name

    def execute(self, data: Any) -> None:
        connection = sqlite3.connect(self.db_name)
        pass
