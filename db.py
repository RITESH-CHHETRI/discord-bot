import mysql.connector
import os
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String


host=os.getenv('Mhost')
port=os.getenv('Mport')
user=os.getenv('Muser')
pwd=os.getenv('Mpass')
dbs=os.getenv('Mdb')

connection_uri=f"mysql://{user}:{pwd}@{host}:{port}/{dbs}")
engine = create_engine(connection_uri,echo=False)
meta=MetaData()

conn=engine.connect()

users = Table('users', meta, Column('id', Integer, primary_key=True),Column('name', String),)