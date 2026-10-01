from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS
import time

app = Flask(__name__)

CORS(app)

def conectar_banco():

    while True:

        try:
            banco = mysql.connector.connect(
                host="mysql",
                user="root",
                password="191421",
                database="usuarios"
            )

            return banco

        except mysql.connector.Error as erro:

            time.sleep(3)

banco = conectar_banco()

cursor = banco.cursor()

@app.post("/usuarios")
def cadastrar():

    dados = request.json

    nome = dados["nome"]
    email = dados["email"]
    senha = dados["senha"]

    sql = """
        INSERT INTO usuarios (nome, email, senha)
        VALUES (%s, %s, %s)
"""

    valores = (nome, email, senha)

    cursor.execute(sql, valores)

    banco.commit()

    return jsonify ({
        "mensagem": "usuario cadastrado com sucesso."
    }), 201

@app.post("/login")
def logar():

    dados = request.json

    nome = dados["nome"]
    email = dados["email"]
    senha = dados["senha"]

    sql = """
            SELECT id, nome, email, senha
            FROM usuarios
            WHERE email = %s
    """

    cursor.execute(sql, (email,))

    usuario = cursor.fetchone()

    if usuario is None:
        return jsonify ({
            "erro": "usuario não encontrado"
        }), 404

    if senha != usuario[3]:
        return jsonify ({
        "erro": "senha ou email incorretos"
    }), 401

    return jsonify ({
        "mensagem": "login realizado com sucesso",
        "id": usuario[0],
        "nome": usuario[1]
    })

@app.post("/tarefas")
def criarTarefa():

    dados = request.json

    titulo = dados["titulo"]
    descricao = dados["descricao"]
    id_user = dados["id_user"]

    sql = """

        INSERT INTO tarefas (titulo, descricao, id_user)
        VALUES (%s, %s, %s)

"""

    valores = (titulo, descricao, id_user)

    cursor.execute(sql, valores)

    banco.commit()

    id_tarefa = cursor.lastrowid

    return jsonify({
        "mensagem": "tarefa cadastrada com sucesso.",
        "tarefa": {
            "id": id_tarefa,
            "titulo": titulo,
            "descricao": descricao
        }
    }), 201

@app.get("/tarefas")
def carregarTarefas():

    id_user = request.args.get("id_user")

    sql = """

        SELECT id, titulo, descricao
        FROM tarefas
        WHERE id_user = %s

"""

    cursor.execute(sql, (id_user,))

    tarefas = cursor.fetchall()

    lista = []

    for tarefa in tarefas:
        lista.append({
            "id": tarefa[0],
            "titulo": tarefa[1],
            "descricao": tarefa[2]
        })

    return jsonify(lista),200

@app.delete("/tarefas/<int:id>")
def deletarTarefas(id):

    sql = """
        DELETE FROM tarefas
        WHERE id = %s
"""

    cursor.execute(sql, (id,))

    banco.commit()

    return jsonify({
        "mensagem": "Tarefa escluida com sucesso."
    }), 200

@app.put("/tarefas/<int:id>")
def editarTarefas(id):

    dados = request.json

    titulo = dados["titulo"]
    descricao = dados["descricao"]

    sql = """

        UPDATE tarefas
        SET titulo = %s, descricao = %s
        WHERE id = %s

"""

    valores = (titulo, descricao, id)

    cursor.execute(sql, valores)

    banco.commit()

    return jsonify ({
        "mensagem": "Tarefa editada com sucesso."
    }), 200


if __name__ == "__main__":
    app.run(debug =True)
