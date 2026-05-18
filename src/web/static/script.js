// Guarda a última origem/destino para recálculo automático
var ultima_origem = null;
var ultimo_destino = null;

// ---- SIMULAÇÃO DE CARGA ----
var veiculo = null;          // marcador do caminhão
var animacao_ativa = false;
var indice_atual = 0;
var pontos_rota = [];        // coordenadas completas da rota
var intervalo_animacao = null;

function limpar_intervalo() {
    if (intervalo_animacao) {
        clearTimeout(intervalo_animacao);
        intervalo_animacao = null;
    }
}

// ------------------------------------------------------------
// Função interna que executa o cálculo de rota (chamada pelas demais)
// ------------------------------------------------------------
function executar_calculo_rota(id_origem, id_destino) {
    var div_texto = document.getElementById('texto_rota');
    div_texto.innerHTML = "Recalculando rota...";

    fetch('/api/rota', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ start: id_origem, target: id_destino })
    })
    .then(function(resposta) { return resposta.json(); })
    .then(function(dados) {
        console.log('Resposta /api/rota:', dados);
        if (dados.has_path) {
            var primeiro_nome = dados.path[0].nome;
            var ultimo_nome = dados.path[dados.path.length - 1].nome;
            var ruas_percurso = (dados.ruas && dados.ruas.length > 0) 
                                ? dados.ruas.join(' → ') 
                                : 'Percurso não disponível';

            var resumo_rota = '<strong>De</strong> ' + primeiro_nome + 
                              ' <strong>para</strong> ' + ultimo_nome;
            var detalhes_percurso = '<details style="margin-top: 10px;">' +
                                    '<summary style="cursor: pointer; font-weight: bold;">🗺️ Ver percurso detalhado</summary>' +
                                    '<p style="margin: 5px 0 0 20px; line-height: 1.6;">' + ruas_percurso + '</p>' +
                                    '</details>';

            if (!window.tempo_inicial) {
                window.tempo_inicial = dados.distance;
            }
            var tempo_atual = dados.distance;
            var eficiencia = ((window.tempo_inicial - tempo_atual) / window.tempo_inicial * 100).toFixed(1);

            div_texto.innerHTML =
                resumo_rota + detalhes_percurso +
                '<br><strong>Tempo total:</strong> ' + dados.distance.toFixed(2) + ' min' +
                '<br><strong>Eficiência:</strong> ' + eficiencia + '%' +
                ' (tempo inicial: ' + window.tempo_inicial.toFixed(2) + ' min, atual: ' + tempo_atual.toFixed(2) + ' min)';

            desenhar_rota(dados.path, 'green');

            // Atualiza pontos da rota global
            pontos_rota = dados.path.map(function(p) { return [p.lat, p.lon]; });

            // Se a entrega estiver ativa, reposiciona o veículo na nova rota
            if (animacao_ativa) {
                console.log('Entrega ativa - reposicionando veículo na nova rota');
                limpar_intervalo();
                if (veiculo && pontos_rota.length > 0) {
                    var pos_atual = veiculo.getLatLng();

                    // Procura o ponto mais próximo **depois** do índice atual
                    var idx_proximo = -1;
                    var dist_min = Infinity;
                    for (var i = indice_atual; i < pontos_rota.length; i++) {
                        var d = Math.pow(pontos_rota[i][0] - pos_atual.lat, 2) + Math.pow(pontos_rota[i][1] - pos_atual.lng, 2);
                        if (d < dist_min) {
                            dist_min = d;
                            idx_proximo = i;
                        }
                    }

                    if (idx_proximo === -1) {
                        console.log('Nenhum ponto à frente – reiniciando animação');
                        if (veiculo) { mapa.removeLayer(veiculo); veiculo = null; }
                        indice_atual = 0;
                        iniciar_animacao();
                    } else {
                        indice_atual = idx_proximo;
                        veiculo.setLatLng(pontos_rota[indice_atual]);
                        mover_veiculo();
                        alert('⚠️ Rota alterada devido a evento de trânsito! O veículo foi redirecionado.');
                    }
                } else {
                    if (veiculo) { mapa.removeLayer(veiculo); veiculo = null; }
                    indice_atual = 0;
                    iniciar_animacao();
                }
            } else {
                // Entrega não está ativa – habilita botão de iniciar
                document.getElementById('botao_iniciar_entrega').disabled = false;
                if (veiculo) { mapa.removeLayer(veiculo); veiculo = null; }
                limpar_intervalo();
            }
        } else {
            console.log('Nenhuma rota encontrada.');
            div_texto.innerHTML = "Não há rota disponível entre os vértices selecionados.";
            limpar_rota();
            document.getElementById('botao_iniciar_entrega').disabled = true;
            if (animacao_ativa) {
                parar_entrega();
            }
        }
    })
    .catch(function(erro) {
        div_texto.innerHTML = "Erro ao calcular rota.";
        console.error(erro);
    });
}

// Função que calcula e exibe a rota interna (Dijkstra) – usa os selects
function calcular_e_mostrar_rota() {
    var id_origem = document.getElementById('origem').value;
    var id_destino = document.getElementById('destino').value;
    if (!id_origem || !id_destino) return;
    executar_calculo_rota(id_origem, id_destino);
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

            desenhar_rota(dados.path, 'blue');

            // Armazena pontos da rota OSRM para a entrega
            pontos_rota = dados.path.map(function(p) { return [p.lat, p.lon]; });
            document.getElementById('botao_iniciar_entrega').disabled = false;
            if (veiculo) {
                mapa.removeLayer(veiculo);
                veiculo = null;
            }
            limpar_intervalo();
            window.tempo_inicial = null;
        } else {
            div_texto.innerHTML = "Não foi possível calcular a rota real.";
            limpar_rota();
            document.getElementById('botao_iniciar_entrega').disabled = true;
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
    window.tempo_inicial = null;

    if (animacao_ativa) {
        parar_entrega();
    }
    if (veiculo) {
        mapa.removeLayer(veiculo);
        veiculo = null;
    }
    calcular_e_mostrar_rota();
});

// ------------------------------------------------------------
// Botão "Simular Evento na Rota Atual"
// (mantido igual, mas agora chama o recálculo correto)
// ------------------------------------------------------------
document.getElementById('botao_simular_evento').addEventListener('click', function() {
    if (!ultima_origem || !ultimo_destino) {
        alert('Calcule uma rota primeiro.');
        return;
    }
    
    var tipo = Math.random() < 0.7 ? 'congestionamento' : 'acidente';
    var fator = tipo === 'congestionamento' ? (Math.random() * 2 + 1.5).toFixed(1) : 1;

    fetch('/api/simular_evento', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            origem: ultima_origem,
            destino: ultimo_destino,
            tipo: tipo,
            fator: parseFloat(fator)
        })
    })
    .then(function(resposta) {
        if (!resposta.ok) throw new Error('Erro na resposta da API');
        return resposta.json();
    })
    .then(function(dados) {
        console.log('Evento simulado:', dados.mensagem);

        // Se a entrega está ativa, recalcula a partir da posição do veículo
        if (animacao_ativa && veiculo) {
            var pos = veiculo.getLatLng();
            fetch('/api/vertice_proximo?lat=' + pos.lat + '&lon=' + pos.lng)
            .then(function(res) { return res.json(); })
            .then(function(vertice) {
                console.log('Vértice próximo:', vertice);
                ultima_origem = vertice.id;
                executar_calculo_rota(ultima_origem, ultimo_destino);
            })
            .catch(function() {
                // fallback: usa a origem original
                executar_calculo_rota(ultima_origem, ultimo_destino);
            });
        } else {
            // Entrega não ativa: recalcula normalmente
            executar_calculo_rota(ultima_origem, ultimo_destino);
        }
    })
    .catch(function(erro) {
        console.error('Erro ao simular evento:', erro);
        alert('Erro ao simular evento. Veja o console.');
    });
});

// ------------------------------------------------------------
// FUNÇÕES DE ENTREGA (ANIMAÇÃO DO VEÍCULO)
// ------------------------------------------------------------
function iniciar_animacao() {
    if (!pontos_rota.length) {
        alert('Nenhuma rota disponível. Calcule uma rota primeiro.');
        return;
    }
    var icone_caminhao = L.icon({
        iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
        shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34]
    });
    if (veiculo) mapa.removeLayer(veiculo);
    veiculo = L.marker(pontos_rota[indice_atual], {icon: icone_caminhao}).addTo(mapa);
    veiculo.bindPopup('🚚 Em trânsito');
    animacao_ativa = true;
    document.getElementById('botao_iniciar_entrega').disabled = true;
    document.getElementById('botao_parar_entrega').disabled = false;
    mover_veiculo();
}

function iniciar_entrega() {
    if (!pontos_rota.length) {
        alert('Nenhuma rota disponível. Calcule uma rota primeiro.');
        return;
    }
    indice_atual = 0;
    limpar_intervalo();
    if (veiculo) mapa.removeLayer(veiculo);
    iniciar_animacao();
}

function parar_entrega() {
    animacao_ativa = false;
    limpar_intervalo();
    document.getElementById('botao_iniciar_entrega').disabled = false;
    document.getElementById('botao_parar_entrega').disabled = true;
}

function mover_veiculo() {
    if (!animacao_ativa) return;
    if (indice_atual >= pontos_rota.length - 1) {
        parar_entrega();
        alert('✅ Entrega concluída!');
        return;
    }
    indice_atual++;
    veiculo.setLatLng(pontos_rota[indice_atual]);
    intervalo_animacao = setTimeout(mover_veiculo, 200);
}

document.getElementById('botao_iniciar_entrega').addEventListener('click', iniciar_entrega);
document.getElementById('botao_parar_entrega').addEventListener('click', parar_entrega);

// ------------------------------------------------------------
// Socket.IO: ao receber evento de trânsito, recalcula automaticamente
// ------------------------------------------------------------
var socket = io.connect('http://' + location.hostname + ':' + location.port);
socket.on('traffic_event', function(data) {
    document.getElementById('texto_notificacao').innerText = data.mensagem;

    if (ultima_origem && ultimo_destino) {
        // Se a entrega está ativa, recalcula a partir da posição do veículo
        if (animacao_ativa && veiculo) {
            var pos = veiculo.getLatLng();
            fetch('/api/vertice_proximo?lat=' + pos.lat + '&lon=' + pos.lng)
            .then(function(res) { return res.json(); })
            .then(function(vertice) {
                console.log('Vértice próximo para recálculo automático:', vertice);
                ultima_origem = vertice.id;
                executar_calculo_rota(ultima_origem, ultimo_destino);
            })
            .catch(function() {
                // fallback: usa a origem original
                executar_calculo_rota(ultima_origem, ultimo_destino);
            });
        } else {
            // Entrega não ativa: recalcula normalmente
            executar_calculo_rota(ultima_origem, ultimo_destino);
        }
    }
});