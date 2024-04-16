from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Pendencia
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
pendencia_tag = Tag(name="Pendencia", description="Adição, visualização, edição e remoção de pendencias à base")

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')

@app.post('/pendencia', tags=[pendencia_tag],
          responses={"200": PendenciaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_pendencia(form: PendenciaSchema):
    """Adiciona uma nova Pendencia à base de dados

    Retorna uma representação das pendencias.
    """
    pendencia = Pendencia(
        autor=form.autor,
        titulo=form.titulo,
        equipamento=form.equipamento,
        descricao=form.descricao,
        status=form.status
        )
    logger.debug(f"Adicionando pendencia de nome: '{pendencia.titulo}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando pendencia
        session.add(pendencia)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado pendencia de nome: '{pendencia.titulo}'")
        return apresenta_pendencia(pendencia), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Pendencia de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar produto '{pendencia.titulo}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar pendencia '{pendencia.titulo}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/pendencias', tags=[pendencia_tag],
         responses={"200": ListagemPendenciasSchema, "404": ErrorSchema})
def get_pendencias():
    """Faz a busca por todos as pendencias cadastradas

    Retorna uma representação da listagem de pendencias.
    """
    logger.debug(f"Coletando pendencias ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pendencias = session.query(Pendencia).all()

    if not pendencias:
        # se não há pendencias cadastrados
        return {"pendencias": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(pendencias))
        # retorna a representação de produto
        return apresenta_pendencias(pendencias), 200


@app.get('/pendencias', tags=[pendencia_tag],
         responses={"200": PendenciaViewSchema, "404": ErrorSchema})
def get_produto(query: PendenciaBuscaSchema):
    """Faz a busca por uma pendencia a partir do id da pendencia

    Retorna uma representação das pendencias.
    """
    pendencia_id = query.id
    logger.debug(f"Coletando dados sobre produto #{pendencia_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pendencia = session.query(Pendencia).filter(Pendencia.id == pendencia_id).first()

    if not pendencia:
        # se o pendencia não foi encontrado
        error_msg = "pendencia não encontrado na base :/"
        logger.warning(f"Erro ao buscar pendencia '{pendencia_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"pendencia econtrado: '{pendencia.titulo}'")
        # retorna a representação de pendencia
        return apresenta_pendencia(pendencia), 200


@app.delete('/pendencia', tags=[pendencia_tag],
            responses={"200": PendenciaDelSchema, "404": ErrorSchema})
def del_produto(query: PendenciaBuscaSchema):
    """Deleta uma pendencia a partir do titulo da pendencia informado

    Retorna uma mensagem de confirmação da remoção.
    """
    pendencia_titulo = unquote(unquote(query.nome))
    logger.debug(f"Deletando dados sobre produto #{pendencia_titulo}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Pendencia).filter(Pendencia.titulo == pendencia_titulo).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado pendencia #{pendencia_titulo}")
        return {"mesage": "Pendencia removida", "id": pendencia_titulo}
    else:
        # se a pendencia não foi encontrado
        error_msg = "pendencia não encontrado na base :/"
        logger.warning(f"Erro ao deletar pendenica #'{pendencia_titulo}', {error_msg}")
        return {"mesage": error_msg}, 404
    
@app.put('/pendencia', tags=[pendencia_tag],
         responses={"200": PendenciaViewSchema, "404": ErrorSchema})
def update_status(query: PendenciaAtualizaSchema):
    """Atualiza o status de uma pendencia existente pelo nome.

    Retorna uma representação da pendencia atualizada.
    """
    pendencia_titulo = query.nome
    pendencia_status = query.status
    logger.debug(f"Atualizando status da pendencia '{pendencia_titulo}'")

    # criando conexão com a base
    session = Session()
    # fazendo a busca pela pendencia pelo nome
    pendencia = session.query(Pendencia).filter(Pendencia.titulo == pendencia_titulo).first()

    if not pendencia:
        # se a pendencia não foi encontrada
        error_msg = "Pendencia não encontrada na base :/"
        logger.warning(f"Erro ao atualizar status da pendencia '{pendencia_titulo}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        # atualiza o status da pendencia
        pendencia.status = pendencia_status
        session.commit()

        logger.debug(f"Status da pendencia '{pendencia_titulo}' atualizado para '{pendencia.status}'")
        # retorna a representação da pendencia atualizada
        return apresenta_pendencia(pendencia), 200


