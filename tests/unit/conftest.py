import pytest
from krakenbot.database.connectors.sqlite import SQLiteConnector
from pathlib import Path
import os


@pytest.fixture
def sqlite_connector():
    file_path = os.path.realpath(__file__)
    db_path = Path(file_path).parent.parent / Path('data/test.db')
    return SQLiteConnector(db_name=str(db_path))
