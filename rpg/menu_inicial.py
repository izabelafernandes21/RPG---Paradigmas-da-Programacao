from rpg.combatentes.personagens import Personagem
from rpg.fabricas import FabricaDePersonagens
from rpg.ui.console import Entrada, LeitorDeTexto, Saida


class MenuInicial:
    """Conversa com o jogador para montar o grupo de heróis.

    Não cria personagens (isso é da fábrica) e não usa print/input
    (isso é da Saida, Entrada e LeitorDeTexto): só conduz o diálogo.
    """

    TAMANHO_GRUPO: int = 3  # constante de classe: quantos heróis no grupo

    def __init__(
        self,
        fabrica: FabricaDePersonagens,
        saida: Saida,
        entrada: Entrada,
        leitor: LeitorDeTexto,
    ) -> None:
        self._fabrica: FabricaDePersonagens = fabrica
        self._saida: Saida = saida
        self._entrada: Entrada = entrada
        self._leitor: LeitorDeTexto = leitor

    def executar(self) -> list[Personagem] | None:
        """Mostra o menu principal. Devolve o grupo montado, ou None se o
        jogador escolher sair."""
        self._saida.mostrar("=====================================")
        self._saida.mostrar("            RPG EM CONSOLE")
        self._saida.mostrar("=====================================")
        indice = self._entrada.escolher("Menu principal:", ["Novo jogo", "Sair"])
        if indice == 1:  # índice 1 = "Sair"
            return None
        return self._montar_grupo()

    def _montar_grupo(self) -> list[Personagem]:
        self._saida.mostrar(f"\nMonte seu grupo de {self.TAMANHO_GRUPO} heróis.")
        grupo: list[Personagem] = []
        for numero in range(1, self.TAMANHO_GRUPO + 1):
            tipo = self._escolher_tipo(numero)
            nome = self._pedir_nome(numero, [heroi.nome for heroi in grupo])
            grupo.append(self._fabrica.criar(tipo, nome))
            self._saida.mostrar(f"{nome} entrou para o grupo!\n")
        return grupo

    def _escolher_tipo(self, numero: int) -> str:
        tipos = self._fabrica.tipos_disponiveis()
        descricoes = [self._descrever(tipo) for tipo in tipos]
        indice = self._entrada.escolher(
            f"Herói {numero}: escolha a classe:", descricoes
        )
        return tipos[indice]

    def _descrever(self, tipo: str) -> str:
        """Texto do menu. Cria um personagem descartável só para ler os
        atributos, assim os números nunca ficam desatualizados."""
        exemplo = self._fabrica.criar(tipo, "exemplo")
        return (
            f"{tipo} (Vida {exemplo.vida_maxima}, Ataque {exemplo.ataque}, "
            f"Defesa {exemplo.defesa}, Habilidade: {exemplo.habilidade.nome})"
        )

    def _pedir_nome(self, numero: int, nomes_usados: list[str]) -> str:
        """Pede o nome até ser diferente dos já usados (evita confusão
        no menu 'Usar em quem?' da Batalha)."""
        while True:
            nome = self._leitor.ler_texto(f"Nome do herói {numero}:")
            if nome in nomes_usados:
                self._saida.mostrar("Esse nome já está em uso. Escolha outro.")
                continue
            return nome
