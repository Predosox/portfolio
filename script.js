function mostrarProjetos(tipo) {
    let projetosGrandes = document.getElementById("projetos-grandes");
    let projetosMenores = document.getElementById("projetos-menores");
    let botoes = document.querySelectorAll(".aba");

    if (tipo === "grandes") {
        projetosGrandes.style.opacity = "0";
        setTimeout(() => {
            projetosGrandes.style.display = "flex";
            projetosMenores.style.display = "none";
            projetosGrandes.style.opacity = "1";
        }, 300);
    } else {
        projetosMenores.style.opacity = "0";
        setTimeout(() => {
            projetosMenores.style.display = "flex";
            projetosGrandes.style.display = "none";
            projetosMenores.style.opacity = "1";
        }, 300);
    }

    // Muda a aba ativa
    botoes.forEach(botao => botao.classList.remove("ativa"));
    document.querySelector(`button[onclick="mostrarProjetos('${tipo}')"]`).classList.add("ativa");
}