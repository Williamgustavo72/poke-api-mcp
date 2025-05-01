# Gerador de Jogos de Loteria

Este projeto implementa um gerador de jogos para diferentes modalidades de loteria (Mega-Sena, Lotofácil e Quina) com foco em qualidade e aleatoriedade dos números gerados.

## Características

- Suporte para múltiplas modalidades de loteria:
  - Mega-Sena (6 a 15 números, intervalo 1-60)
  - Lotofácil (15 a 20 números, intervalo 1-25)
  - Quina (5 a 15 números, intervalo 1-80)
- Geração de números com alta qualidade de aleatoriedade usando `random.SystemRandom`
- Validação de jogos para evitar repetições
- Análise de distribuição dos números gerados
- Formatação amigável dos resultados

## Requisitos

- Python 3.6 ou superior

## Instalação

1. Clone o repositório:
```bash
git clone [URL_DO_REPOSITORIO]
cd [NOME_DO_DIRETORIO]
```

## Uso

Para usar o gerador, importe e utilize a classe `GeradorLoteria`:

```python
from app import GeradorLoteria, TipoLoteria

# Criar uma instância do gerador
gerador = GeradorLoteria()

# Gerar jogos da Mega-Sena (5 jogos com 6 números cada)
jogos_mega = gerador.gerar_jogos(TipoLoteria.MEGASENA, quantidade_jogos=5, numeros_por_jogo=6)

# Gerar jogos da Lotofácil (3 jogos com 15 números cada)
jogos_lotofacil = gerador.gerar_jogos(TipoLoteria.LOTOFACIL, quantidade_jogos=3, numeros_por_jogo=15)

# Analisar os jogos gerados
analise = gerador.analisar_jogos(jogos_mega)
```

## Características de Segurança

- Utiliza `random.SystemRandom()` para geração de números aleatórios criptograficamente seguros
- Validação de distribuição para evitar padrões previsíveis
- Verificação de unicidade dos jogos gerados

## Validações Implementadas

1. **Números Únicos**: Garante que não há números repetidos no mesmo jogo
2. **Jogos Únicos**: Evita a geração de jogos idênticos no mesmo conjunto
3. **Distribuição Equilibrada**:
   - Limita sequências de números consecutivos
   - Mantém equilíbrio entre números pares e ímpares
4. **Limites por Modalidade**: Respeita as regras específicas de cada tipo de loteria

## Exemplo de Saída

```
Jogos gerados para MEGASENA:
--------------------------------------------------
Jogo 01: 03 - 15 - 27 - 35 - 42 - 58
Jogo 02: 07 - 13 - 22 - 45 - 51 - 60
Jogo 03: 02 - 11 - 19 - 33 - 47 - 55
--------------------------------------------------

Análise dos jogos gerados:
--------------------------------------------------
Total de jogos: 3
Números por jogo: 6
Porcentagem de números pares: 44.4%
Porcentagem de números ímpares: 55.6%
--------------------------------------------------
```

## Contribuição

Sinta-se à vontade para contribuir com o projeto através de Pull Requests ou reportando issues.

## Licença

Este projeto está sob a licença MIT. 