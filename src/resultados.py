import time
from typing import Dict, Any
from config import LOTERIA_API_URLS
import requests


def get_resultado(tipo_loteria: str, concurso: int) -> Dict[str, Any]:
    """
    Busca as dezenas sorteadas para o concurso informado de uma loteria suportada.
    Args:
        tipo_loteria (str): Nome da loteria (ex: 'mega-sena', 'lotofacil', ...)
        concurso (int): Número do concurso
    Returns:
        dict: {'tipo_loteria': tipo_loteria, 'numero_concurso': concurso, 'resultado': [dezenas sorteadas ordenadas]}
    """
    url_base = LOTERIA_API_URLS.get(tipo_loteria)
    campo_dezenas = 'dezenasSorteadasOrdemSorteio'
    if not url_base or not campo_dezenas:
        raise ValueError(f"Loteria '{tipo_loteria}' não suportada.")
    try:
        response = requests.get(f'{url_base}/{concurso}', headers={'Content-Type': 'application/json'})
        print(f'{tipo_loteria} concurso {concurso} Check')
        response.raise_for_status()
        data = response.json()
        dezenas = data.get(campo_dezenas)
        if dezenas is None:
            raise ValueError(f"Campo '{campo_dezenas}' não encontrado na resposta da API.")
        resultado = sorted(dezenas)
        time.sleep(3)
        return {'tipo_loteria': tipo_loteria, 'numero_concurso': concurso, 'resultado': resultado}
    except Exception as e:
        print(f"Erro ao buscar concurso {concurso} da loteria {tipo_loteria}: {e}")
        return {'tipo_loteria': tipo_loteria, 'numero_concurso': concurso, 'resultado': None}


def obter_ultimo_concurso(loteria: str):
    """Obtém informações resumidas do último concurso de uma loteria específica"""
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
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            dados = response.json()
            numero = dados.get('numero')
            data_apuracao = dados.get('dataApuracao')
            dezenas = dados.get('dezenasSorteadasOrdemSorteio')
            houve_ganhadores = False
            lista_rateio = dados.get('listaRateioPremio')
            if lista_rateio and isinstance(lista_rateio, list) and len(lista_rateio) > 0:
                ganhadores = lista_rateio[0].get('numeroDeGanhadores', 0)
                houve_ganhadores = ganhadores > 0
            return {
                'numero': numero,
                'data_apuracao': data_apuracao,
                'dezenas': dezenas,
                'houve_ganhadores': houve_ganhadores
            }
        else:
            print(f"Erro ao obter dados de {loteria}: Status {response.status_code}")
            print(f"Resposta: {response.text}")
        return None
    except Exception as e:
        print(f"Erro ao obter último concurso de {loteria}: {str(e)}")
        return None


if __name__ == "__main__":
    # Exemplo de chamada
    tipo = 'mega-sena'
    concurso = 2000  # Altere para um concurso válido
    resultado = get_resultado(tipo, concurso)
    print(resultado) 

    dados_ultimo = obter_ultimo_concurso('mega-sena')
    print(dados_ultimo)
    