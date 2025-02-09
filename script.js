// Você pode adicionar interatividade aqui, como animações ou manipulação de DOM.
// Por exemplo, um efeito de scroll suave para as seções.

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});