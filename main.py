from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
database_url = 'mysql+pymysql://root:Senac2021@localhost:3306/locadora'

class Filme(Base):
    __tablename__ = 'filme'

    id = Column(Integer, autoincrement=True, primary_key=True)
    titulo = Column(String(100), nullable=False)
    genero = Column(String(100), nullable=False)
    ano = Column(Integer, nullable=False)

    def __repr__(self):
        return f'Filme [Título = {self.titulo}, Genero = {self.genero}, Ano = {self.ano}]'

def create_database():
    engine = create_engine(database_url, echo=True)
    try:
        engine.connect()
    except Exception as e:
        if'1049' in str(e):
            engine = create_engine(database_url.rsplit('/', 1)[0], echo=True)
            conn = engine.connect()
            conn.execute('CREATE DATABASE locadora')
            conn.close()
            print('Banco locadora criado com sucesso')
        else:
            raise e

create_database()

#Configurações
engine = create_engine(database_url, echo=True)
conn = engine.connect()
Session = sessionmaker(bind=engine)
session = Session()

def create_table():
    Base.metadata.create_all(engine)
    print('Tabela filme criada com sucesso!')
create_table()

#Inserção no banco
data_insert = Filme(titulo = 'Lago Azul', ano = '1970', genero = 'aventura')
session.add(data_insert)
session.commit()


#Remoção do banco
session.query(Filme).filter(Filme.titulo == 'Lago Azul').delete()
session.commit()

#Atualização de dados
session.query(Filme).filter(Filme.genero == 'ação').update({'titulo' : 'Batimam'})
session.commit()

#Consulta de dados
data = session.query(Filme).all()
print(data)

session.close()


