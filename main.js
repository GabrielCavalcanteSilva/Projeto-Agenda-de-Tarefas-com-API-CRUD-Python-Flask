async function cadastrar() {

    const API = 'http://127.0.0.1:5000';
    
    if(document.getElementById("senha").value == document.getElementById("conf-senha").value) {

        const dados = {
            nome: document.getElementById("nome").value,
            email: document.getElementById("email").value,
            senha: document.getElementById("senha").value
        }

        const resposta = await fetch(`${API}/usuarios`, {
            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify(dados)
        });

        if(resposta.ok) {

            alert("Cadastro realizado com sucesso!!")

            window.location.href = "./login.html"

        }

    }

}

async function logar() {
    
    const API = 'http://127.0.0.1:5000';

        const dados = {
            nome: document.getElementById("nome").value,
            email: document.getElementById("email").value,
            senha: document.getElementById("senha").value
        }

        const resposta = await fetch(`${API}/login`, {
            method: 'POST',

            headers: {
                'Content-Type': 'application/json'
            },

            body: JSON.stringify(dados)
        });

        const res = await resposta.json()

        if(resposta.ok) {

            localStorage.setItem("id", res.id)
            localStorage.setItem("email", dados.email)
            localStorage.setItem("nome", dados.nome)

            alert("Login realizado com sucesso!!")

            window.location.href = "./index.html"

        } else {
            alert (res.erro)
        }

}

function sair() {
    localStorage.removeItem("id");
    localStorage.removeItem("nome");
    localStorage.removeItem("email");

    window.location.href = "./login.html";
}

async function criarTarefa() {

    const API = 'http://127.0.0.1:5000';

    const titulo = document.getElementById("titulo").value
    const descricao = document.getElementById("descricao").value

    if(titulo === "" || descricao === "") {
        alert ("Existem campos vazios!! Preencha todos os campos.")
        return
    }

    const dados = {
        titulo: document.getElementById("titulo").value,
        descricao: document.getElementById("descricao").value,
        id_user: localStorage.getItem("id")
    }

    const resposta = await fetch(`${API}/tarefas`, {

        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(dados)

    })

    const res = await resposta.json()

    if(resposta.ok) {

        adicionarTarefaNaTela(res.tarefa)

    }
}

async function carregarTarefas() {

    const API = 'http://127.0.0.1:5000'

    const id_user = localStorage.getItem("id")

    const resposta = await fetch(`${API}/tarefas?id_user=${id_user}`)

    const res = await resposta.json()

    if(resposta.ok) {
        res.forEach(tarefa => {
            console.log("Adicionando:", tarefa);
            adicionarTarefaNaTela(tarefa);
        });
    }

}

async function deletarTarefas(elemento) {

    const API = "http://127.0.0.1:5000"

    const id = elemento.dataset.id;

    const resposta = await fetch(`${API}/tarefas/${id}`, {

        method: "DELETE",

    })

    if(resposta.ok) {
        removerTarefaDaTela(id)
    }

}

async function editarTarefas() {

    const API = "http://127.0.0.1:5000"

    const dados = pegarTarefaEditando()

   if(dados === null) {
        return;
   }

    const resposta = await fetch(`${API}/tarefas/${dados.id}`, {

        method: "PUT",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(dados)

    })

    const res = await resposta.json()

    if(resposta.ok) {

        atualizarTarefaNaTela(dados);

        fecharModal();

    }



}

carregarTarefas()