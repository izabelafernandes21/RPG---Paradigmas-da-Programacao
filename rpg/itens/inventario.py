from rpg.itens.itens import Equipavel, Usavel


class Inventario:
    """Guarda os itens do grupo. Só guarda e entrega: não sabe o que um
    item faz (isso é do próprio item) nem mostra nada na tela.

    Há duas listas porque um item pode ser Usavel, Equipavel ou os dois.
    Assim não precisamos de isinstance para descobrir o tipo de cada um.
    """

    def __init__(self) -> None:
        self._usaveis: list[Usavel] = []
        self._equipaveis: list[Equipavel] = []

    # Propriedades devolvem uma CÓPIA: quem recebe não altera a lista interna
    @property
    def usaveis(self) -> list[Usavel]:
        return list(self._usaveis)

    @property
    def equipaveis(self) -> list[Equipavel]:
        return list(self._equipaveis)

    def adicionar_usavel(self, item: Usavel) -> None:
        self._usaveis.append(item)

    def adicionar_equipavel(self, item: Equipavel) -> None:
        self._equipaveis.append(item)

    def remover_usavel(self, item: Usavel) -> None:
        self._usaveis.remove(item)

    def remover_equipavel(self, item: Equipavel) -> None:
        self._equipaveis.remove(item)
