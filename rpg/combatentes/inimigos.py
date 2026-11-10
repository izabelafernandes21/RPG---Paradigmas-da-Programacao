from abc import ABC

from rpg.combatentes.base import Combatente


class Inimigo(Combatente, ABC):
    """Base de todos os inimigos.

    Aberta para extensão (Open/Closed): para criar um Chefao, basta fazer
    `class Chefao(Inimigo)` em outro arquivo ou aqui, sem mexer em nada
    que já existe. Continua abstrata porque não implementa grito_de_guerra().
    """


class Goblin(Inimigo):
    """Inimigo simples: vida baixa, ataque médio, defesa baixa."""

    def __init__(self, nome: str) -> None:
        super().__init__(nome, vida_maxima=50, ataque=14, defesa=3)

    def grito_de_guerra(self) -> str:
        return "Grrrr! Dinheiro ou vida!"
