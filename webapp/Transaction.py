from sqlalchemy import Column, Integer, String, Boolean, DateTime, create_engine
from sshtunnel import SSHTunnelForwarder
from sqlalchemy.orm import declarative_base, sessionmaker
import serial
from configparser import ConfigParser
import datetime
import time
import threading

config = ConfigParser()
config.read('config.ini')

ssh_host = config.get('SSH', 'host')
ssh_port = config.getint('SSH', 'port')
ssh_username = config.get('SSH', 'username')
ssh_password = config.get('SSH', 'password')

mysql_host = config.get('MySQL', 'host')
mysql_port = config.getint('MySQL', 'port')
mysql_username = config.get('MySQL', 'username')
mysql_password = config.get('MySQL', 'password')

database_name = config.get('Database', 'name')

tunnel = None

def get_tunnel():
    global tunnel
    if tunnel is None or not tunnel.is_active:
        tunnel = SSHTunnelForwarder(
            (ssh_host, ssh_port),
            ssh_username=ssh_username,
            ssh_password=ssh_password,
            remote_bind_address=(mysql_host, mysql_port)
        )
        tunnel.start()
    return tunnel

Base = declarative_base()
class TransactionModel(Base):
    __tablename__ = 'transactions'

    transactions_id = Column(Integer, primary_key=True, autoincrement=True)
    iban = Column(String(16))
    amount = Column(Integer)
    date = Column(DateTime)


class Transaction:
    def __init__(self, amount: int, iban: str, language: str) -> None:
        self.amount = amount
        self.date = datetime.datetime.now()
        self.iban = iban
        self.language = language

    def print_transaction_details(self, serial_port: str) -> None:
        def print_details():
            receipt_ser = serial.Serial(serial_port, 19200, timeout=1)
            text_size_cmd = b'\x1B\x21\x08'
            header_text = (
                f'\n{"-" * 32}\n'
                f'{" " * 6}{"Banque Helvetique".center(20)}\n'
                f'{"-" * 32}\n'
                f'{"Date":<12}{self.date}\n'
                f'{"IBAN":<6}{self.iban}\n'
                f'{"Amount":<12}CHF {self.amount}\n'
                f'{"Thank you for using our ATM!":^32}\n'
                f'{"-" * 32}\n'
            )
            receipt_ser.write(text_size_cmd + header_text.encode('utf-8'))
            time.sleep(0.1)
            receipt_ser.write(b'\n')
            time.sleep(0.1)
            cut_cmd = b'\x1B\x21\x08'
            receipt_ser.write(cut_cmd)
            receipt_ser.close()
        thread = threading.Thread(target=print_details)
        thread.start()

    def record_transaction_to_db(self):
        tunnel = get_tunnel()
        engine = create_engine(
            f'mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_host}:{tunnel.local_bind_port}/{database_name}'
        )
        Session = sessionmaker(bind=engine)
        session = Session()
        try:
            transaction = TransactionModel(
                iban=self.iban,
                amount=self.amount,
                date= self.date
            )
            session.add(transaction)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
