from flask import flash
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from database import Time, db_session


def select_todos():
    # 1 - montar o select
    times_sql = select(Time)
    # 2 - executar o select
    times = db_session.execute(times_sql).scalars().all()

    return times

def salvar(nome, turma, responsavel):
    try:
        time_novo = Time(nome=nome, turma=turma, responsavel=responsavel)
        db_session.add(time_novo)
        db_session.commit()
        flash("times criados com sucesso", "success")
    except SQLAlchemyError as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"Erro: {e}")
    except Exception as e:
        db_session.rollback()
        flash("Ocorreu um erro, tente novamente", "error")
        print(f"Erro: {e}")