from rpg.combatentes.base import Combatente
from rpg.combatentes.inimigos import Goblin
from rpg.combatentes.personagens import Arqueiro, Guerreiro, Mago, Personagem
from rpg.ui.console import ConsoleSaida, Saida


def mostrar_vida(saida: Saida, alvo: Combatente) -> None:
    saida.mostrar(f"  Vida de {alvo.nome}: {alvo.vida}/{alvo.vida_maxima}")


def main(saida: Saida) -> None:
    # Depende da abstração Saida, não de print.
    herois: list[Personagem] = [
        Guerreiro("Thorin"),
        Mago("Merlin"),
        Arqueiro("Robin"),
    ]

    saida.mostrar("=== STATUS ===")
    for combatente in [*herois, Goblin("Grunk")]:
        saida.mostrar(combatente.status())
        saida.mostrar(f'  "{combatente.grito_de_guerra()}"')

    saida.mostrar("\n=== ATAQUES BÁSICOS ===")
    for heroi in herois:
        goblin = Goblin("Grunk")  # goblin novo a cada teste
        saida.mostrar(heroi.atacar(goblin))
        mostrar_vida(saida, goblin)

    saida.mostrar("\n=== HABILIDADES ESPECIAIS ===")
    for heroi in herois:
        goblin = Goblin("Grunk")
        saida.mostrar(heroi.usar_habilidade(goblin))
        mostrar_vida(saida, goblin)


if __name__ == "__main__":
    main(ConsoleSaida())
