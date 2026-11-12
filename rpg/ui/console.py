from typing import Protocol


class Saida(Protocol):
    """Interface pequena: quem sabe mostrar texto."""

    def mostrar(self, texto: str) -> None: ...


class Entrada(Protocol):
    """Interface pequena: quem sabe pedir uma escolha ao jogador."""

    def escolher(self, prompt: str, opcoes: list[str]) -> int: ...

class LeitorDeTexto(Protocol):
    """Interface pequena: quem sabe ler um texto livre (ex.: um nome).

    É separada de Entrada de propósito: a Batalha só precisa de escolhas
    numéricas e não deve ser obrigada a conhecer leitura de texto.
    """

    def ler_texto(self, prompt: str) -> str: ...


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

    def ler_texto(self, prompt: str) -> str:
        """Pede um texto e repete até o jogador digitar algo não vazio."""
        while True:
            texto = input(f"{prompt} ").strip()
            if texto:
                return texto
            print("O texto não pode ser vazio.")
