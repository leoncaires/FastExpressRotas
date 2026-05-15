// Guarda a última origem/destino para recálculo automático
var ultima_origem = null;
var ultimo_destino = null;

// Função que calcula e exibe a rota interna (Dijkstra)
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
            // Monta resumo com nome das ruas (usando dados.ruas) e pontos inicial/final
            var primeiro_nome = dados.path[0].nome;
            var ultimo_nome = dados.path[dados.path.length - 1].nome;
            var ruas_percurso = (dados.ruas && dados.ruas.length > 0) 
                                ? dados.ruas.join(' → ') 
                                : 'Percurso não disponível';
            
            var resumo_rota = '<strong>De</strong> ' + primeiro_nome + 
                              ' <strong>para</strong> ' + ultimo_nome;

            // Percurso detalhado em bloco expansível
            var detalhes_percurso = '<details style="margin-top: 10px;">' +
                                    '<summary style="cursor: pointer; font-weight: bold;">🗺️ Ver percurso detalhado</summary>' +
                                    '<p style="margin: 5px 0 0 20px; line-height: 1.6;">' + ruas_percurso + '</p>' +
                                    '</details>';

            // Armazena o tempo da primeira rota calculada (para comparação de eficiência)
            if (!window.tempo_inicial) {
                window.tempo_inicial = dados.distance;
            }

            var tempo_atual = dados.distance;
            var eficiencia = ((window.tempo_inicial - tempo_atual) / window.tempo_inicial * 100).toFixed(1);

            div_texto.innerHTML =
                resumo_rota +
                detalhes_percurso +
                '<br><strong>Tempo total:</strong> ' + dados.distance.toFixed(2) + ' min' +
                '<br><strong>Eficiência:</strong> ' + eficiencia + '%' +
                ' (tempo inicial: ' + window.tempo_inicial.toFixed(2) + ' min, atual: ' + tempo_atual.toFixed(2) + ' min)';

            desenhar_rota(dados.path, 'green');  // verde = algoritmo próprio
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
                '<strong>Rota real (OSRM)</strong>' +
                '<br><strong>Origem:</strong> ' + dados.origem +
                '<br><strong>Destino:</strong> ' + dados.destino +
                '<br><strong>Distância:</strong> ' + dados.distance_km + ' km' +
                '<br><strong>Tempo estimado:</strong> ' + dados.duration_min + ' min';

            desenhar_rota(dados.path, 'blue');  // azul = API externa
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

// Botão "Calcular Rota (Real)"
document.getElementById('botao_calcular_real').addEventListener('click', function() {
    ultima_origem = document.getElementById('origem').value;
    ultimo_destino = document.getElementById('destino').value;
    calcularRotaReal(ultima_origem, ultimo_destino);
});

// Botão "Calcular Rota Interna (Dijkstra)"
document.getElementById('botao_calcular_interno').addEventListener('click', function() {
    ultima_origem = document.getElementById('origem').value;
    ultimo_destino = document.getElementById('destino').value;
    window.tempo_inicial = null;   // reseta o tempo inicial para a nova rota
    calcular_e_mostrar_rota();
});

// Botão "Simular Evento na Rota Atual"
document.getElementById('botao_simular_evento').addEventListener('click', function() {
    if (!ultima_origem || !ultimo_destino) {
        alert('Calcule uma rota interna (Dijkstra) primeiro.');
        return;
    }
    fetch('/api/simular_evento', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            origem: ultima_origem,
            destino: ultimo_destino,
            tipo: 'congestionamento',
            fator: 3.0
        })
    })
    .then(function(resposta) {
        if (!resposta.ok) {
            throw new Error('Erro na resposta da API');
        }
        return resposta.json();
    })
    .then(function(dados) {
        console.log('Evento simulado:', dados.mensagem);
        calcular_e_mostrar_rota();
    })
    .catch(function(erro) {
        console.error('Erro ao simular evento:', erro);
        alert('Erro ao simular evento. Veja o console.');
    });
});

// Socket.IO: ao receber evento de trânsito, recalcula automaticamente
var socket = io.connect('http://' + location.hostname + ':' + location.port);
socket.on('traffic_event', function(data) {
    // Atualiza a notificação
    document.getElementById('texto_notificacao').innerText = data.mensagem;

    // Se já existe uma rota calculada, recalcula (mantém tempo_inicial para comparação)
    if (ultima_origem && ultimo_destino) {
        calcular_e_mostrar_rota();
    }
});