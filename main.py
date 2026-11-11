from rpg.batalha import Batalha
from rpg.combatentes.chefao import Chefao
from rpg.combatentes.inimigos import Goblin, Inimigo
from rpg.combatentes.personagens import Arqueiro, Guerreiro, Mago, Personagem
from rpg.ui.console import ConsoleEntrada, ConsoleSaida


def main() -> None:
    # Aqui são criadas as implementações concretas e injetadas na Batalha
    saida = ConsoleSaida()
    entrada = ConsoleEntrada()

    herois: list[Personagem] = [Guerreiro("Thorin"), Mago("Merlin"), Arqueiro("Robin")]
    inimigos: list[Inimigo] = [Goblin("Grunk"), Chefao("Ogro Rei")]

    Batalha(herois, inimigos, saida, entrada).executar()


if __name__ == "__main__":
    main()
