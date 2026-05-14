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



// Função para calcular rota real usando API OSRM
function calcularRotaReal(id_origem, id_destino) {
    var div_texto = document.getElementById('texto_rota');

    fetch('/api/rota_real', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start: id_origem, target: id_destino })
    })
    .then(function(resposta) { return resposta.json(); })
    .then(function(dados) {

        if (dados.path && dados.path.length > 0) {

            div_texto.innerHTML =
                '<strong>Rota real encontrada</strong>' +
                '<br><strong>Origem:</strong> ' + dados.origem +
                '<br><strong>Destino:</strong> ' + dados.destino +
                '<br><strong>Distância:</strong> ' + dados.distance_km + ' km' +
                '<br><strong>Tempo estimado:</strong> ' + dados.duration_min + ' min';

            desenhar_rota(dados.path);

        } else {
            div_texto.innerHTML = "Não foi possível calcular a rota real.";
            limpar_rota();
        }
    })
    .catch(function(erro) {
        div_texto.innerHTML = "Erro ao consultar API real.";
        console.error(erro);
    });
}


// Botão "Calcular Rota"
document.getElementById('botao_calcular').addEventListener('click', function() {
    ultima_origem = document.getElementById('origem').value;
    ultimo_destino = document.getElementById('destino').value;
    calcularRotaReal(ultima_origem, ultimo_destino);
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