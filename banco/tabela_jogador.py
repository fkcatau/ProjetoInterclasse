from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from database import Jogador, db_session

def select_todos():
    jogadores_sql = select(Jogador)
    jogadores = db_session.execute(jogadores_sql).scalars().all()
    return jogadores

def select_quantidade_total():
    jogadores_sql = select(func.count(Jogador.id))
    qtd_total = db_session.execute(jogadores_sql).scalar()
    return qtd_total

def salvar(nome, numero_camisa, posicao, time_id):
    try:
        jogador_novo = Jogador(
            nome=nome,
            numero_camisa=int(numero_camisa),
            posicao=posicao,
            time_id=int(time_id)
        )
        db_session.add(jogador_novo)
        db_session.commit()
        flash("Jogador criado com sucesso", "success")
        return True
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Ocorreu um erro no banco de dados, tente novamente", "error")
        print(f"Erro: {e}")
        return False
    except Exception as e:
        db_session.rollback()
        flash("Ocorreu um erro inesperado, tente novamente", "error")
        print(f"Erro: {e}")
        return False
