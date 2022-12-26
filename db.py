from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session


DATABASE_URL = f"mysql://root:mysql@localhost:3306/mysql"
engine = create_engine(DATABASE_URL, encoding="utf8")
Base = declarative_base()
session = Session(bind=engine)
session.execute("ALTER TABLE olx_orders CONVERT TO CHARACTER SET utf8")
session.execute("ALTER TABLE kolesa_orders CONVERT TO CHARACTER SET utf8")

session.commit()
