import sqlite3
from typing import Any, Optional, Sequence

DATABASE_EXTENSIONS = ["sqlite", "sqlite3", "db", "db3", "s3db", "sl3"]


class SQLiteConnector:
    def __init__(self, db_name: str) -> None:
        self._db_valid_extensions = DATABASE_EXTENSIONS
        self.db_name = self._validate_db_name(db_name=db_name)
        self.connection = sqlite3.connect(db_name)
        self.connected = True

    def _validate_db_name(self, db_name: str) -> str:
        if not db_name:
            raise ValueError("Please input your database name.")
        db_name = db_name.split("/")[-1]
        if db_name.split(".")[1].lower() not in self._db_valid_extensions:
            raise ValueError("Your database extension is incorrect.")
        return db_name

    def close(self) -> None:
        """Close databse connection and set connected flag to False."""
        if self.connected:
            self.connection.close()
            self.connected = False

    def execute(self, query: str, data: Sequence[Any] = [], autoclose: bool = True) -> Optional[Sequence[Any]]:
        """Execute SQL query for the connected database.

        Args:
            query (str): SQL query to be executed for the given database.
            data (Sequence[Any], optional): Data for the query (e.g. inserted values). Defaults to [].
            autoclose (bool, optional): Autoclose database connection. Defaults to True.

        Returns:
            Optional[Sequence[Any]]: the SQL query result
        """
        if not self.connected:
            self.connection = sqlite3.connect(self.db_name)
            self.connected = True
        cursor = self.connection.cursor()
        if data:
            cursor.executemany(query, data)
        else:
            cursor.execute(
                query,
            )
        records = cursor.fetchall()
        self.connection.commit()
        if autoclose:
            self.connection.close()
            self.connected = False
        if records:
            return records
        return None
