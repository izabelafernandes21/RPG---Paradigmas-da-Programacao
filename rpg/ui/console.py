from typing import Protocol


class Saida(Protocol):
    """Interface pequena: quem sabe mostrar texto."""

    def mostrar(self, texto: str) -> None: ...


class Entrada(Protocol):
    """Interface pequena: quem sabe pedir uma escolha ao jogador."""

    def escolher(self, prompt: str, opcoes: list[str]) -> int: ...


class ConsoleSaida:
    """Implementação de Saida usando print (não herda de Saida: Protocol
    usa 'tipagem estrutural', basta ter o método com a mesma assinatura)."""

    def mostrar(self, texto: str) -> None:
        print(texto)


class ConsoleEntrada:
    """Implementação de Entrada usando input, com validação."""

    def escolher(self, prompt: str, opcoes: list[str]) -> int:
        """Mostra as opções numeradas e devolve o ÍNDICE (começando em 0)."""
        print(prompt)
        for numero, opcao in enumerate(opcoes, start=1):
            print(f"  {numero}) {opcao}")

        while True:  # repete até o jogador digitar algo válido
            texto = input("> ").strip()
            try:
                escolha = int(texto)
            except ValueError:
                print("Digite apenas o número da opção.")
                continue
            if 1 <= escolha <= len(opcoes):
                return escolha - 1
            print(f"Opção inválida. Escolha entre 1 e {len(opcoes)}.")
