from collections.abc import Callable

from rpg.combatentes.personagens import Personagem

# Apelido de tipo: "uma função que recebe o nome e devolve um Personagem"
Construtor = Callable[[str], Personagem]


class FabricaDePersonagens:
    """Cria personagens a partir do nome da classe (ex.: "Mago").

    Não conhece Guerreiro, Mago nem Arqueiro: ela recebe "receitas" por
    meio de registrar(). Assim, uma classe nova não exige editar esta
    fábrica (Aberto/Fechado).
    """

    def __init__(self) -> None:
        # dicionário: nome da classe -> receita para criá-la
        self._construtores: dict[str, Construtor] = {}

    def registrar(self, tipo: str, construtor: Construtor) -> None:
        """Ensina a fábrica a criar um novo tipo de personagem."""
        self._construtores[tipo] = construtor

    def tipos_disponiveis(self) -> list[str]:
        """Nomes dos tipos registrados, na ordem em que foram registrados."""
        return list(self._construtores)

    def criar(self, tipo: str, nome: str) -> Personagem:
        """Cria uma NOVA instância a cada chamada."""
        if tipo not in self._construtores:
            raise ValueError(f"Tipo de personagem desconhecido: {tipo}")
        return self._construtores[tipo](nome)
