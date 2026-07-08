from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base


DATABASE_URL = "mysql+pymysql://root:password2007@localhost:3306/manager"
                                                 
# CONNECT WITH DESIED DATABASE                                                
engine=create_engine(DATABASE_URL)

#create sessions for database during commits
sessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)


#USED IN ORM
Base=declarative_base()


#create tunnel to database
def get_db():
    db=sessionLocal();
    try:
        yield db
    finally:
        db.close()