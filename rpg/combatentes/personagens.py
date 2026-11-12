from abc import ABC

from rpg.combatentes.base import Combatente
from rpg.habilidades.habilidades import Habilidade


class Personagem(Combatente, ABC):
    """Combatente controlado pelo jogador. Possui uma habilidade especial."""

    def __init__(
        self,
        nome: str,
        vida_maxima: int,
        ataque: int,
        defesa: int,
        habilidade: Habilidade,  # injeção de dependência: recebida de fora
    ) -> None:
        super().__init__(nome, vida_maxima, ataque, defesa)
        self._habilidade: Habilidade = habilidade

    @property
    def habilidade(self) -> Habilidade:
        return self._habilidade

    def usar_habilidade(self, alvo: Combatente) -> str:
        """Delega para a habilidade: o Personagem não sabe COMO ela funciona."""
        return self._habilidade.usar(self, alvo)


# Equilíbrio dos atributos (a soma "poder" é parecida, muda o estilo):
#   Guerreiro: muita vida e defesa, ataque médio  -> aguenta, mas bate pouco
#   Mago:      pouca vida e defesa, ataque alto   -> "canhão de vidro"
#   Arqueiro:  tudo intermediário, ataque médio-alto -> versátil

class Guerreiro(Personagem):
    def __init__(self, nome: str, habilidade: Habilidade) -> None:
        super().__init__(nome, 120, 15, 10, habilidade)

    def grito_de_guerra(self) -> str:
        return "Pela glória da batalha!"


class Mago(Personagem):
    def __init__(self, nome: str, habilidade: Habilidade) -> None:
        super().__init__(nome, 70, 25, 3, habilidade)

    def grito_de_guerra(self) -> str:
        return "Sentirão o poder arcano!"


class Arqueiro(Personagem):
    def __init__(self, nome: str, habilidade: Habilidade) -> None:
        super().__init__(nome, 90, 20, 6, habilidade)

    def grito_de_guerra(self) -> str:
        return "Minha flecha nunca erra!"
