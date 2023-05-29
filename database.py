from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import bcrypt

db_url = 'mysql+mysqlconnector://root:@localhost/Bank'
engine = create_engine(db_url)
Base = declarative_base()

# Create session
Session = sessionmaker(bind=engine)
session = Session()


class Account(Base):
    __tablename__ = 'accounts'

    account_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    iban = Column(String(16))
    balance = Column(Integer)
    status = Column(Integer)
    attempts = Column(Integer)


class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    pin_hash = Column(String(255))

    def verify_pin(self, pin):
        account = session.query(Account).filter_by(user_id=self.user_id).first()
        user = session.query(User).filter_by(user_id=account.user_id).first()
        return bcrypt.checkpw(pin.encode('utf-8'), user.pin_hash.encode('utf-8'))
