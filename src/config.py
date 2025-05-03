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
    'mega-sena': {'range': (1, 60), 'quantidade': 6, 'dias_sorteio': ['Terça-feira', 'Quinta-feira', 'Sábado']},
    'lotofacil': {'range': (1, 25), 'quantidade': 15, 'dias_sorteio': ['Segunda a Sábado']},
    'quina': {'range': (1, 80), 'quantidade': 5, 'dias_sorteio': ['Segunda a Sábado']},
    'lotomania': {'range': (1, 100), 'quantidade': 50, 'dias_sorteio': ['Segunda-feira', 'Quarta-feira', 'Sexta-feira']},
    'timemania': {'range': (1, 80), 'quantidade': 10, 'dias_sorteio': ['Terça-feira', 'Quinta-feira', 'Sábado']},
    'dupla-sena': {'range': (1, 50), 'quantidade': 6, 'dias_sorteio': ['Segunda-feira', 'Quarta-feira', 'Sexta-feira']},
    'dia-de-sorte': {'range': (1, 31), 'quantidade': 7, 'dias_sorteio': ['Terça-feira', 'Quinta-feira', 'Sábado']},
    'super-sete': {'range': (0, 9), 'quantidade': 7, 'dias_sorteio': ['Segunda-feira', 'Quarta-feira', 'Sexta-feira']},
    'mais-milionaria': {'range': (1, 50), 'quantidade': 6, 'dias_sorteio': ['Quarta-feira', 'Sábado']}
}