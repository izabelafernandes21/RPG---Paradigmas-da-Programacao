from collections.abc import Callable, Sequence

from rpg.combatentes.base import Combatente
from rpg.combatentes.inimigos import Inimigo
from rpg.combatentes.personagens import Personagem
from rpg.ui.console import Entrada, Saida
from rpg.itens.inventario import Inventario


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
        inventario: Inventario,
        saida: Saida,
        entrada: Entrada,
    ) -> None:
        self._herois: list[Personagem] = herois
        self._inimigos: list[Inimigo] = inimigos
        self._inventario: Inventario = inventario
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
        # Lista de (texto do menu, método que executa a ação). Cada método
        # recebe o herói, faz suas próprias perguntas, mostra o resultado e
        # devolve True se a ação foi realizada (False = o jogador voltou
        # atrás, então o menu é mostrado de novo).
        acoes: list[tuple[str, Callable[[Personagem], bool]]] = [
            ("Atacar", self._acao_atacar),
            (f"Usar {heroi.habilidade.nome}", self._acao_habilidade),
            ("Usar item", self._acao_usar_item),
            ("Equipar item", self._acao_equipar_item),
        ]
        opcoes = [nome for nome, _ in acoes]
        while True:
            indice = self._entrada.escolher(
                f"Vez de {heroi.nome}. O que fazer?", opcoes
            )
            _, executar = acoes[indice]
            if executar(heroi):
                break

    # ---------- Ações do herói ----------
    def _acao_atacar(self, heroi: Personagem) -> bool:
        return self._agir_contra_inimigo(heroi.atacar)

    def _acao_habilidade(self, heroi: Personagem) -> bool:
        return self._agir_contra_inimigo(heroi.usar_habilidade)

    def _agir_contra_inimigo(self, executar: Callable[[Combatente], str]) -> bool:
        """Parte comum de atacar e usar habilidade (era o corpo antigo)."""
        alvo = self._escolher_alvo()
        vivos_antes = self._vivos(self._inimigos)  # foto antes da ação
        self._saida.mostrar(executar(alvo))
        self._anunciar_derrotas(vivos_antes)
        return True

    def _acao_usar_item(self, heroi: Personagem) -> bool:
        itens = self._inventario.usaveis
        if not itens:
            self._saida.mostrar("Não há itens para usar.")
            return False
        rotulos = [f"{i.nome} ({i.descricao})" for i in itens] + ["Voltar"]
        indice = self._entrada.escolher("Usar qual item?", rotulos)
        if indice == len(itens):  # a última opção é "Voltar"
            return False
        item = itens[indice]
        alvo = self._escolher_aliado("Usar em quem?")
        self._saida.mostrar(f"{heroi.nome} usa {item.nome} em {alvo.nome}.")
        self._saida.mostrar(item.usar(alvo))
        self._inventario.remover_usavel(item)  # a poção é consumida
        return True

    def _acao_equipar_item(self, heroi: Personagem) -> bool:
        itens = self._inventario.equipaveis
        if not itens:
            self._saida.mostrar("Não há equipamentos para equipar.")
            return False
        rotulos = [f"{i.nome} ({i.descricao})" for i in itens] + ["Voltar"]
        indice = self._entrada.escolher("Equipar qual item?", rotulos)
        if indice == len(itens):
            return False
        item = itens[indice]
        alvo = self._escolher_aliado("Equipar em quem?")
        self._saida.mostrar(f"{heroi.nome} equipa {item.nome} em {alvo.nome}.")
        self._saida.mostrar(item.equipar(alvo))
        self._inventario.remover_equipavel(item)  # sai do inventário
        return True

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

    def _escolher_aliado(self, pergunta: str) -> Combatente:
        """Pergunta qual herói vivo recebe o item. Se só há um, nem pergunta."""
        vivos = self._vivos(self._herois)
        if len(vivos) == 1:
            return vivos[0]
        nomes = [f"{h.nome} ({h.vida}/{h.vida_maxima})" for h in vivos]
        return vivos[self._entrada.escolher(pergunta, nomes)]

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
