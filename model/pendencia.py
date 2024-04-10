from sqlalchemy import Column, String, DateTime, Uuid
from datetime import datetime
from typing import Union

import uuid

from  model import Base

class Pendencia(Base):
    __tablename__ = 'Pendencia'

    id = Column("pk_pendencia", Uuid, primary_key=True, default=uuid.uuid4)
    autor = Column(String(140))
    titulo = Column(String(140), unique=True)
    equipamento = Column(String(140))
    descricao = Column(String(280))
    status = Column(String(140))
    data_insercao = Column(DateTime, default=datetime.now())


    def __init__(self, autor:str, titulo:str, equipamento:str, descricao:str, status:str,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um pendencia

        Arguments:
            autor: autor do pendencia.
            titulo: titulo da pendência
            equipamento: mostra qual o equipamento a pendencia está se referindo
            descricao: descricao esperado para a pendencia
            status: status que a pendência se encontra
            data_insercao: data de quando o pendencia foi inserido à base
        """
        print("dentro da model da pendencia")

        self.autor = autor
        self.titulo = titulo
        self.equipamento = equipamento
        self.descricao = descricao
        self.status = status

        # se não for informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao


