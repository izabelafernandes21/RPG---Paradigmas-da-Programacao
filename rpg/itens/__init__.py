from __future__ import annotations  # type hints viram texto, avaliados só depois

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Protocol

# Mesmo truque das habilidades: o import só existe para o verificador de tipos
if TYPE_CHECKING:
    from rpg.combatentes.base import Combatente


# ---------- Interfaces pequenas (Interface Segregation) ----------
class Usavel(Protocol):
    """Quem pode ser USADO em um combatente (ex.: poção)."""

    @property
    def nome(self) -> str: ...

    @property
    def descricao(self) -> str: ...

    def usar(self, alvo: Combatente) -> str: ...


class Equipavel(Protocol):
    """Quem pode ser EQUIPADO por um combatente (ex.: espada)."""

    @property
    def nome(self) -> str: ...

    @property
    def descricao(self) -> str: ...

    def equipar(self, portador: Combatente) -> str: ...


# ---------- Base comum dos itens ----------
class Item(ABC):
    """Abstração de item: todo item tem nome e uma descrição do seu efeito."""

    def __init__(self, nome: str) -> None:
        self._nome: str = nome

    @property
    def nome(self) -> str:
        return self._nome

    @property
    @abstractmethod
    def descricao(self) -> str:
        """Resumo do efeito, mostrado no menu. Cada item escreve o seu."""


class Pocao(Item):
    """Item de cura. Cumpre o contrato de Usavel (tem o método usar)."""

    def __init__(self, nome: str, cura: int) -> None:
        super().__init__(nome)
        self._cura: int = cura

    @property
    def descricao(self) -> str:
        return f"cura {self._cura}"

    def usar(self, alvo: Combatente) -> str:
        vida_antes = alvo.vida
        alvo.curar(self._cura)  # curar() já respeita a vida máxima
        recuperado = alvo.vida - vida_antes  # quanto realmente foi curado
        return f"{alvo.nome} recupera {recuperado} de vida."


class Equipamento(Item):
    """Item que dá bônus permanentes. Cumpre o contrato de Equipavel."""

    def __init__(
        self, nome: str, bonus_ataque: int = 0, bonus_defesa: int = 0
    ) -> None:
        super().__init__(nome)
        self._bonus_ataque: int = bonus_ataque
        self._bonus_defesa: int = bonus_defesa

    @property
    def descricao(self) -> str:
        partes: list[str] = []
        if self._bonus_ataque:
            partes.append(f"+{self._bonus_ataque} ataque")
        if self._bonus_defesa:
            partes.append(f"+{self._bonus_defesa} defesa")
        return ", ".join(partes)

    def equipar(self, portador: Combatente) -> str:
        # Não mexe em _ataque/_defesa direto: usa o método controlado
        portador.aplicar_bonus(self._bonus_ataque, self._bonus_defesa)
        return f"{portador.nome} ganha {self.descricao}."
