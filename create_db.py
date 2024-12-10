from models import Base
from db_set import engine

Base.metadata.create_all(engine)
