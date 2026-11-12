# RPG em Console

Aplicação de RPG por turnos em modo console, desenvolvida em Python para a disciplina de **Paradigmas da Programação**. O objetivo do projeto é praticar os conceitos fundamentais de **Programação Orientada a Objetos** (abstração, encapsulamento, herança e polimorfismo) e os **cinco princípios SOLID**.

## Sumário

1. [Sobre o jogo](#1-sobre-o-jogo)
2. [Requisitos](#2-requisitos)
3. [Como executar](#3-como-executar)
4. [Como jogar](#4-como-jogar)
5. [Estrutura do projeto](#5-estrutura-do-projeto)
6. [Princípios SOLID aplicados](#6-princípios-solid-aplicados)
7. [Conceitos de POO utilizados](#7-conceitos-de-poo-utilizados)
8. [Como estender o jogo](#8-como-estender-o-jogo)

---

## 1. Sobre o jogo

O jogador monta um grupo de **3 heróis** e enfrenta dois inimigos em uma batalha por turnos: o **Goblin Grunk** e o chefão **Ogro Rei**.

| Classe | Vida | Ataque | Defesa | Habilidade | Efeito da habilidade |
|---|---|---|---|---|---|
| Guerreiro | 120 | 15 | 10 | Golpe Poderoso | Causa o dobro do ataque (a defesa do alvo ainda conta) |
| Mago | 70 | 25 | 3 | Bola de Fogo | Dano mágico que **ignora** a defesa do alvo |
| Arqueiro | 90 | 20 | 6 | Tiro Duplo | Ataca duas vezes seguidas |

**Regra de dano:** `dano final = max(1, dano - defesa)`. Todo golpe causa pelo menos 1 de dano.

**Inimigos:**

- **Goblin** (Vida 50, Ataque 14, Defesa 3): ataca sempre o herói com menos vida.
- **Ogro Rei** (Vida 120, Ataque 20, Defesa 6): ataca normalmente, mas a cada 3 ações usa uma habilidade especial.

**Inventário compartilhado do grupo:**

- Poção de Cura (cura 40) e Poção Grande (cura 80): consumidas ao usar.
- Espada de Aço (+8 ataque) e Escudo de Ferro (+5 defesa): bônus permanentes.

---

## 2. Requisitos

- **Python 3.10 ou superior** (o código usa a sintaxe `list[X] | None` e `Protocol`).
- Nenhuma biblioteca externa: apenas a biblioteca padrão. **Não há dependências a instalar.**


## 3. Como executar

Python é uma linguagem interpretada, então **não há etapa de compilação separada**: basta executar o arquivo `main.py`.

### 3.1 Clonar o repositório

```bash
git clone https://github.com/izabelafernandes21/RPG---Paradigmas-da-Programacao.git
cd RPG---Paradigmas-da-Programacao
```

### 3.2 Solução de problemas

| Problema | Causa provável | Solução |
|---|---|---|
| `ModuleNotFoundError: No module named 'rpg'` | Comando executado fora da pasta raiz | Entre na pasta do projeto e rode `python main.py` |
| `SyntaxError` ou erro em anotações de tipo | Python anterior à versão 3.10 | Atualize o Python |
| `python: command not found` | Em Linux/macOS o comando costuma ser `python3` | Use `python3 main.py` |

---

## 4. Como jogar

1. No **menu principal**, escolha `1) Novo jogo`.
2. Para cada um dos 3 heróis, escolha a **classe** e digite um **nome** (os nomes não podem se repetir).
3. Na batalha, a cada rodada os heróis agem primeiro e depois os inimigos. No turno de cada herói, escolha:
   - **Atacar**: ataque básico em um inimigo.
   - **Usar habilidade**: habilidade especial da classe.
   - **Usar item**: consome uma poção em um aliado.
   - **Equipar item**: aplica um equipamento em um aliado.
4. Todas as escolhas são feitas **digitando o número** da opção e pressionando Enter. Entradas inválidas são recusadas e a pergunta é repetida.
5. A batalha termina com **vitória** (todos os inimigos derrotados) ou **derrota** (todos os heróis caíram).

---

## 5. Estrutura do projeto

```
.
├── main.py                       # Ponto de entrada e "raiz de composição"
└── rpg/
    ├── batalha.py                # Batalha: orquestra os turnos
    ├── fabricas.py               # FabricaDePersonagens (criação por registro)
    ├── menu_inicial.py           # MenuInicial: monta o grupo de heróis
    ├── combatentes/
    │   ├── base.py               # Combatente (classe abstrata)
    │   ├── personagens.py        # Personagem, Guerreiro, Mago, Arqueiro
    │   ├── inimigos.py           # Inimigo, Goblin
    │   └── chefao.py             # Chefao (inimigo com habilidade periódica)
    ├── habilidades/
    │   └── habilidades.py        # Habilidade, GolpePoderoso, BolaDeFogo, TiroDuplo
    ├── itens/
    │   ├── itens.py              # Usavel, Equipavel, Item, Pocao, Equipamento
    │   └── inventario.py         # Inventario
    └── ui/
        └── console.py            # Saida, Entrada, LeitorDeTexto e implementações
```

---

## 6. Princípios SOLID aplicados

Cada princípio abaixo indica **onde** foi aplicado e **como**, com referência ao código.

### S: Single Responsibility Principle (Responsabilidade Única)

> *Uma classe deve ter apenas um motivo para mudar.*

Cada classe do projeto tem um papel bem delimitado:

| Classe | Única responsabilidade | O que ela **não** faz |
|---|---|---|
| `Combatente` (`combatentes/base.py`) | Guardar o estado (vida, ataque, defesa) e as regras de dano/cura | Não imprime nada: `atacar()` e `status()` **devolvem texto** |
| `Batalha` (`batalha.py`) | Coordenar a ordem dos turnos | Não calcula dano (é dos combatentes), não usa `print`/`input` (é da UI) |
| `MenuInicial` (`menu_inicial.py`) | Conduzir o diálogo de montagem do grupo | Não cria personagens (é da fábrica) |
| `FabricaDePersonagens` (`fabricas.py`) | Criar personagens a partir do nome do tipo | Não conhece as regras do jogo |
| `Inventario` (`itens/inventario.py`) | Guardar e entregar itens | Não sabe o que o item faz e não mostra nada na tela |
| `Pocao` / `Equipamento` (`itens/itens.py`) | Aplicar o próprio efeito | Não gerenciam o inventário |
| `ConsoleSaida` / `ConsoleEntrada` (`ui/console.py`) | Falar com o terminal (`print`/`input`) e validar a entrada | Não conhecem o jogo |

**Exemplo concreto:** se o formato da mensagem de status mudar, só `Combatente.status()` é alterado. Se o jogo migrar do terminal para uma interface gráfica, só `ui/console.py` precisa de um substituto; `Batalha` e `Combatente` continuam intactos.

### O: Open/Closed Principle (Aberto/Fechado)

> *Entidades devem estar abertas para extensão e fechadas para modificação.*

Há quatro pontos de extensão no projeto:

1. **`Chefao`** (`combatentes/chefao.py`): foi criado em um arquivo novo, **sem alterar** `Goblin`, `Combatente`, `Habilidade` nem `Batalha`. Ele apenas sobrescreve `Inimigo.agir()` para usar uma habilidade a cada 3 ações.
2. **`FabricaDePersonagens.registrar()`** (`fabricas.py`): a fábrica não conhece `Guerreiro`, `Mago` ou `Arqueiro`. As "receitas" são registradas de fora, em `main.criar_fabrica()`. Uma nova classe jogável **não exige editar a fábrica**.
3. **`Habilidade`** (`habilidades/habilidades.py`): novas habilidades são novas subclasses que implementam `usar()`.
4. **`Inimigo.agir()`** (`combatentes/inimigos.py`): é o ponto de extensão do comportamento dos inimigos. A `Batalha` apenas chama `inimigo.agir(...)`.

Além disso, o menu de ações do herói em `Batalha._turno_do_heroi` é uma **lista de pares (texto, método)**. Para ganhar uma nova ação, basta adicionar um item na lista, sem alterar a lógica que exibe e executa o menu.

### L: Liskov Substitution Principle (Substituição de Liskov)

> *Subtipos devem poder substituir seus tipos base sem quebrar o programa.*

- **`Inimigo` → `Goblin` / `Chefao`:** em `Batalha._turno_dos_inimigos`, o código trata todos como `Inimigo` e chama `inimigo.agir(herois_vivos)`. A própria classe tem o comentário *"A Batalha NÃO sabe se é Goblin ou Chefao"*. O `Chefao.agir()` respeita o contrato da classe base: recebe a lista de alvos vivos e devolve um `str`.
- **`Combatente` → `Guerreiro` / `Mago` / `Arqueiro` / `Goblin` / `Chefao`:** qualquer um pode ser alvo de `receber_dano`, `curar`, `aplicar_bonus` ou `atacar`, sem verificação de tipo.
- **`Habilidade` → `GolpePoderoso` / `BolaDeFogo` / `TiroDuplo`:** `usar(usuario, alvo)` aceita **qualquer** `Combatente`. Tanto o `Personagem` quanto o `Chefao` executam `self._habilidade.usar(...)` sem saber qual habilidade têm. `TiroDuplo` até reaproveita `usuario.atacar(alvo)`, confiando no contrato de `Combatente`.
- **Sem `isinstance`:** o `Inventario` mantém duas listas separadas (`_usaveis` e `_equipaveis`) justamente para não precisar descobrir o tipo de cada item em tempo de execução.

### I: Interface Segregation Principle (Segregação de Interfaces)

> *Nenhuma classe deve ser forçado a depender de métodos que não usa.*

O projeto usa `typing.Protocol` para definir **interfaces pequenas e específicas**:

**Em `ui/console.py`:**

| Interface | Método | Quem usa |
|---|---|---|
| `Saida` | `mostrar()` | `Batalha`, `MenuInicial` |
| `Entrada` | `escolher()` | `Batalha`, `MenuInicial` |
| `LeitorDeTexto` | `ler_texto()` | Apenas `MenuInicial` |

`LeitorDeTexto` é separada de `Entrada` **de propósito**: a `Batalha` só precisa de escolhas numéricas e não deve ser obrigada a conhecer leitura de texto livre. Por isso o construtor da `Batalha` recebe `saida` e `entrada`, mas **não** um leitor.

**Em `itens/itens.py`:**

| Interface | Método-chave | Implementada por |
|---|---|---|
| `Usavel` | `usar(alvo)` | `Pocao` |
| `Equipavel` | `equipar(portador)` | `Equipamento` |

Uma poção não precisa implementar `equipar()`, e uma espada não precisa implementar `usar()`. Um item futuro que seja **os dois** (ex.: um amuleto que cura e dá bônus) pode cumprir ambos os contratos.

### D: Dependency Inversion Principle (Inversão de Dependência)

> *Módulos de alto nível devem depender de abstrações, não de implementações concretas.*

- **`Batalha`** (alto nível) depende de `Saida` e `Entrada` (abstrações), **não** de `ConsoleSaida`/`ConsoleEntrada`. Tudo chega pelo construtor (injeção de dependência), então a batalha pode ser testada com uma saída falsa ou ligada a outra interface.
- **`Personagem` e `Chefao`** recebem a `Habilidade` pelo construtor, em vez de instanciar uma habilidade concreta internamente.
- **`MenuInicial`** recebe a `FabricaDePersonagens`, `Saida`, `Entrada` e `LeitorDeTexto` de fora.
- **`Inventario`** depende dos Protocols `Usavel` e `Equipavel`, não das classes `Pocao` e `Equipamento`.
- **Raiz de composição (`main.py`):** é o **único** lugar que conhece as classes concretas (`ConsoleSaida`, `Goblin`, `GolpePoderoso`...) e as liga entre si. Todo o restante do código fala apenas com abstrações.
- **Dependência circular evitada:** `habilidades.py` e `itens.py` importam `Combatente` apenas sob `TYPE_CHECKING`, ou seja, só para o verificador de tipos. Em tempo de execução não há acoplamento.

---

## 7. Conceitos de POO utilizados

| Conceito | Onde aparece |
|---|---|
| **Abstração** | Classes abstratas `Combatente`, `Habilidade` e `Item` (com `@abstractmethod`) |
| **Encapsulamento** | Atributos privados (`_vida`, `_ataque`...) com *properties* somente leitura; `aplicar_bonus()` é a única forma de alterar ataque/defesa e garante que nunca fiquem negativos; `Inventario` devolve **cópias** das listas |
| **Herança** | `Combatente` → `Personagem` → `Guerreiro`/`Mago`/`Arqueiro`; `Combatente` → `Inimigo` → `Goblin`/`Chefao` |
| **Polimorfismo** | `grito_de_guerra()`, `agir()`, `Habilidade.usar()` e `Item.descricao` têm comportamento diferente por subclasse, chamados de forma uniforme |
| **Composição** | `Personagem` e `Chefao` *têm uma* `Habilidade`; `Batalha` *tem* heróis, inimigos e inventário |

---

## 8. Como estender o jogo

**Adicionar uma nova classe jogável** (ex.: `Clerigo`):

1. Criar `class Clerigo(Personagem)` em `combatentes/personagens.py`, implementando `grito_de_guerra()`.
2. (Opcional) Criar uma nova `Habilidade` em `habilidades/habilidades.py`.
3. Registrar em `main.criar_fabrica()`:
   ```python
   fabrica.registrar("Clerigo", lambda nome: Clerigo(nome, Cura()))
   ```
   Ela aparece automaticamente no menu. Nenhuma outra classe precisa ser alterada.

**Adicionar um novo inimigo:** criar uma subclasse de `Inimigo` (sobrescrevendo `agir()` se quiser um comportamento diferente) e incluí-la na lista `inimigos` em `main.main()`.

**Adicionar um novo item:** criar uma subclasse de `Item` que implemente `usar()` e/ou `equipar()` e adicioná-la em `main.criar_inventario()`.

---

### Montando o grupo

<img width="573" height="216" alt="Captura de tela 2026-11-12 195125" src="https://github.com/user-attachments/assets/38f10bab-e076-400c-951e-7e5732cfd111" />

### Turno de um herói

<img width="450" height="343" alt="Captura de tela 2026-11-12 195304" src="https://github.com/user-attachments/assets/1ca96653-60f3-4df4-a8eb-8e65146a3855" />

### Usar um item

<img width="311" height="313" alt="Captura de tela 2026-11-12 195530" src="https://github.com/user-attachments/assets/4b99b2e8-360f-4ba9-965d-d7660d3a50a6" />

### Atacar um inimigo

<img width="553" height="193" alt="Captura de tela 2026-11-12 195605" src="https://github.com/user-attachments/assets/67e69d7c-0417-4ea3-ac1f-b522ad8c260f" />

### Equipar um item

<img width="329" height="350" alt="Captura de tela 2026-11-12 195643" src="https://github.com/user-attachments/assets/dd7a9baf-bdb3-45d8-9558-8d4adf1be400" />

### Fim do RPG

<img width="373" height="71" alt="Captura de tela 2026-11-12 195802" src="https://github.com/user-attachments/assets/a7dc23f9-91ee-4e48-ab77-cea9983f9289" />

## Autora

Izabela Fernandes · Projeto acadêmico da disciplina de Paradigmas da Programação.
