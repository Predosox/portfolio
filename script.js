function mostrarProjetos(tipo) {
    let projetosGrandes = document.getElementById("projetos-grandes");
    let projetosMenores = document.getElementById("projetos-menores");
    let botoes = document.querySelectorAll(".aba");

    if (tipo === "grandes") {
        projetosGrandes.style.display = "block";
        projetosMenores.style.display = "none";
    } else if (tipo === "menores") {
        projetosGrandes.style.display = "none";
        projetosMenores.style.display = "block";
    }

    
    botoes.forEach(botao => botao.classList.remove("ativa"));
    document.querySelector(`button[onclick="mostrarProjetos('${tipo}')"]`).classList.add("ativa");
}
