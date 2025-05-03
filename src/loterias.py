import random
from config import LOTERIA_CONFIG

class GeradorJogos:
    def __init__(self, loteria_config):
        self.loteria_config = loteria_config
        
    def gerar_jogo(self, tipo_loteria):
        """Gera um único jogo aleatório para o tipo de loteria especificado."""
        if tipo_loteria not in self.loteria_config:
            raise ValueError(f"Tipo de loteria '{tipo_loteria}' não encontrado na configuração.")
            
        config = self.loteria_config[tipo_loteria]
        range_inicio, range_fim = config['range']
        quantidade = config['quantidade']
        
        # Gera um jogo aleatório com a quantidade correta de números dentro do intervalo
        jogo = sorted(random.sample(range(range_inicio, range_fim + 1), quantidade))
        
        return jogo
    
    def gerar_jogos(self, tipo_loteria, quantidade_jogos, metodo='aleatorio'):
        """
        Gera a quantidade especificada de jogos únicos para o tipo de loteria.
        
        Parâmetros:
        - tipo_loteria: string com o tipo de loteria ('mega-sena', 'lotofacil', 'quina')
        - quantidade_jogos: quantidade de jogos para gerar
        - metodo: método de geração ('aleatorio', 'estatistico', 'balanceado')
        
        Retorna:
        - Lista de jogos gerados
        """
        if tipo_loteria not in self.loteria_config:
            raise ValueError(f"Tipo de loteria '{tipo_loteria}' não encontrado na configuração.")
            
        config = self.loteria_config[tipo_loteria]
        range_inicio, range_fim = config['range']
        quantidade = config['quantidade']
        
        # Valida se é possível gerar a quantidade solicitada de jogos únicos
        total_combinacoes_possiveis = self._calcular_combinacoes(range_fim - range_inicio + 1, quantidade)
        
        if quantidade_jogos > total_combinacoes_possiveis:
            raise ValueError(f"Não é possível gerar {quantidade_jogos} jogos únicos. O máximo possível é {total_combinacoes_possiveis}.")
        
        # Conjunto para armazenar jogos gerados e garantir unicidade
        jogos_unicos = set()
        
        # Tentativas máximas para evitar loops infinitos
        max_tentativas = quantidade_jogos * 10
        tentativas = 0
        
        # Gera jogos únicos de acordo com o método selecionado
        while len(jogos_unicos) < quantidade_jogos and tentativas < max_tentativas:
            if metodo == 'aleatorio':
                jogo = self.gerar_jogo(tipo_loteria)
            elif metodo == 'estatistico':
                jogo = self._gerar_jogo_estatistico(tipo_loteria)
            elif metodo == 'balanceado':
                jogo = self._gerar_jogo_balanceado(tipo_loteria)
            else:
                jogo = self.gerar_jogo(tipo_loteria)
                
            # Converte o jogo para tupla para poder adicionar ao conjunto (set)
            jogo_tupla = tuple(jogo)
            
            # Adiciona o jogo ao conjunto se ainda não existir
            if jogo_tupla not in jogos_unicos:
                jogos_unicos.add(jogo_tupla)
                
            tentativas += 1
            
        # Converte de volta para lista e ordena cada jogo
        jogos = [list(jogo) for jogo in jogos_unicos]
        
        return jogos
    
    def _gerar_jogo_estatistico(self, tipo_loteria):
        """
        Método exemplo para geração estatística.
        Na implementação real, usaria estatísticas de sorteios anteriores.
        """
        # Aqui seria implementada a lógica com base em estatísticas reais
        # Por enquanto, é apenas um placeholder que gera jogos aleatórios
        return self.gerar_jogo(tipo_loteria)
    
    def _gerar_jogo_balanceado(self, tipo_loteria):
        """
        Método exemplo para geração balanceada (pares/ímpares, dezenas, etc).
        """
        config = self.loteria_config[tipo_loteria]
        range_inicio, range_fim = config['range']
        quantidade = config['quantidade']
        
        # Determina quantos números pares e ímpares incluir
        # Proporção aproximada de 50/50
        n_pares = quantidade // 2
        n_impares = quantidade - n_pares
        
        # Separa os números disponíveis em pares e ímpares
        numeros_pares = [n for n in range(range_inicio, range_fim + 1) if n % 2 == 0]
        numeros_impares = [n for n in range(range_inicio, range_fim + 1) if n % 2 != 0]
        
        # Seleciona números pares e ímpares
        selecionados_pares = random.sample(numeros_pares, n_pares)
        selecionados_impares = random.sample(numeros_impares, n_impares)
        
        # Combina e ordena
        jogo = sorted(selecionados_pares + selecionados_impares)
        
        return jogo
    
    def _calcular_combinacoes(self, n, k):
        """
        Calcula C(n,k) - o número de combinações possíveis.
        Fórmula: n! / (k! * (n-k)!)
        """
        from math import comb
        return comb(n, k)

    def obter_dias_sorteio(self, tipo_loteria):
        """
        Retorna a lista de dias de sorteio para a loteria informada.
        Parâmetros:
        - tipo_loteria: string com o tipo de loteria ('mega-sena', 'lotofacil', etc)
        Retorna:
        - Lista de dias de sorteio (strings)
        """
        if tipo_loteria not in self.loteria_config:
            raise ValueError(f"Tipo de loteria '{tipo_loteria}' não encontrado na configuração.")
        return self.loteria_config[tipo_loteria]['dias_sorteio']


# Exemplo de uso
if __name__ == "__main__":
    # Inicializa o gerador
    gerador = GeradorJogos(LOTERIA_CONFIG)
    
    # Exemplo: gerar 5 jogos da Mega-Sena
    print("Gerando 5 jogos aleatórios da Mega-Sena:")
    jogos_mega = gerador.gerar_jogos('mega-sena', 5)
    for i, jogo in enumerate(jogos_mega, 1):
        print(f"Jogo {i}: {jogo}")
    
    print("\nGerando 3 jogos balanceados da Lotofácil:")
    jogos_lotofacil = gerador.gerar_jogos('lotofacil', 3, metodo='balanceado')
    for i, jogo in enumerate(jogos_lotofacil, 1):
        print(f"Jogo {i}: {jogo}")
    
    print("\nGerando 4 jogos da Quina:")
    jogos_quina = gerador.gerar_jogos('quina', 4)
    for i, jogo in enumerate(jogos_quina, 1):
        print(f"Jogo {i}: {jogo}")

    dias = gerador.obter_dias_sorteio('lotofacil')
    print(dias)  # Saída: ['Quarta-feira', 'Sábado']