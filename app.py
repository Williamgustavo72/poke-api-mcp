import random
from enum import Enum
from typing import List, Dict, Set, Tuple
import secrets
import hashlib
from collections import Counter

class TipoLoteria(Enum):
    MEGASENA = "megasena"
    LOTOFACIL = "lotofacil"
    QUINA = "quina"

class ConfiguracaoLoteria:
    def __init__(self, numero_min: int, numero_max: int, quantidade_min: int, quantidade_max: int):
        self.numero_min = numero_min
        self.numero_max = numero_max
        self.quantidade_min = quantidade_min
        self.quantidade_max = quantidade_max

class GeradorLoteria:
    def __init__(self):
        self.configuracoes: Dict[TipoLoteria, ConfiguracaoLoteria] = {
            TipoLoteria.MEGASENA: ConfiguracaoLoteria(1, 60, 6, 15),
            TipoLoteria.LOTOFACIL: ConfiguracaoLoteria(1, 25, 15, 20),
            TipoLoteria.QUINA: ConfiguracaoLoteria(1, 80, 5, 15)
        }
        # Usar secrets para melhor aleatoriedade
        self._rng = random.SystemRandom()

    def _gerar_hash_jogo(self, jogo: List[int]) -> str:
        """Gera um hash único para um jogo."""
        jogo_str = "-".join(map(str, sorted(jogo)))
        return hashlib.sha256(jogo_str.encode()).hexdigest()

    def _validar_jogo_unico(self, novo_jogo: List[int], jogos_existentes: List[List[int]]) -> bool:
        """Verifica se o jogo já existe no conjunto de jogos."""
        novo_hash = self._gerar_hash_jogo(novo_jogo)
        for jogo in jogos_existentes:
            if self._gerar_hash_jogo(jogo) == novo_hash:
                return False
        return True

    def _validar_distribuicao(self, jogo: List[int], config: ConfiguracaoLoteria) -> bool:
        """Valida se a distribuição dos números no jogo está adequada."""
        # Verifica se há muitos números consecutivos
        consecutivos = 0
        for i in range(1, len(jogo)):
            if jogo[i] == jogo[i-1] + 1:
                consecutivos += 1
                if consecutivos > 3:  # Não permite mais de 4 números consecutivos
                    return False
            else:
                consecutivos = 0
        
        # Verifica a distribuição entre números pares e ímpares
        pares = sum(1 for n in jogo if n % 2 == 0)
        impares = len(jogo) - pares
        min_ratio = 0.3  # No mínimo 30% de cada
        if pares/len(jogo) < min_ratio or impares/len(jogo) < min_ratio:
            return False
        
        return True

    def validar_quantidade(self, tipo_loteria: TipoLoteria, quantidade_numeros: int) -> bool:
        config = self.configuracoes[tipo_loteria]
        if not (config.quantidade_min <= quantidade_numeros <= config.quantidade_max):
            raise ValueError(
                f"A quantidade de números para {tipo_loteria.value} deve estar entre "
                f"{config.quantidade_min} e {config.quantidade_max}"
            )
        return True

    def gerar_jogos(self, tipo_loteria: TipoLoteria, quantidade_jogos: int, numeros_por_jogo: int) -> List[List[str]]:
        """
        Gera jogos de números aleatórios ordenados e não repetidos para um tipo específico de loteria.
        
        Args:
            tipo_loteria (TipoLoteria): Tipo de loteria (MEGASENA, LOTOFACIL, etc)
            quantidade_jogos (int): Quantidade de jogos a serem gerados
            numeros_por_jogo (int): Quantidade de números em cada jogo
        
        Returns:
            List[List[str]]: Lista de jogos, onde cada jogo é uma lista de números formatados
        """
        config = self.configuracoes[tipo_loteria]
        self.validar_quantidade(tipo_loteria, numeros_por_jogo)
        
        jogos_gerados = []
        tentativas_maximas = quantidade_jogos * 10  # Limite de tentativas para evitar loop infinito
        tentativas = 0
        
        while len(jogos_gerados) < quantidade_jogos and tentativas < tentativas_maximas:
            # Gera um novo jogo usando secrets para maior aleatoriedade
            numeros_disponiveis = list(range(config.numero_min, config.numero_max + 1))
            self._rng.shuffle(numeros_disponiveis)
            novo_jogo = sorted(numeros_disponiveis[:numeros_por_jogo])
            
            # Valida o novo jogo
            if (self._validar_jogo_unico(novo_jogo, jogos_gerados) and 
                self._validar_distribuicao(novo_jogo, config)):
                jogos_gerados.append(novo_jogo)
            
            tentativas += 1
        
        if len(jogos_gerados) < quantidade_jogos:
            raise RuntimeError(
                f"Não foi possível gerar {quantidade_jogos} jogos únicos com a "
                f"distribuição desejada após {tentativas_maximas} tentativas."
            )
        
        # Converte para o formato de strings com zeros à esquerda
        return [[f"{numero:02d}" for numero in jogo] for jogo in jogos_gerados]

    def analisar_jogos(self, jogos: List[List[str]]) -> Dict:
        """
        Analisa a qualidade dos jogos gerados.
        
        Returns:
            Dict: Estatísticas sobre os jogos gerados
        """
        numeros_flat = [int(num) for jogo in jogos for num in jogo]
        
        # Análise de frequência
        frequencia = Counter(numeros_flat)
        
        # Análise de paridade
        pares = sum(1 for n in numeros_flat if int(n) % 2 == 0)
        impares = len(numeros_flat) - pares
        
        return {
            "total_jogos": len(jogos),
            "numeros_por_jogo": len(jogos[0]),
            "distribuicao_frequencia": dict(frequencia),
            "porcentagem_pares": (pares / len(numeros_flat)) * 100,
            "porcentagem_impares": (impares / len(numeros_flat)) * 100
        }

def imprimir_jogos(jogos: List[List[str]], tipo_loteria: TipoLoteria):
    """
    Imprime os jogos gerados de forma formatada.
    """
    print(f"\nJogos gerados para {tipo_loteria.value.upper()}:")
    print("-" * 50)
    for i, jogo in enumerate(jogos, 1):
        numeros_formatados = " - ".join(jogo)
        print(f"Jogo {i:02d}: {numeros_formatados}")
    print("-" * 50)

def imprimir_analise(analise: Dict):
    """
    Imprime a análise dos jogos gerados.
    """
    print("\nAnálise dos jogos gerados:")
    print("-" * 50)
    print(f"Total de jogos: {analise['total_jogos']}")
    print(f"Números por jogo: {analise['numeros_por_jogo']}")
    print(f"Porcentagem de números pares: {analise['porcentagem_pares']:.1f}%")
    print(f"Porcentagem de números ímpares: {analise['porcentagem_impares']:.1f}%")
    #print("\nDistribuição de frequência dos números:")
    #for num, freq in sorted(analise['distribuicao_frequencia'].items()):
    #    print(f"Número {num:02d}: {freq} vezes")
    print("-" * 50)

# Exemplo de uso
if __name__ == "__main__":
    gerador = GeradorLoteria()
    
    # Exemplo de jogos da Mega-Sena
    jogos_mega = gerador.gerar_jogos(TipoLoteria.MEGASENA, quantidade_jogos=5, numeros_por_jogo=6)
    imprimir_jogos(jogos_mega, TipoLoteria.MEGASENA)
    analise_mega = gerador.analisar_jogos(jogos_mega)
    imprimir_analise(analise_mega)
    
    # Exemplo de jogos da Lotofácil
    jogos_lotofacil = gerador.gerar_jogos(TipoLoteria.LOTOFACIL, quantidade_jogos=3, numeros_por_jogo=15)
    imprimir_jogos(jogos_lotofacil, TipoLoteria.LOTOFACIL)
    analise_lotofacil = gerador.analisar_jogos(jogos_lotofacil)
    imprimir_analise(analise_lotofacil)
