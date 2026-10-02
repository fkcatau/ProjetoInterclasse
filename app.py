
from flask import Flask, render_template, request, redirect, url_for, flash, g
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from banco import tabela_time
from database import *

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    # buscar todos os times do banco
    # 1 - montar o select
    times_sql = select(Time)
    jogadores_sql = select(Jogador)
    partidas_sql = select(Partida)
    # 2 - executar o select
    times = db_session.execute(times_sql).scalars().all()
    jogadores = db_session.execute(jogadores_sql).scalars().all()
    partidas = db_session.execute(partidas_sql).scalars().all()


    return render_template(
        "dashboard.html",
        total_jogadores=len(jogadores),
        total_times=len(times),
        total_partidas=len(partidas),

    )


@app.route("/jogadores")
def listar_jogadores():
    # buscar todos os times do banco
    # 1 - montar o select
    jogadores_sql = select(Jogador)
    # 2 - executar o select
    jogadores = db_session.execute(jogadores_sql).scalars().all()
    return render_template("jogadores.html", jogadores=jogadores, times=[])


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
    #Quando clicar no botão cadastrar
    if request.method == "POST":
        # 1 -pegar os valores digitados no form
        nome = request.form.get("nome",).strip()
        numero_camisa = request.form.get("numero_camisa") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None

        # 2 - Verificar se foi digitado
        if not nome:
            flash("preencha o nome", "error")
            return redirect(url_for("novo_jogador"))
        if not numero_camisa:
            flash("preencha o numero", "error")
            return redirect(url_for("novo_jogador"))
        if not posicao:
            flash("preencha a posição", "error")
            return redirect(url_for("novo_jogador"))
        #salvar no banco
        try:
            jogador = Jogador(nome=nome, numero_camisa=int(numero_camisa), posicao=posicao, time_id=int(time_id))
            db_session.add(jogador)
            db_session.commit()
            flash("jogadores criado com sucesso", "success")


        except SQLAlchemyError as e:
            db_session.rollback()
            flash("Ocorreu um erro, tente novamente", "error")
            print(f"Erro: {e}")
        except Exception as e:
            db_session.rollback()
            flash("Ocorreu um erro, tente novamente", "error")
            print(f"Erro: {e}")

    #Carregar o formulário
    # buscar todos os jogadores do banco
    # 1 - montar o select
    jogadores_sql = select(Jogador)
    # 2 - executar o select
    jogadores = db_session.execute(jogadores_sql).scalars().all()

    # buscar todos os times do banco
    # 1 - montar o select
    times_sql = select(Time)
    # 2 - executar o select
    times = db_session.execute(jogadores_sql).scalars().all()

    return render_template("jogadores.html", jogadores=jogadores, times=times)



@app.route("/times")
def listar_times():
    # buscar todos os times do banco
    # 1 - montar o select
    times_sql = select(Time)
    # 2 - executar o select
    times = db_session.execute(times_sql).scalars().all()
    return render_template("times.html", times=times)



@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():
    if request.method == "POST":
        # 1 -pegar os valores digitados no form
        nome = request.form.get("nome")
        turma = request.form.get("turma")
        responsavel = request.form.get("responsavel")

        #2 - Verificar se foi digitado
        if not nome:
            flash("preencha o nome", "error")
            return render_template("times.html")
        if not turma:
            flash("preencha o turma", "error")
            return render_template("times.html")
        if not responsavel:
            flash("preencha o resposável", "error")
            return render_template("times.html")
    #3 - Salvar no banco
        tabela_time.salvar(nome=nome, turma=turma, responsavel=responsavel)

        times = tabela_time.select_todos()
    return render_template("times.html", times=times)


@app.route("/partidas")
def listar_partidas():

    partidas_sql = select(Time)

    return render_template("partidas.html", partidas=[], times=[])


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():

    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("placar_casa") or 0
        gols_visitante = request.form.get("placar_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()
        local = request.form.get("local", "").strip()

    return render_template("partidas.html", partidas=[], times=[])


if __name__ == "__main__":
    app.run(debug=True)
