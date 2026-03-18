from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# conexão com banco
def conectar():
    return sqlite3.connect("database.db")

# cria tabela
def criar_tabela():
    con = conectar()
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        telefone TEXT NOT NULL
    )
    """)
    con.commit()
    con.close()

# tela inicial (cadastro)
@app.route('/')
def index():
    return render_template('index.html', pagina="cadastro")

# cadastrar cliente
@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')

    if not nome or not email or not telefone:
        return redirect('/')

    con = conectar()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
        (nome, email, telefone)
    )
    con.commit()
    con.close()

    return redirect('/clientes')

# ver clientes
@app.route('/clientes')
def clientes():
    con = conectar()
    cur = con.cursor()
    cur.execute("SELECT * FROM clientes")
    dados = cur.fetchall()
    con.close()

    return render_template('index.html', pagina="clientes", clientes=dados)

# iniciar app
if __name__ == '__main__':
    criar_tabela()
    app.run(debug=True)