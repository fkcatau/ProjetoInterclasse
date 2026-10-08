from flask import Flask, render_template, request, redirect, url_for, flash, g
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from banco import tabela_time
from database import *

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"


@app.route("/")
def dashboard():
    times_sql = select(Time)
    jogadores_sql = select(Jogador)
    partidas_sql = select(Partida)

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
    jogadores_sql = select(Jogador)
    jogadores = db_session.execute(jogadores_sql).scalars().all()

    # Buscando os times para caso o template precise listar ou filtrar
    times_sql = select(Time)
    times = db_session.execute(times_sql).scalars().all()

    return render_template("jogadores.html", jogadores=jogadores, times=times)


@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        numero_camisa = request.form.get("numero_camisa") or None
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id") or None

        if not nome:
            flash("Preencha o nome", "error")
            return redirect(url_for("novo_jogador"))
        if not numero_camisa:
            flash("Preencha o número", "error")
            return redirect(url_for("novo_jogador"))
        if not posicao:
            flash("Preencha a posição", "error")
            return redirect(url_for("novo_jogador"))
        if not time_id:
            flash("Selecione um time", "error")
            return redirect(url_for("novo_jogador"))

        try:
            # Tratamento seguro para converter strings do form em inteiros
            jogador = Jogador(
                nome=nome,
                numero_camisa=int(numero_camisa),
                posicao=posicao,
                time_id=int(time_id)
            )
            db_session.add(jogador)
            db_session.commit()
            flash("Jogador criado com sucesso!", "success")
            return redirect(url_for("listar_jogadores"))  # Redireciona para não reenviar o form ao dar F5

        except SQLAlchemyError as e:
            db_session.rollback()
            flash("Ocorreu um erro no banco de dados, tente novamente.", "error")
            print(f"Erro SQL: {e}")
        except Exception as e:
            db_session.rollback()
            flash("Ocorreu um erro inesperado, tente novamente.", "error")
            print(f"Erro: {e}")

    # Carregar o formulário (GET ou caso falhe o POST)
    jogadores_sql = select(Jogador)
    jogadores = db_session.execute(jogadores_sql).scalars().all()

    times_sql = select(Time)
    # CORRIGIDO: Agora executa a query correta (times_sql em vez de jogadores_sql)
    times = db_session.execute(times_sql).scalars().all()

    return render_template("jogadores.html", jogadores=jogadores, times=times)


@app.route("/times")
def listar_times():
    times_sql = select(Time)
    times = db_session.execute(times_sql).scalars().all()
    return render_template("times.html", times=times)


@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():
    # Inicializa a variável para evitar erro caso seja um acesso via GET puro
    times_sql = select(Time)
    times = db_session.execute(times_sql).scalars().all()

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        turma = request.form.get("turma", "").strip()
        responsavel = request.form.get("responsavel", "").strip()

        if not nome or not turma or not responsavel:
            flash("Preencha todos os campos obrigatórios", "error")
            return render_template("times.html", times=times)

        try:
            # Misturar SQLAlchemy puro com a sua estrutura do 'tabela_time'
            # pode dar conflito de sessão. Se o 'tabela_time' não salvar, avise.
            tabela_time.salvar(nome=nome, turma=turma, responsavel=responsavel)
            flash("Time cadastrado com sucesso!", "success")
            return redirect(url_for("listar_times"))
        except Exception as e:
            print(f"Erro ao salvar time: {e}")
            flash("Erro ao salvar o time.", "error")

    return render_template("times.html", times=times)


@app.route("/partidas")
def listar_partidas():
    partidas_sql = select(Partida)
    partidas = db_session.execute(partidas_sql).scalars().all()
    return render_template("partidas.html", partidas=partidas)


@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():
    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("placar_casa") or 0
        gols_visitante = request.form.get("placar_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()
        local = request.form.get("local", "").strip()

        # Lógica para salvar a partida viria aqui...

    times_sql = select(Time)
    times = db_session.execute(times_sql).scalars().all()
    return render_template("partidas.html", partidas=[], times=times)


if __name__ == "__main__":
    app.run(debug=True)
