# 🧠 Contiguous Allocation Simulator

Este projeto é um simulador interativo desenvolvido para demonstrar o funcionamento básico da técnica de **Alocação Contígua de Blocos** em Sistemas de Arquivos, bem como os efeitos e cálculo de **fragmentação externa**. O simulador foi construído como parte da avaliação do **Trabalho 3** da disciplina de **Sistemas Operacionais** do **IFCE - Campus Maracanaú**.

O projeto conta com um menu interativo completo, renderização visual de blocos no terminal, cálculo de métricas em tempo real e testes automatizados.

---

## 👥 Divisão da Equipe e Entregas

O projeto foi dividido de forma colaborativa entre **4 integrantes**, cobrindo todas as frentes de arquitetura, simulação, métricas e visualização:

1. **Integrante 1: Rodrigo**
   * **Responsabilidades**: Definição da arquitetura, implementação dos modelos centrais (`Disk`, `File`) e do buscador contíguo com estratégia *First-Fit*.
   * **Arquivos**: `src/models/disk.py`, `src/models/file.py`, `src/allocation/contiguous_allocator.py`.

2. **Integrante 2: Amanda Vieira (Simulação e Casos de Uso)**
   * **Responsabilidades**: Operações de manipulação lógica de arquivos (criação, remoção, listagem) e construção de cenários didáticos.
   * **Arquivos**: `src/simulation/simulator.py`, `examples/simple_demo.py`, `examples/fragmentation_demo.py`.

3. **Integrante 3: João Victor de Lima Pereira (Métricas e Análise)**
   * **Responsabilidades**: Desenvolvimento do módulo analítico de métricas de ocupação do disco e cálculo preciso de fragmentação externa.
   * **Arquivos**: `src/metrics/fragmentation_metrics.py`, `examples/metrics_demo.py`, `tests/test_fragmentation_metrics.py`.

4. **Integrante 4: Orleoncio (Visualização e Apresentação)**
   * **Responsabilidades**: Criação da exibição textual-gráfica dos blocos do disco em formato de grade e legendas das partições de arquivos.
   * **Arquivos**: `src/visualization/disk_render.py`.

---

## 🛠️ Arquitetura do Sistema

O projeto segue um design modularizado orientado a objetos com a seguinte estrutura de pastas:

```text
contiguous-allocation-simulator/
├── src/
│   ├── models/              # Representação física e lógica (Disk, File)
│   ├── allocation/          # Algoritmos e estratégias de busca (First-Fit)
│   ├── simulation/          # Orquestrador central (Simulator)
│   ├── metrics/             # Cálculo analítico de fragmentação
│   └── visualization/       # Renderização visual dos blocos no terminal
├── examples/                # Cenários didáticos pré-configurados
├── tests/                   # Suíte de testes unitários automatizados
├── main.py                  # Ponto de entrada interativo da aplicação
└── build.sh                 # Script de compilação automática
```

---

## 📊 Métricas de Fragmentação

O módulo de análise calcula as seguintes métricas a partir do estado atual do disco:

* **Taxa de Ocupação (%)**: Percentual de blocos ocupados no disco.
  $$\text{Taxa de Ocupação} = \frac{\text{Blocos Ocupados}}{\text{Total de Blocos}} \times 100$$
* **Fragmentação Externa (%)**: Percentual de espaço livre que não pode ser aproveitado por um único arquivo correspondente à maior região contígua livre, quantificando a fragmentação do disco.
  $$\text{Fragmentação Externa} = \left(1 - \frac{\text{Maior Região Livre Contígua}}{\text{Espaço Livre Total}}\right) \times 100$$

*Nota: Quando o disco está cheio ou o espaço livre está em uma única região contígua, a fragmentação externa é de $0.0\%$.*

---

## 🚀 Como Executar

### 1. Menu Interativo Principal (main.py)
A aplicação conta com um menu unificado que executa tanto os cenários didáticos clássicos quanto um modo de simulação passo a passo interativo.

Execute o comando a partir da raiz do projeto:
```bash
python3 main.py
```

O menu permite selecionar as seguintes opções:
* **Opção 1**: Cenário 1 (Alocação e Exclusão Básica)
* **Opção 2**: Cenário 2 (Demonstração prática de falha por Fragmentação Externa)
* **Opção 3**: Cenário 3 (Relatório consolidado de métricas)
* **Opção 4**: Modo Interativo (Onde você especifica o tamanho do disco e gerencia a criação/exclusão de arquivos manualmente, vendo o disco e as métricas atualizarem em tempo real)

---

## 📦 Compilação e Distribuição (Executável Autônomo)

Para testar o simulador em computadores que não possuem Python instalado, fornecemos um script de compilação para gerar um executável autônomo do Linux:

```bash
./build.sh
```

* **Como funciona**: O script verifica a presença do `PyInstaller`. Caso não o encontre, cria um ambiente virtual temporário (`build_venv`), instala a dependência e compila a aplicação de forma limpa, sem poluir os pacotes do sistema (PEP 668).
* **Resultado**: O executável compilado será gerado em **`./dist/simulador`** e pode ser rodado diretamente com:
  ```bash
  ./dist/simulador
  ```

---

## 🧪 Testes Automatizados

A suíte de testes valida a lógica física do disco, o buscador First-Fit e o comportamento lógico das criações/remoções de arquivos. Para rodar todos os testes unitários da aplicação:

```bash
python3 -m unittest discover tests -v
```
