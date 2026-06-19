# Contiguous Allocation Simulator (Escopo Simplificado)

Este projeto é um simulador simplificado desenvolvido para demonstrar o funcionamento básico da técnica de **Alocação Contígua de Blocos** em Sistemas de Arquivos para a disciplina de Sistemas Operacionais.

Esta versão contém exclusivamente os entregáveis dos **Integrantes 1 e 2**:
* **Integrante 1**: Modelos de domínio (`Disk`, `File`) e o algoritmo de alocação contígua (`ContiguousAllocator` com busca *First-Fit*).
* **Integrante 2**: Operações de manipulação do simulador (`Simulator` com criação, remoção e listagem de arquivos) e cenários de testes demonstrativos.

---

## 🛠️ Arquitetura do Sistema

O código fonte está localizado dentro do diretório `src/` e segue a seguinte estrutura:

* **`src.models`**: Abstrai as entidades físicas de representação de dados:
  * `Disk`: Vetor linear de blocos em memória (atômico).
  * `File`: Metadados do arquivo (nome, tamanho e bloco inicial).
* **`src.allocation`**: Define o motor de busca:
  * `ContiguousAllocator`: Gerencia a busca contígua por First-Fit e alteração atômica dos blocos.
* **`src.simulation`**: Define o fluxo operacional do simulador:
  * `Simulator`: Classe de coordenação (fachada) para manipulação de arquivos (criar, remover e listar).

---

## 🚀 Como Executar os Exemplos Didáticos

Os cenários didáticos demonstram o funcionamento básico e a ocorrência de fragmentação externa por meio de representações textuais simples de blocos (ex: `[A][A][.][.][B]`).

* **Cenário 1: Criação e Exclusão Básica**
  Demonstra a alocação sequencial e a liberação de espaço no meio do disco.
  ```bash
  python3 examples/simple_demo.py
  ```

* **Cenário 2: Demonstração da Fragmentação Externa**
  Demonstra a situação onde o disco possui espaço livre total suficiente para alocar um arquivo, mas a alocação falha por não haver nenhuma partição contígua livre com o tamanho requerido.
  ```bash
  python3 examples/fragmentation_demo.py
  ```

---

## 🧪 Como Executar os Testes Automatizados

Os testes cobrem a integridade física do disco, o acerto do buscador First-Fit e o comportamento do orquestrador do simulador.

Execute os testes com a ferramenta padrão `unittest` do Python:
```bash
python3 -m unittest discover tests
```
