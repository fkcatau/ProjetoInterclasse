from flask import Flask, render_template, request, redirect, url_for, flash
from banco import tabela_time
from banco import tabela_jogador
from banco import tabela_partida

app = Flask(__name__)
app.secret_key = "chave-secreta-interclasse-2026"

@app.route("/")
def dashboard():
    total_t = tabela_time.select_qauntidade_total()
    total_j = tabela_jogador.select_quantidade_total()
    total_p = tabela_partida.select_quantidade_total()

    return render_template(
        "dashboard.html",
        total_times=total_t,
        total_jogadores=total_j,
        total_partidas=total_p,
    )

@app.route("/jogadores")
def listar_jogadores():
    jogadores = tabela_jogador.select_todos()
    times = tabela_time.select_todos()
    return render_template("jogadores.html", jogadores=jogadores, times=times)

@app.route("/jogadores/novo", methods=["GET", "POST"])
def novo_jogador():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        numero_camisa = request.form.get("numero_camisa")
        posicao = request.form.get("posicao", "").strip()
        time_id = request.form.get("time_id")

        if not nome or not numero_camisa or not posicao or not time_id:
            flash("Preencha todos os campos obrigatórios", "error")
            return redirect(url_for("novo_jogador"))

        if tabela_jogador.salvar(nome, numero_camisa, posicao, time_id):
            return redirect(url_for("listar_jogadores"))

    jogadores = tabela_jogador.select_todos()
    times = tabela_time.select_todos()
    return render_template("jogadores.html", jogadores=jogadores, times=times)

@app.route("/times")
def listar_times():
    times = tabela_time.select_todos()
    return render_template("times.html", times=times)

@app.route("/times/novo", methods=["GET", "POST"])
def novo_time():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        turma = request.form.get("turma", "").strip()
        responsavel = request.form.get("responsavel", "").strip()

        if not nome or not turma or not responsavel:
            flash("Preencha todos os campos obrigatórios", "error")
            times = tabela_time.select_todos()
            return render_template("times.html", times=times)

        tabela_time.salvar(nome=nome, turma=turma, responsavel=responsavel)
        return redirect(url_for("listar_times"))

    times = tabela_time.select_todos()
    return render_template("times.html", times=times)

@app.route("/partidas")
def listar_partidas():
    partidas = tabela_partida.select_todos()
    times = tabela_time.select_todos()
    return render_template("partidas.html", partidas=partidas, times=times)

@app.route("/partidas/nova", methods=["GET", "POST"])
def nova_partida():
    if request.method == "POST":
        time_casa_id = request.form.get("time_casa_id")
        time_visitante_id = request.form.get("time_visitante_id")
        gols_casa = request.form.get("placar_casa") or 0
        gols_visitante = request.form.get("placar_visitante") or 0
        data_partida = request.form.get("data_partida", "").strip()
        local = request.form.get("local", "").strip()

        if not time_casa_id or not time_visitante_id or not data_partida or not local:
            flash("Preencha todos os campos obrigatórios.", "error")
            times = tabela_time.select_todos()
            partidas = tabela_partida.select_todos()
            return render_template("partidas.html", partidas=partidas, times=times)

        if time_casa_id == time_visitante_id:
            flash("Um time não pode jogar contra ele mesmo!", "error")
            times = tabela_time.select_todos()
            partidas = tabela_partida.select_todos()
            return render_template("partidas.html", partidas=partidas, times=times)

        if tabela_partida.salvar(time_casa_id, time_visitante_id, gols_casa, gols_visitante, data_partida, local):
            return redirect(url_for("listar_partidas"))

    partidas = tabela_partida.select_todos()
    times = tabela_time.select_todos()
    return render_template("partidas.html", partidas=partidas, times=times)

if __name__ == "__main__":
    app.run(debug=True)
