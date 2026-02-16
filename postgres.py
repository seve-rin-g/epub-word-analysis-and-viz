from sqlalchemy import create_engine, text
from faker import Faker
import time, logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

def get_db_engine():
    # create engine for connecting to PostgreSQL
    return create_engine('postgresql://{}:{}@{}/{}'.format('postgres', 'postgrespw', 'postgres:5432','ol_bookdb'))

while True:
    try:
        db_engine = get_db_engine().connect()
        if db_engine:   
            print("Database connection successful!")
            break
    except Exception as e:
        LOGGER.warning(f"Database connection failed {str(e)}.")
        time.sleep(5)  # wait for 5 seconds before retrying

faker = Faker('en_US')

for i in range(10):
    # insert fake data into the database
    query = f"INSERT INTO ol_bookdb.book (title, author) VALUES ('{faker.sentence()}', '{faker.name()}')"
    db_engine.execute(text(query))
    LOGGER.info(f"record {i} inserted: {query}")

db_engine.commit() # commit the transaction
db_engine.close()