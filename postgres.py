from sqlalchemy import create_engine, text
from faker import Faker

def get_db_engine():
    # create engine for connecting to PostgreSQL
    engine = create_engine('postgresql://{}:{}@{}/{}'.format('postgres', 'postgres', 'localhost:5432','ol_bookdb'))

while True:
    try:
        db_engine = get_db_engine().connect()
        if db_engine:   
            print("Database connection successful!")
            break
    except Exception as e:
        print(f"Database connection failed {str(e)}.")

faker = Faker('en_US')

for i in range(10):
    print(f"inserting record {i}")
    # insert fake data into the database
    db_engine.execute("INSERT INTO book (title, author, publication_date) VALUES (%s, %s, %s)", (faker.sentence(), faker.name(), faker.date())).execution_options(autocommit=True))
    print (f"record {i} inserted")
    
db_engine.close()