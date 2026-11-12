from collections.abc import Sequence

from rpg.combatentes.base import Combatente
from rpg.combatentes.inimigos import Inimigo
from rpg.habilidades.habilidades import Habilidade


class Chefao(Inimigo):
    """Inimigo forte: ataca normalmente, mas a cada 3 ações usa uma habilidade.

    Criado em um arquivo novo, sem alterar Goblin, Combatente, Habilidade
    nem Batalha. Isso é o princípio Aberto/Fechado na prática.
    """

    INTERVALO_ESPECIAL: int = 3  # constante de classe: a cada quantas ações

       def __init__(self, nome: str, habilidade: Habilidade) -> None:
        super().__init__(nome, vida_maxima=120, ataque=20, defesa=6)
        # Habilidade injetada de fora, igual ao Personagem
        self._habilidade: Habilidade = habilidade
        self._acoes_realizadas: int = 0  # contador privado de ações

    def agir(self, alvos: Sequence[Combatente]) -> str:
        """Sobrescreve o comportamento padrão com o ataque especial periódico."""
        self._acoes_realizadas += 1
        alvo = self._escolher_alvo(alvos)

        # % é o resto da divisão: 3, 6, 9... dão resto 0
        if self._acoes_realizadas % self.INTERVALO_ESPECIAL == 0:
            return (
                f"{self.nome} ruge e concentra toda a sua força!\n"
                + self._habilidade.usar(self, alvo)
            )
        return self.atacar(alvo)

    def grito_de_guerra(self) -> str:
        return "Tremei diante do Rei Ogro!"
