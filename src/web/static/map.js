// Inicializa o mapa Leaflet com visão central (São Paulo) e zoom 13
var mapa = L.map('mapa').setView([-23.555, -46.64], 13);

// Camada de tiles do OpenStreetMap (gratuita, sem chave de API)
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(mapa);

// Variáveis para gerenciar a linha da rota e marcadores
var camada_rota = null;   // polyline da rota atual
var marcadores = [];      // array com marcadores de origem/destino

function limpar_rota() {
    // Remove a rota anterior do mapa, se existir
    if (camada_rota) {
        mapa.removeLayer(camada_rota);
        camada_rota = null;
    }
    // Remove marcadores antigos
    marcadores.forEach(function(marcador) {
        mapa.removeLayer(marcador);
    });
    marcadores = [];
}

function desenhar_rota(dados_caminho) {
    // Limpa desenho anterior
    limpar_rota();
    if (!dados_caminho || dados_caminho.length === 0) return;

    // Converte os dados de caminho (lat, lon) em array de coordenadas
    var coordenadas = dados_caminho.map(function(v) {
        return [v.lat, v.lon];
    });

    // Cria uma polyline verde e adiciona ao mapa
    camada_rota = L.polyline(coordenadas, { color: 'green', weight: 4 }).addTo(mapa);

    // Adiciona marcadores no início e fim da rota
    var marcador_inicio = L.marker(coordenadas[0], { title: 'Origem' })
        .addTo(mapa)
        .bindPopup('Origem: ' + dados_caminho[0].nome);
    var marcador_fim = L.marker(coordenadas[coordenadas.length - 1], { title: 'Destino' })
        .addTo(mapa)
        .bindPopup('Destino: ' + dados_caminho[dados_caminho.length - 1].nome);

    marcadores.push(marcador_inicio, marcador_fim);

    // Ajusta a visualização para enquadrar toda a rota
    mapa.fitBounds(coordenadas);
}

async function calcularRotaReal(startId, targetId) {
    const resposta = await fetch('/api/rota_real', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            start: startId,
            target: targetId
        })
    });

    const dados = await resposta.json();

    limpar_rota();

    const coordenadas = dados.path.map(function(p) {
        return [p.lat, p.lon];
    });

    camada_rota = L.polyline(coordenadas, {
        color: 'blue',
        weight: 5
    }).addTo(mapa);

    mapa.fitBounds(coordenadas);

    alert(
        'Rota real calculada via API OSRM\n' +
        'Origem: ' + dados.origem + '\n' +
        'Destino: ' + dados.destino + '\n' +
        'Distância: ' + dados.distance_km + ' km\n' +
        'Tempo estimado: ' + dados.duration_min + ' min'
    );
}
