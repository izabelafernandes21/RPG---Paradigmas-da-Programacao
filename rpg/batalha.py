from collections.abc import Callable, Sequence

from rpg.combatentes.base import Combatente
from rpg.combatentes.inimigos import Inimigo
from rpg.combatentes.personagens import Personagem
from rpg.ui.console import Entrada, Saida


class Batalha:
    """Orquestra os turnos entre heróis e inimigos.

    Só coordena: quem sabe atacar são os Combatentes, quem sabe mostrar
    texto é a Saida e quem sabe pedir escolhas é a Entrada.
    Tudo chega pelo construtor (injeção de dependência).
    """

    def __init__(
        self,
        herois: list[Personagem],
        inimigos: list[Inimigo],
        saida: Saida,
        entrada: Entrada,
    ) -> None:
        self._herois: list[Personagem] = herois
        self._inimigos: list[Inimigo] = inimigos
        self._saida: Saida = saida
        self._entrada: Entrada = entrada
        self._rodada: int = 0

    # ---------- Fluxo principal ----------
    def executar(self) -> bool:
        """Roda a batalha até um lado cair. Devolve True se os heróis venceram."""
        self._saida.mostrar("=== A BATALHA COMEÇA! ===")
        for inimigo in self._inimigos:
            self._saida.mostrar(f'{inimigo.nome}: "{inimigo.grito_de_guerra()}"')

        while self._vivos(self._herois) and self._vivos(self._inimigos):
            self._rodada += 1
            self._mostrar_status()
            self._turno_dos_herois()
            # Se todos os inimigos já caíram, eles não contra-atacam
            if self._vivos(self._inimigos):
                self._turno_dos_inimigos()

        venceu = bool(self._vivos(self._herois))
        if venceu:
            self._saida.mostrar(
                f"\n=== VITÓRIA! Os heróis venceram em {self._rodada} rodadas. ==="
            )
        else:
            self._saida.mostrar("\n=== DERROTA... Todos os heróis caíram. ===")
        return venceu

    # ---------- Turnos ----------
    def _turno_dos_herois(self) -> None:
        self._saida.mostrar("--- Turno dos heróis ---")
        for heroi in self._herois:
            if not heroi.esta_vivo():
                continue  # herói morto não age
            if not self._vivos(self._inimigos):
                break  # inimigos acabaram: o turno termina
            self._turno_do_heroi(heroi)

    def _turno_do_heroi(self, heroi: Personagem) -> None:
        # Lista de (texto do menu, função a executar). Cada função recebe o
        # alvo e devolve o texto. Para ganhar uma nova opção (ex.: usar item),
        # basta adicionar um item nesta lista, sem mexer no resto.
        acoes: list[tuple[str, Callable[[Combatente], str]]] = [
            ("Atacar", heroi.atacar),
            (f"Usar {heroi.habilidade.nome}", heroi.usar_habilidade),
        ]
        opcoes = [nome for nome, _ in acoes]
        indice = self._entrada.escolher(f"Vez de {heroi.nome}. O que fazer?", opcoes)
        _, executar = acoes[indice]

        alvo = self._escolher_alvo()
        vivos_antes = self._vivos(self._inimigos)  # foto antes da ação
        self._saida.mostrar(executar(alvo))
        self._anunciar_derrotas(vivos_antes)

    def _turno_dos_inimigos(self) -> None:
        self._saida.mostrar("--- Turno dos inimigos ---")
        for inimigo in self._inimigos:
            if not inimigo.esta_vivo():
                continue
            herois_vivos = self._vivos(self._herois)
            if not herois_vivos:
                break
            # A Batalha NÃO sabe se é Goblin ou Chefao: só chama agir()
            self._saida.mostrar(inimigo.agir(herois_vivos))
            self._anunciar_derrotas(herois_vivos)

    # ---------- Auxiliares ----------
    def _escolher_alvo(self) -> Combatente:
        """Pergunta o alvo. Se só há um inimigo vivo, nem pergunta."""
        vivos = self._vivos(self._inimigos)
        if len(vivos) == 1:
            return vivos[0]
        indice = self._entrada.escolher("Escolha o alvo:", [v.nome for v in vivos])
        return vivos[indice]

    def _mostrar_status(self) -> None:
        self._saida.mostrar(f"\n=== RODADA {self._rodada} ===")
        self._saida.mostrar("Heróis:")
        for heroi in self._vivos(self._herois):
            self._saida.mostrar(f"  {heroi.status()}")
        self._saida.mostrar("Inimigos:")
        for inimigo in self._vivos(self._inimigos):
            self._saida.mostrar(f"  {inimigo.status()}")

    def _anunciar_derrotas(self, vivos_antes: Sequence[Combatente]) -> None:
        """Quem estava vivo antes e agora não está acabou de ser derrotado."""
        for combatente in vivos_antes:
            if not combatente.esta_vivo():
                self._saida.mostrar(f"{combatente.nome} foi derrotado!")

    @staticmethod
    def _vivos(grupo: Sequence[Combatente]) -> list[Combatente]:
        """Filtra apenas os combatentes que ainda estão vivos."""
        return [c for c in grupo if c.esta_vivo()]
