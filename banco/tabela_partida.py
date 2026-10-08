from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from database import Partida, db_session

def select_todos():
    partidas_sql = select(Partida)
    partidas = db_session.execute(partidas_sql).scalars().all()
    return partidas

def select_quantidade_total():
    partidas_sql = select(func.count(Partida.id))
    qtd_total = db_session.execute(partidas_sql).scalar()
    return qtd_total

def salvar(time_casa_id, time_visitante_id, gols_casa, gols_visitante, data_partida, local):
    try:
        partida_nova = Partida(
            time_casa_id=int(time_casa_id),
            time_visitante_id=int(time_visitante_id),
            gols_casa=int(gols_casa),
            gols_visitante=int(gols_visitante),
            data_partida=data_partida,
            local=local
        )
        db_session.add(partida_nova)
        db_session.commit()
        flash("Partida cadastrada com sucesso", "success")
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
