// Aguarda o carregamento do DOM e carrega marcadores de todos os vértices
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/vertices')
        .then(function(resposta) { return resposta.json(); })
        .then(function(lista_vertices) {
            lista_vertices.forEach(function(v) {
                L.marker([v.lat, v.lon]).addTo(mapa).bindPopup(v.nome);
            });
        });
});

// Evento do botão "Calcular Rota"
document.getElementById('botao_calcular').addEventListener('click', function() {
    var id_origem = document.getElementById('origem').value;
    var id_destino = document.getElementById('destino').value;
    var div_texto = document.getElementById('texto_rota');

    div_texto.innerHTML = "Calculando...";

    fetch('/api/rota', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start: id_origem, target: id_destino })
    })
    .then(function(resposta) { return resposta.json(); })
    .then(function(dados) {
        if (dados.has_path) {
            // Constrói string dos nomes dos vértices no caminho
            var nomes_caminho = dados.path.map(function(v) { return v.nome; }).join(' → ');
            div_texto.innerHTML =
                '<strong>Rota encontrada:</strong> ' + nomes_caminho +
                '<br><strong>Tempo total:</strong> ' + dados.distance + ' min';
            desenhar_rota(dados.path);  // função definida em map.js
        } else {
            div_texto.innerHTML = "Não há rota disponível entre os vértices selecionados.";
            limpar_rota();  // limpa mapa
        }
    })
    .catch(function(erro) {
        div_texto.innerHTML = "Erro ao calcular rota.";
        console.error(erro);
    });
});