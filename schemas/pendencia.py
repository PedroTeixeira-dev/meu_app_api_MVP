from pydantic import BaseModel
from typing import  List
from model.pendencia import Pendencia

class PendenciaSchema(BaseModel):
    """ Define como uma nova pendeência deve ser apresentada
    """
    autor: str = "Pedro Teixeira"
    titulo: str = "Vazamento de óleo do equipamento 1"
    equipamento: str = "Equipamento 1"
    descricao: str = "Vazamento de óleo na junta da gaxeta do equipamento 1"
    status: str = "Em aberto"


class PendenciaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da pendencia.
    """
    nome: str = "Teste"


class ListagemPendenciasSchema(BaseModel):
    """ Define como uma listagem de pendencias será retornada.
    """
    pendencias:List[PendenciaSchema]


def apresenta_pendencias(pendencias: List[Pendencia]):
    """ Retorna uma representação da pendencia seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for pendencia in pendencias:
        result.append({
            "autor": pendencia.autor,
            "titulo": pendencia.titulo,
            "equipamento": pendencia.equipamento,
            "descricao": pendencia.descricao,
            "status": pendencia.status
        })

    return {"pendencias": result}


class PendenciaViewSchema(BaseModel):
    """ Define como uma pendência será retornada.
    """
    id: int = 1
    autor: str = "Pedro Teixeira"
    titulo: str = "Vazamento de óleo no equipamento 1"
    equipamento: str = "Equipamento 1"
    status: str = "Em aberto"

class PendenciaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    titulo: str

def apresenta_pendencia(pendencia: Pendencia):
    """ Retorna uma representação da pendencia seguindo o schema definido em
        PendenciaViewSchema.
    """
    return {
        "id": pendencia.id,
        "autor": pendencia.autor,
        "titulo": pendencia.titulo,
        "equipamento": pendencia.equipamento,
        "descricao": pendencia.descricao,
        "status" : pendencia.status
    }
