import pandas as pd
import logging
from typing import List, Dict
from models.pokemon import Pokemon

class DataTransformer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    async def transform(self, pokemon_list: List[Dict]) -> Dict:
        """
        Transforma os dados dos Pokémon em análises e estatísticas.
        
        Args:
            pokemon_list: Lista de dicionários com dados dos Pokémon
            
        Returns:
            Dicionário com análises e estatísticas
        """
        try:
            # Converte para DataFrame
            df = pd.DataFrame(pokemon_list)
            
            # Análises por tipo
            tipos_analise = self._analise_por_tipo(df)
            
            # Top 5 por experiência
            top_experiencia = self._top_experiencia(df)
            
            # Estatísticas gerais
            estatisticas = self._estatisticas_gerais(df)
            
            return {
                'tipos_analise': tipos_analise,
                'top_experiencia': top_experiencia,
                'estatisticas': estatisticas
            }
            
        except Exception as e:
            self.logger.error(f"Erro na transformação de dados: {str(e)}")
            raise
            
    def _analise_por_tipo(self, df: pd.DataFrame) -> Dict:
        """Analisa estatísticas por tipo de Pokémon."""
        # Explode a lista de tipos
        df_tipos = df.explode('tipos')
        
        # Agrupa por tipo e calcula médias
        analise = df_tipos.groupby('tipos').agg({
            'ataque': 'mean',
            'defesa': 'mean',
            'hp': 'mean'
        }).round(2)
        
        return analise.to_dict()
        
    def _top_experiencia(self, df: pd.DataFrame) -> List[Dict]:
        """Retorna os 5 Pokémon com maior experiência base."""
        top_5 = df.nlargest(5, 'experiencia_base')[['nome', 'experiencia_base']]
        return top_5.to_dict('records')
        
    def _estatisticas_gerais(self, df: pd.DataFrame) -> Dict:
        """Calcula estatísticas gerais dos Pokémon."""
        return {
            'total_pokemon': len(df),
            'media_ataque': float(df['ataque'].mean()),
            'media_defesa': float(df['defesa'].mean()),
            'media_hp': float(df['hp'].mean()),
            'distribuicao_categorias': df['categoria'].value_counts().to_dict()
        } 