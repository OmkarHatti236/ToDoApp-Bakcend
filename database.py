from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DATABASE_URL='sqlite:///./todoapp.db'
DATABASE_URL='postgresql://postgres:OmkarHatti@localhost:5432/todoapplication'
# DATABASE_URL='mysql+pymysql://root:OmkarHatti@127.0.0.1:3306/todoapplication'

engine=create_engine(DATABASE_URL)
sessionLocal=sessionmaker(autoflush=False,autocommit=False,bind=engine)