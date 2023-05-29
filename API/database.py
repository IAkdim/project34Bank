from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
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

    user_id: int = Column(Integer, primary_key=True)
    pin_hash: str = Column(String(60))
    accounts = relationship("Account", back_populates="user")

    def verify_pin(self, pin: str):
        return bcrypt.checkpw(pin.encode('utf-8'), self.pin_hash.encode('utf-8'))

class Account(Base):
    __tablename__ = 'accounts'

    account_id: int = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey('users.user_id'))
    iban: str = Column(String(16))
    balance: int = Column(Integer)
    status: int = Column(Integer)
    attempts: int = Column(Integer)
    user = relationship("User", back_populates="accounts")

    def increment_attempts(self):
        self.attempts += 1
        if self.attempts >= 3:
            self.status = 1
        session.commit()

    def reset_attempts(self):
        self.attempts = 0
        session.commit()