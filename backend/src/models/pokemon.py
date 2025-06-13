from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Pokemon:
    id: int
    nome: str
    experiencia_base: int
    tipos: List[str]
    hp: int
    ataque: int
    defesa: int
    categoria: Optional[str] = None

    def __post_init__(self):
        # Normaliza o nome para título
        self.nome = self.nome.title()
        
        # Categoriza o Pokémon baseado na experiência
        if self.categoria is None:
            if self.experiencia_base < 50:
                self.categoria = "Fraco"
            elif self.experiencia_base <= 100:
                self.categoria = "Médio"
            else:
                self.categoria = "Forte" 