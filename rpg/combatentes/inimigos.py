from abc import ABC

from collections.abc import Sequence

from rpg.combatentes.base import Combatente


class Inimigo(Combatente, ABC):
    """Base de todos os inimigos.

    Aberta para extensão (Open/Closed): novos inimigos são novas subclasses.
    O método agir() é o ponto de extensão: a Batalha chama agir() em qualquer
    inimigo, e cada subclasse decide o que fazer (polimorfismo).
    """

    def agir(self, alvos: Sequence[Combatente]) -> str:
        """Comportamento padrão: ataca o alvo com menos vida.

        Subclasses podem sobrescrever (ex.: Chefao). Recebe só alvos vivos.
        Devolve o texto do que aconteceu (sem print).
        """
        return self.atacar(self._escolher_alvo(alvos))

    def _escolher_alvo(self, alvos: Sequence[Combatente]) -> Combatente:
        """Escolhe o alvo mais fraco (menor vida). Em empate, o primeiro."""
        return min(alvos, key=lambda alvo: alvo.vida)


class Goblin(Inimigo):
    """Inimigo simples: vida baixa, ataque médio, defesa baixa."""

    def __init__(self, nome: str) -> None:
        super().__init__(nome, vida_maxima=50, ataque=14, defesa=3)

    def grito_de_guerra(self) -> str:
        return "Grrrr! Dinheiro ou vida!"
