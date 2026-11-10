from __future__ import annotations  # type hints viram texto, avaliados só depois

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Este import só existe para o verificador de tipos (mypy/IDE).
# Em tempo de execução ele é ignorado, então não há import circular.
if TYPE_CHECKING:
    from rpg.combatentes.base import Combatente


class Habilidade(ABC):
    """Contrato de toda habilidade especial."""

    def __init__(self, nome: str) -> None:
        self._nome: str = nome

    @property
    def nome(self) -> str:
        return self._nome

    @abstractmethod
    def usar(self, usuario: Combatente, alvo: Combatente) -> str:
        """Executa a habilidade e devolve o texto do resultado."""


class GolpePoderoso(Habilidade):
    """Causa o dobro do ataque do usuário (a defesa do alvo ainda conta)."""

    def __init__(self) -> None:
        super().__init__("Golpe Poderoso")

    def usar(self, usuario: Combatente, alvo: Combatente) -> str:
        dano = alvo.receber_dano(usuario.ataque * 2)
        return f"{usuario.nome} usa {self.nome} em {alvo.nome} e causa {dano} de dano!"


class BolaDeFogo(Habilidade):
    """Dano mágico: ignora a defesa do alvo."""

    def __init__(self) -> None:
        super().__init__("Bola de Fogo")

    def usar(self, usuario: Combatente, alvo: Combatente) -> str:
        dano = alvo.receber_dano(usuario.ataque, ignorar_defesa=True)
        return (
            f"{usuario.nome} lança {self.nome} em {alvo.nome} "
            f"e causa {dano} de dano mágico (ignora defesa)!"
        )


class TiroDuplo(Habilidade):
    """Ataca duas vezes seguidas, reaproveitando o ataque básico."""

    def __init__(self) -> None:
        super().__init__("Tiro Duplo")

    def usar(self, usuario: Combatente, alvo: Combatente) -> str:
        linhas = [f"{usuario.nome} usa {self.nome}!"]
        for _ in range(2):
            if alvo.esta_vivo():  # se o alvo morreu no 1º tiro, não atira de novo
                linhas.append(usuario.atacar(alvo))
        return "\n".join(linhas)
