from rpg.batalha import Batalha
from rpg.combatentes.chefao import Chefao
from rpg.combatentes.inimigos import Goblin, Inimigo
from rpg.combatentes.personagens import Arqueiro, Guerreiro, Mago, Personagem
from rpg.ui.console import ConsoleEntrada, ConsoleSaida
from rpg.itens.inventario import Inventario
from rpg.itens.itens import Equipamento, Pocao


def main() -> None:
    # Aqui são criadas as implementações concretas e injetadas na Batalha
    saida = ConsoleSaida()
    entrada = ConsoleEntrada()

    herois: list[Personagem] = [Guerreiro("Thorin"), Mago("Merlin"), Arqueiro("Robin")]
    inimigos: list[Inimigo] = [Goblin("Grunk"), Chefao("Ogro Rei")]

        # Inventário compartilhado pelo grupo
    inventario = Inventario()
    inventario.adicionar_usavel(Pocao("Poção de Cura", cura=40))
    inventario.adicionar_usavel(Pocao("Poção Grande", cura=80))
    inventario.adicionar_equipavel(Equipamento("Espada de Aço", bonus_ataque=8))
    inventario.adicionar_equipavel(Equipamento("Escudo de Ferro", bonus_defesa=5))

    Batalha(herois, inimigos, inventario, saida, entrada).executar()


if __name__ == "__main__":
    main()
