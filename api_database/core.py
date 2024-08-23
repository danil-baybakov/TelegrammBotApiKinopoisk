from api_database.utils.crud import InterfaceApiDatabase, ParamsStorage, History
from api_database.common.model import create_tables

create_tables()
api_db = InterfaceApiDatabase()

if __name__ == "__main__":
    ...
