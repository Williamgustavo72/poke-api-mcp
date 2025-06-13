import pandas as pd
import matplotlib.pyplot as plt
import logging
from typing import Dict, List
import os
import numpy as np

class ReportGenerator:
    def __init__(self):
        """Inicializa o gerador de relatórios."""
        self.logger = logging.getLogger(__name__)
        self.output_dir = os.path.join("relatorios")
        
        # Cria o diretório de saída se ele não existir
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            self.logger.info(f"Diretório '{self.output_dir}' criado.")

    # --- MÉTODOS PÚBLICOS ---

    async def generate(self, data: Dict) -> Dict:
        """
        Gera relatórios e visualizações a partir dos dados transformados.
        
        Args:
            data: Dicionário com dados transformados.
            
        Returns:
            Dicionário com caminhos dos arquivos gerados.
        """
        try:
            self.logger.info("Iniciando a geração de relatórios...")
            
            # Prepara os DataFrames que serão usados em múltiplos locais
            df_tipos = self._preparar_df_tipos(data.get('tipos_analise', {}))
            df_top = self._preparar_df_top(data.get('top_experiencia', []))

            # Gera relatórios a partir dos DataFrames preparados
            csv_paths = self._gerar_csv(df_tipos, df_top)
            grafico_path = self._gerar_grafico_tipos(df_tipos)
            
            self.logger.info("Relatórios gerados com sucesso!")
            return {
                'csv_path': csv_paths,  # Mantendo compatibilidade com o código existente
                'graficos_path': grafico_path
            }
        except Exception as e:
            self.logger.error(f"Erro fatal na geração de relatórios: {e}", exc_info=True)
            raise

    # --- MÉTODOS PRIVADOS (AUXILIARES) ---

    def _preparar_df_tipos(self, tipos_data: Dict) -> pd.DataFrame:
        """Prepara e limpa o DataFrame de análise por tipo."""
        if not tipos_data:
            self.logger.warning("Dados de 'tipos_analise' estão vazios.")
            return pd.DataFrame()
            
        # Converte para DataFrame e transpõe
        df = pd.DataFrame(tipos_data).T
        
        # Reseta o índice e renomeia
        df = df.reset_index()
        df = df.rename(columns={'index': 'tipo'})
        
        # Reorganiza o DataFrame para ter tipos como índice e estatísticas como colunas
        df = df.melt(id_vars=['tipo'], 
                    var_name='estatistica', 
                    value_name='valor')
        
        # Pivota o DataFrame para ter tipos como índice e estatísticas como colunas
        df = df.pivot(index='tipo', 
                     columns='estatistica', 
                     values='valor')
        
        # Renomeia as colunas para português
        df = df.rename(columns={
            'attack': 'ataque',
            'defense': 'defesa',
            'hp': 'hp'
        })
        
        self.logger.info(f"DataFrame preparado:\n{df}")
        self.logger.info(f"Colunas disponíveis: {df.columns.tolist()}")
        
        return df

    def _preparar_df_top(self, top_data: List) -> pd.DataFrame:
        """Prepara e limpa o DataFrame de Pokémon com mais experiência."""
        if not top_data:
            self.logger.warning("Dados de 'top_experiencia' estão vazios.")
            return pd.DataFrame()

        df = pd.DataFrame(top_data)
        df = df.rename(columns={'nome': 'Nome', 'experiencia_base': 'Experiência Base'})
        df = df.sort_values('Experiência Base', ascending=False)
        return df

    def _gerar_csv(self, df_tipos: pd.DataFrame, df_top: pd.DataFrame) -> Dict[str, str]:
        """Gera arquivos CSV com as análises."""
        try:
            paths = {}
            if not df_tipos.empty:
                path_tipos = os.path.join(self.output_dir, 'analise_tipos.csv')
                df_tipos.to_csv(path_tipos, encoding='utf-8', index=True)
                paths['tipos'] = path_tipos

            if not df_top.empty:
                path_top = os.path.join(self.output_dir, 'top_experiencia.csv')
                df_top.to_csv(path_top, encoding='utf-8', index=False)
                paths['top'] = path_top

            # Retorna um dicionário com os caminhos dos arquivos
            return {
                'tipos': paths.get('tipos', ''),
                'top': paths.get('top', '')
            }
        except Exception as e:
            self.logger.error(f"Erro ao gerar arquivos CSV: {e}", exc_info=True)
            raise

    def _gerar_grafico_tipos(self, df_tipos_original: pd.DataFrame) -> str:
        """Gera um gráfico de barras a partir do DataFrame de tipos."""
        if df_tipos_original.empty:
            self.logger.info("DataFrame de tipos vazio, pulando geração de gráfico.")
            return ""
            
        try:
            # Transpõe o DataFrame para que 'ataque', 'defesa', 'hp' se tornem COLUNAS
            df = df_tipos_original.T
            
            # Log do DataFrame para debug
            self.logger.info(f"DataFrame após transposição:\n{df}")
            self.logger.info(f"Colunas disponíveis: {df.columns.tolist()}")

            plt.style.use('default')
            fig, ax = plt.subplots(figsize=(15, 8))

            tipos = df.index.values
            x = np.arange(len(tipos))
            width = 0.25

            # Plota as barras para cada estatística
            ax.bar(x - width, df['ataque'], width, label='Ataque')
            ax.bar(x, df['defesa'], width, label='Defesa')
            ax.bar(x + width, df['hp'], width, label='HP')

            # Configurações do gráfico
            ax.set_title('Média de Estatísticas por Tipo de Pokémon', fontsize=16, pad=20)
            ax.set_ylabel('Valor Médio', fontsize=12, labelpad=10)
            ax.set_xlabel('Tipos de Pokémon', fontsize=12, labelpad=10)
            ax.set_xticks(x)
            ax.set_xticklabels(tipos, rotation=45, ha="right")
            ax.legend()
            ax.grid(True, axis='y', linestyle='--', alpha=0.6)

            plt.tight_layout()

            # Salva o gráfico
            grafico_path = os.path.join(self.output_dir, 'distribuicao_tipos.png')
            plt.savefig(grafico_path, dpi=300)
            plt.close(fig)

            return grafico_path
        except Exception as e:
            self.logger.error(f"Erro ao gerar gráfico de tipos: {e}\nDataFrame no momento do erro:\n{df.head()}", exc_info=True)
            raise