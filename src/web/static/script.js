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

// Guarda a última origem/destino para recálculo automático
var ultima_origem = null;
var ultimo_destino = null;

// Função que calcula e exibe a rota
function calcular_e_mostrar_rota() {
    var id_origem = document.getElementById('origem').value;
    var id_destino = document.getElementById('destino').value;
    var div_texto = document.getElementById('texto_rota');

    if (!id_origem || !id_destino) {
        return;
    }

    div_texto.innerHTML = "Recalculando rota...";

    fetch('/api/rota', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start: id_origem, target: id_destino })
    })
    .then(function(resposta) { return resposta.json(); })
    .then(function(dados) {
        if (dados.has_path) {
            var nomes_caminho = dados.path.map(function(v) { return v.nome; }).join(' → ');
            div_texto.innerHTML =
                '<strong>Rota encontrada:</strong> ' + nomes_caminho +
                '<br><strong>Tempo total:</strong> ' + dados.distance + ' min';
            desenhar_rota(dados.path);
        } else {
            div_texto.innerHTML = "Não há rota disponível entre os vértices selecionados.";
            limpar_rota();
        }
    })
    .catch(function(erro) {
        div_texto.innerHTML = "Erro ao calcular rota.";
        console.error(erro);
    });
}

// Botão "Calcular Rota"
document.getElementById('botao_calcular').addEventListener('click', function() {
    ultima_origem = document.getElementById('origem').value;
    ultimo_destino = document.getElementById('destino').value;
    calcular_e_mostrar_rota();
});

// Socket.IO: ao receber evento de trânsito, recalcula automaticamente
var socket = io.connect('http://' + document.domain + ':' + location.port);
socket.on('traffic_event', function(data) {
    // Atualiza a notificação
    document.getElementById('texto_notificacao').innerText = data.mensagem;

    // Se já existe uma rota calculada, recalcula
    if (ultima_origem && ultimo_destino) {
        calcular_e_mostrar_rota();
    }
});