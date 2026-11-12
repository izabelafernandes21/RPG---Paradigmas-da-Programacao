from rpg.batalha import Batalha
from rpg.combatentes.chefao import Chefao
from rpg.combatentes.inimigos import Goblin, Inimigo
from rpg.combatentes.personagens import Arqueiro, Guerreiro, Mago
from rpg.fabricas import FabricaDePersonagens
from rpg.habilidades.habilidades import BolaDeFogo, GolpePoderoso, TiroDuplo
from rpg.itens.inventario import Inventario
from rpg.itens.itens import Equipamento, Pocao
from rpg.menu_inicial import MenuInicial
from rpg.ui.console import ConsoleEntrada, ConsoleSaida


def criar_fabrica() -> FabricaDePersonagens:
    """Registra as classes jogáveis e qual habilidade cada uma recebe.
    A ordem aqui é a ordem em que aparecem no menu."""
    fabrica = FabricaDePersonagens()
    # lambda nome: ... é uma mini-função que recebe o nome e monta o herói
    fabrica.registrar("Guerreiro", lambda nome: Guerreiro(nome, GolpePoderoso()))
    fabrica.registrar("Mago", lambda nome: Mago(nome, BolaDeFogo()))
    fabrica.registrar("Arqueiro", lambda nome: Arqueiro(nome, TiroDuplo()))
    return fabrica


def criar_inventario() -> Inventario:
    """Inventário inicial compartilhado pelo grupo."""
    inventario = Inventario()
    inventario.adicionar_usavel(Pocao("Poção de Cura", cura=40))
    inventario.adicionar_usavel(Pocao("Poção Grande", cura=80))
    inventario.adicionar_equipavel(Equipamento("Espada de Aço", bonus_ataque=8))
    inventario.adicionar_equipavel(Equipamento("Escudo de Ferro", bonus_defesa=5))
    return inventario


def main() -> None:
    # Único lugar que conhece as classes concretas e as liga umas às outras
    saida = ConsoleSaida()
    entrada = ConsoleEntrada()

    # 'entrada' é passada duas vezes: o mesmo objeto cumpre os Protocols
    # Entrada (escolher) e LeitorDeTexto (ler_texto)
    menu = MenuInicial(criar_fabrica(), saida, entrada, entrada)
    herois = menu.executar()
    if herois is None:  # o jogador escolheu "Sair"
        saida.mostrar("Até a próxima!")
        return

    inimigos: list[Inimigo] = [Goblin("Grunk"), Chefao("Ogro Rei", GolpePoderoso())]
    Batalha(herois, inimigos, criar_inventario(), saida, entrada).executar()


if __name__ == "__main__":
    main()
