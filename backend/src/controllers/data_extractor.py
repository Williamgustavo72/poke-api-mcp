import logging
import aiohttp
import asyncio
import pandas as pd
from typing import List, Dict
from models.pokemon import Pokemon
import json
import os
from datetime import datetime, timedelta

class DataExtractor:
    def __init__(self):
        self.base_url = "https://pokeapi.co/api/v2"
        self.logger = logging.getLogger(__name__)
        self.cache_dir = "cache"
        self.cache_expiry = timedelta(hours=24)
        
        # Cria diretório de cache se não existir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        
    async def extract(self, limit: int = 100, offset: int = 0) -> Dict:
        """
        Extrai dados dos Pokémon da PokeAPI.
        
        Args:
            limit: Quantidade de Pokémon para extrair
            offset: Deslocamento para paginação
            
        Returns:
            Dicionário com dados dos Pokémon em formato JSON
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Obtém lista inicial de Pokémon
                pokemon_list = await self._get_pokemon_list(session, limit, offset)
                pokemon_data = []
                
                # Cria tasks para buscar detalhes de cada Pokémon
                tasks = []
                for pokemon in pokemon_list['results']:
                    tasks.append(self._get_pokemon_details(session, pokemon['url']))
                
                # Executa todas as requisições em paralelo
                details_list = await asyncio.gather(*tasks)
                
                # Processa os detalhes
                for details in details_list:
                    pokemon = self._create_pokemon_object(details)
                    pokemon_data.append(self._pokemon_to_dict(pokemon))
                
                return {
                    "status": "success",
                    "total": len(pokemon_data),
                    "limit": limit,
                    "offset": offset,
                    "data": pokemon_data
                }
                
        except Exception as e:
            self.logger.error(f"Erro na extração de dados: {str(e)}")
            return {
                "status": "error",
                "message": str(e),
                "data": []
            }
            
    async def _get_pokemon_list(self, session: aiohttp.ClientSession, limit: int, offset: int) -> Dict:
        """Obtém lista de Pokémon da API."""
        cache_key = f"pokemon_list_{limit}_{offset}"
        cached_data = self._get_from_cache(cache_key)
        
        if cached_data:
            return cached_data
            
        async with session.get(f"{self.base_url}/pokemon?limit={limit}&offset={offset}") as response:
            response.raise_for_status()
            data = await response.json()
            self._save_to_cache(cache_key, data)
            return data
        
    async def _get_pokemon_details(self, session: aiohttp.ClientSession, url: str) -> Dict:
        """Obtém detalhes de um Pokémon específico."""
        # Extrai o ID do Pokémon da URL
        pokemon_id = url.split('/')[-2]
        cache_key = f"pokemon_details_{pokemon_id}"
        
        # Verifica cache
        cached_data = self._get_from_cache(cache_key)
        if cached_data:
            return cached_data
            
        # Se não estiver em cache, faz a requisição
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()
            self._save_to_cache(cache_key, data)
            return data
        
    def _create_pokemon_object(self, data: Dict) -> Pokemon:
        """Cria objeto Pokemon a partir dos dados da API."""
        return Pokemon(
            id=data['id'],
            nome=data['name'],
            experiencia_base=data['base_experience'],
            tipos=[t['type']['name'] for t in data['types']],
            hp=next(s['base_stat'] for s in data['stats'] if s['stat']['name'] == 'hp'),
            ataque=next(s['base_stat'] for s in data['stats'] if s['stat']['name'] == 'attack'),
            defesa=next(s['base_stat'] for s in data['stats'] if s['stat']['name'] == 'defense')
        )
        
    def _pokemon_to_dict(self, pokemon: Pokemon) -> Dict:
        """Converte objeto Pokemon para dicionário."""
        return {
            "id": pokemon.id,
            "nome": pokemon.nome,
            "experiencia_base": pokemon.experiencia_base,
            "tipos": pokemon.tipos,
            "hp": pokemon.hp,
            "ataque": pokemon.ataque,
            "defesa": pokemon.defesa,
            "categoria": pokemon.categoria
        }
        
    def _get_from_cache(self, key: str) -> Dict:
        """Recupera dados do cache."""
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        
        if os.path.exists(cache_file):
            # Verifica se o cache expirou
            file_time = datetime.fromtimestamp(os.path.getmtime(cache_file))
            if datetime.now() - file_time < self.cache_expiry:
                with open(cache_file, 'r') as f:
                    return json.load(f)
        return None
        
    def _save_to_cache(self, key: str, data: Dict):
        """Salva dados no cache."""
        cache_file = os.path.join(self.cache_dir, f"{key}.json")
        with open(cache_file, 'w') as f:
            json.dump(data, f) 