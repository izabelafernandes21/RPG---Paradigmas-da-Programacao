from abc import ABC, abstractmethod


class Combatente(ABC):
    """Classe abstrata: tudo que luta (personagem ou inimigo) é um Combatente."""

    def __init__(self, nome: str, vida_maxima: int, ataque: int, defesa: int) -> None:
        # Atributos privados (prefixo _): só mudam por métodos da própria classe.
        self._nome: str = nome
        self._vida_maxima: int = vida_maxima
        self._vida: int = vida_maxima  # começa com a vida cheia
        self._ataque: int = ataque
        self._defesa: int = defesa

    # ---------- Propriedades (somente leitura: não há setter) ----------
    @property
    def nome(self) -> str:
        return self._nome

    @property
    def vida(self) -> int:
        return self._vida

    @property
    def vida_maxima(self) -> int:
        return self._vida_maxima

    @property
    def ataque(self) -> int:
        return self._ataque

    @property
    def defesa(self) -> int:
        return self._defesa

    # ---------- Comportamentos comuns a todos ----------
    def esta_vivo(self) -> bool:
        """Retorna True enquanto a vida for maior que zero."""
        return self._vida > 0

    def receber_dano(self, dano: int, ignorar_defesa: bool = False) -> int:
        """Aplica o dano e devolve o dano final realmente causado.

        Regra: dano final = max(1, dano - defesa). Sempre causa pelo menos 1.
        Se ignorar_defesa=True (ex.: magia), a defesa não é descontada.
        """
        reducao = 0 if ignorar_defesa else self._defesa
        dano_final = max(1, dano - reducao)
        # max(0, ...) garante que a vida nunca fique negativa
        self._vida = max(0, self._vida - dano_final)
        return dano_final

    def curar(self, quantidade: int) -> None:
        """Recupera vida, sem ultrapassar a vida máxima."""
        self._vida = min(self._vida_maxima, self._vida + quantidade)

    def aplicar_bonus(self, ataque: int = 0, defesa: int = 0) -> None:
        """Soma bônus (ex.: de equipamentos) aos atributos.

        É o ÚNICO jeito de alterar ataque e defesa de fora da classe,
        e ele garante a regra: os valores nunca ficam negativos.
        """
        self._ataque = max(0, self._ataque + ataque)
        self._defesa = max(0, self._defesa + defesa)

    def atacar(self, alvo: "Combatente") -> str:
        """Ataque básico. Devolve o texto do que aconteceu (sem print)."""
        dano = alvo.receber_dano(self._ataque)
        return f"{self._nome} ataca {alvo.nome} e causa {dano} de dano."

    def status(self) -> str:
        """Linha de status pronta para ser exibida pela interface."""
        return (
            f"{type(self).__name__} {self._nome} | "
            f"Vida: {self._vida}/{self._vida_maxima} | "
            f"Ataque: {self._ataque} | Defesa: {self._defesa}"
        )

    # ---------- Método abstrato: cada subclasse DEVE implementar ----------
    @abstractmethod
    def grito_de_guerra(self) -> str:
        """Frase característica do combatente (comportamento próprio)."""
