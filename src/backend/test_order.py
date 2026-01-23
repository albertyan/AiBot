from sqlalchemy import Column, Integer, String, create_mock_engine
from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy.schema import CreateTable

class Base(DeclarativeBase):
    pass

class BaseMixin:
    id = Column(Integer, primary_key=True)
    extra = Column(String)

class User(BaseMixin, Base):
    __tablename__ = 'user'
    name = Column(String)

def dump(sql, *multiparams, **params):
    print(sql.compile(dialect=engine.dialect))

engine = create_mock_engine("sqlite://", dump)

print("--- Default Mixin Order ---")
# Compile User table
print(CreateTable(User.__table__).compile(engine))

class UserExplicit(BaseMixin, Base):
    __tablename__ = 'user_explicit'
    id = Column(Integer, primary_key=True)
    name = Column(String)

print("\n--- Explicit Definition Order ---")
print(CreateTable(UserExplicit.__table__).compile(engine))
