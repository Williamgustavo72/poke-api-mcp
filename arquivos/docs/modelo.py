from flask import Flask, render_template, jsonify, request
import requests
from bs4 import BeautifulSoup
import random
import json
from datetime import datetime
import schedule
import time
import threading

app = Flask(__name__)

# URLs da API da Loteria Caixa
LOTERIA_API_URLS = {
    'mega-sena': 'https://servicebus2.caixa.gov.br/portaldeloterias/api/megasena',
    'lotofacil': 'https://servicebus2.caixa.gov.br/portaldeloterias/api/lotofacil',
    'quina': 'https://servicebus2.caixa.gov.br/portaldeloterias/api/quina',
    'lotomania': 'https://servicebus2.caixa.gov.br/portaldeloterias/api/lotomania',
    'timemania': 'https://servicebus2.caixa.gov.br/portaldeloterias/api/timemania',
    'dupla-sena': 'https://servicebus2.caixa.gov.br/portaldeloterias/api/duplasena',
    'dia-de-sorte': 'https://servicebus2.caixa.gov.br/portaldeloterias/api/diadesorte',
    'super-sete': 'https://servicebus2.caixa.gov.br/portaldeloterias/api/supersete',
    'mais-milionaria': 'https://servicebus2.caixa.gov.br/portaldeloterias/api/maismilionaria'
}

# Configurações dos jogos
LOTERIA_CONFIG = {
    'mega-sena': {'range': (1, 60), 'quantidade': 6, 'dias_sorteio': ['Quarta-feira', 'Sábado']},
    'lotofacil': {'range': (1, 25), 'quantidade': 15, 'dias_sorteio': ['Segunda-feira', 'Terça-feira', 'Quarta-feira', 'Quinta-feira', 'Sexta-feira']},
    'quina': {'range': (1, 80), 'quantidade': 5, 'dias_sorteio': ['Segunda a Sábado']},
    'lotomania': {'range': (1, 100), 'quantidade': 50, 'dias_sorteio': ['Segunda-feira', 'Quarta-feira', 'Sexta-feira']},
    'timemania': {'range': (1, 80), 'quantidade': 10, 'dias_sorteio': ['Terça-feira', 'Quinta-feira', 'Sábado']},
    'dupla-sena': {'range': (1, 50), 'quantidade': 6, 'dias_sorteio': ['Segunda-feira', 'Quarta-feira', 'Sexta-feira']},
    'dia-de-sorte': {'range': (1, 31), 'quantidade': 7, 'dias_sorteio': ['Terça-feira', 'Quinta-feira', 'Sábado']},
    'super-sete': {'range': (0, 9), 'quantidade': 7, 'dias_sorteio': ['Segunda-feira', 'Quarta-feira', 'Sexta-feira']},
    'mais-milionaria': {'range': (1, 50), 'quantidade': 6, 'dias_sorteio': ['Sábado']}
}

class LoteriasSimulator:
    def __init__(self):
        self.resultados = {}
        self.jogos_gerados = {}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'application/json',
            'Origin': 'https://loterias.caixa.gov.br',
            'Referer': 'https://loterias.caixa.gov.br/'
        }
        
    def obter_ultimo_concurso(self, loteria):
        """Obtém o último concurso de uma loteria específica"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': '*/*',
                'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
                'Origin': 'https://loterias.caixa.gov.br',
                'Referer': 'https://loterias.caixa.gov.br/',
                'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
                'Sec-Ch-Ua-Mobile': '?0',
                'Sec-Ch-Ua-Platform': '"Windows"',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-site'
            }
            
            url = f"{LOTERIA_API_URLS[loteria]}"
            session = requests.Session()
            response = session.get(url, headers=headers, verify=False)
            
            if response.status_code == 200:
                dados = response.json()
                print(f"Dados obtidos com sucesso para {loteria}")
                return dados
            else:
                print(f"Erro ao obter dados de {loteria}: Status {response.status_code}")
                print(f"Resposta: {response.text}")
            return None
        except Exception as e:
            print(f"Erro ao obter último concurso de {loteria}: {str(e)}")
            return None

    def processar_resultado_quina(self, resultado):
        """Processa o resultado específico da Quina"""
        try:
            info_resultado = {
                'dezenas': resultado.get('dezenas', []),
                'concurso': resultado.get('numero', ''),
                'data_sorteio': resultado.get('dataApuracao', ''),
                'proximo_concurso': resultado.get('numeroConcursoProximo', ''),
                'data_proximo_sorteio': resultado.get('dataProximoConcurso', ''),
                'acumulado': resultado.get('acumulado', False),
                'valor_acumulado': resultado.get('valorAcumulado', '0,00'),
                'local_sorteio': resultado.get('localSorteio', ''),
                'dias_sorteio': ['Segunda a Sábado'],
                'premiacoes': []
            }

            # Processamento específico das premiações da Quina
            premiacoes = resultado.get('listaRateioPremio', [])
            faixas_quina = {
                '5': 'Quina',
                '4': 'Quadra',
                '3': 'Terno',
                '2': 'Duque'
            }
            
            for premiacao in premiacoes:
                faixa = premiacao.get('faixa', '')
                info_premiacao = {
                    'descricao': faixas_quina.get(str(faixa), f'{faixa} Acertos'),
                    'quantidade': premiacao.get('numeroDeGanhadores', 0),
                    'valorPremio': premiacao.get('valorPremio', '0,00')
                }
                info_resultado['premiacoes'].append(info_premiacao)

            return info_resultado
        except Exception as e:
            print(f"Erro ao processar resultado da Quina: {str(e)}")
            return None

    def atualizar_resultados(self):
        """Atualiza os resultados das loterias usando a API oficial"""
        print("Iniciando atualização dos resultados...")
        for loteria in LOTERIA_CONFIG.keys():
            try:
                print(f"Atualizando {loteria}...")
                resultado = self.obter_ultimo_concurso(loteria)
                if resultado:
                    if loteria == 'quina':
                        info_resultado = self.processar_resultado_quina(resultado)
                    else:
                        info_resultado = {
                            'dezenas': resultado.get('dezenas', []),
                            'concurso': resultado.get('numero', ''),
                            'data_sorteio': resultado.get('dataApuracao', ''),
                            'proximo_concurso': resultado.get('numeroConcursoProximo', ''),
                            'data_proximo_sorteio': resultado.get('dataProximoConcurso', ''),
                            'acumulado': resultado.get('acumulado', False),
                            'valor_acumulado': resultado.get('valorAcumulado', '0,00'),
                            'local_sorteio': resultado.get('localSorteio', ''),
                            'dias_sorteio': LOTERIA_CONFIG[loteria]['dias_sorteio'],
                            'premiacoes': []
                        }

                        premiacoes = resultado.get('listaRateioPremio', [])
                        for premiacao in premiacoes:
                            info_premiacao = {
                                'descricao': premiacao.get('descricaoFaixa', ''),
                                'quantidade': premiacao.get('numeroDeGanhadores', 0),
                                'valorPremio': premiacao.get('valorPremio', '0,00')
                            }
                            info_resultado['premiacoes'].append(info_premiacao)

                        if loteria == 'mais-milionaria':
                            info_resultado['trevos'] = resultado.get('listaTrevos', [])

                    if info_resultado:
                        self.resultados[loteria] = info_resultado
                        print(f"Atualizado {loteria}: Concurso {info_resultado['concurso']}")
                    else:
                        print(f"Não foi possível processar o resultado de {loteria}")
                else:
                    print(f"Não foi possível atualizar {loteria}")

            except Exception as e:
                print(f"Erro ao atualizar {loteria}: {str(e)}")
                continue

    def verificar_premiacao(self, tipo_loteria, numeros):
        """Verifica se um jogo foi premiado"""
        if tipo_loteria not in self.resultados:
            return None
            
        resultado = self.resultados[tipo_loteria]
        dezenas_sorteadas = set(resultado['dezenas'])
        dezenas_jogadas = set(str(num) for num in numeros)  # Convertendo para string para garantir compatibilidade
        
        acertos = len(dezenas_sorteadas.intersection(dezenas_jogadas))
        
        return {
            'acertos': acertos,
            'concurso': resultado['concurso'],
            'data_sorteio': resultado['data_sorteio']
        }

    def gerar_jogo(self, tipo_loteria):
        """Gera um jogo aleatório para o tipo de loteria especificado"""
        try:
            if tipo_loteria not in LOTERIA_CONFIG:
                print(f"Tipo de loteria inválido: {tipo_loteria}")
                return None
                
            config = LOTERIA_CONFIG[tipo_loteria]
            numeros = sorted(random.sample(range(config['range'][0], config['range'][1] + 1), 
                                        config['quantidade']))
            
            # Tratamento especial para +Milionária (2 trevos)
            trevos = []
            if tipo_loteria == 'mais-milionaria':
                trevos = sorted(random.sample(range(1, 7), 2))
            
            jogo = {
                'numeros': [str(num) for num in numeros],  # Convertendo números para string
                'trevos': [str(num) for num in trevos] if tipo_loteria == 'mais-milionaria' else None,
                'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Verificar premiação se houver resultado disponível
            premiacao = self.verificar_premiacao(tipo_loteria, numeros)
            if premiacao:
                jogo['premiacao'] = premiacao
            
            if tipo_loteria not in self.jogos_gerados:
                self.jogos_gerados[tipo_loteria] = []
            
            # Limitar o histórico a 10 jogos por tipo
            if len(self.jogos_gerados[tipo_loteria]) >= 10:
                self.jogos_gerados[tipo_loteria].pop(0)
            
            self.jogos_gerados[tipo_loteria].append(jogo)
            print(f"Jogo gerado com sucesso para {tipo_loteria}: {jogo}")
            return jogo
            
        except Exception as e:
            print(f"Erro ao gerar jogo para {tipo_loteria}: {str(e)}")
            return None

simulator = LoteriasSimulator()

def agendar_atualizacoes():
    """Agenda atualizações dos resultados"""
    # Atualiza a cada 30 minutos
    schedule.every(30).minutes.do(simulator.atualizar_resultados)
    
    # Atualiza em horários específicos de sorteio
    schedule.every().day.at("20:00").do(simulator.atualizar_resultados)  # Horário principal
    schedule.every().day.at("16:00").do(simulator.atualizar_resultados)  # Loteria Federal
    
    while True:
        schedule.run_pending()
        time.sleep(60)

# Iniciar thread para atualizações agendadas
thread_atualizacao = threading.Thread(target=agendar_atualizacoes)
thread_atualizacao.daemon = True
thread_atualizacao.start()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/gerar-jogo/<tipo_loteria>')
def gerar_novo_jogo(tipo_loteria):
    try:
        print(f"Recebendo requisição para gerar jogo de {tipo_loteria}")
        jogo = simulator.gerar_jogo(tipo_loteria)
        if jogo:
            print(f"Jogo gerado com sucesso: {jogo}")
            return jsonify(jogo)
        print(f"Erro: tipo de loteria inválido - {tipo_loteria}")
        return jsonify({'error': 'Tipo de loteria inválido'}), 400
    except Exception as e:
        print(f"Erro ao gerar jogo: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/resultados')
def get_resultados():
    return jsonify(simulator.resultados)

@app.route('/api/jogos-anteriores/<tipo_loteria>')
def get_jogos_anteriores(tipo_loteria):
    if tipo_loteria in simulator.jogos_gerados:
        return jsonify(simulator.jogos_gerados[tipo_loteria])
    return jsonify([])

if __name__ == '__main__':
    # Fazer primeira atualização ao iniciar
    simulator.atualizar_resultados()
    app.run(debug=True)