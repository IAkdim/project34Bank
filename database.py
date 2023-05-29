from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, LargeBinary
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import bcrypt

db_url = 'mysql+mysqlconnector://root:@localhost/Bank'
engine = create_engine(db_url)
Base = declarative_base()

# Create session
Session = sessionmaker(bind=engine)
session = Session()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    pin_hash = Column(LargeBinary(60))
    accounts = relationship("Account", back_populates="user")

    def verify_pin(self, pin):
        return bcrypt.checkpw(pin.encode('utf-8'), self.pin_hash)

class Account(Base):
    __tablename__ = 'accounts'

    account_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    iban = Column(String(16))
    balance = Column(Integer)
    status = Column(Integer)
    attempts = Column(Integer)
    user = relationship("User", back_populates="accounts")
