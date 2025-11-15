/*(async() => {
    const res = await fetch("/static/unidades.json");
    const data = await res.json();
    console.log(data);

    let footer = "";
    footer += '<div class="container-lg">';
    footer += '<div class="row">';

data.map(unidade => footer += '<div class="col-sm d-flex" style="min-width: 33%">'
    + '<div><h6>' + unidade['nome'] + '</h6>'
    + '<address>'
    + unidade['gestor'] + '<br />'
    + unidade['endereco_linha1'] + '<br />'
    + unidade['endereco_linha2'] + '<br />'
    + 'E-mail: ' + unidade['contatos'][0]['email'] + '<br />'
    + '</address>'
    + '</div></div>');
    footer += '</div></div>';

    console.log(footer);

    document.getElementById("unidades").innerHTML = footer;

})();

*/
window.addEventListener('load', function() {
    if (window.innerWidth < 768) {
        document.getElementById("main-navigation").classList.remove('active');
        document.getElementById("main-navigation").classList.remove('col-sm-4');
        document.getElementById("main-navigation").classList.remove('col-lg-3');
        document.getElementById("main-navigation").classList.remove('px-0');
    }
});