from flask import flash
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from database import Time, db_session

def select_todos():
    times_sql = select(Time)
    times = db_session.execute(times_sql).scalars().all()
    return times

def select_qauntidade_total():
    times_sql = select(func.count(Time.id))
    qtd_total = db_session.execute(times_sql).scalar()
    return qtd_total

def salvar(nome, turma, responsavel):
    try:
        time_novo = Time(nome=nome, turma=turma, responsavel=responsavel)
        db_session.add(time_novo)
        db_session.commit()
        flash("Time cadastrado com sucesso!", "success")
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
