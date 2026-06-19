import sys
import os

# Adiciona o diretório raiz ao path para importar o simulador
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.simulation.simulator import Simulator

def format_disk(blocks) -> str:
    return "".join(f"[{b if b is not None else '.'}]" for b in blocks)

def run() -> None:
    print("==================================================")
    print("  CENÁRIO 2: DEMONSTRAÇÃO DE FRAGMENTAÇÃO EXTERNA ")
    print("==================================================")

    # 1. Inicializa o simulador com 12 blocos
    print("\nPasso 1: Inicializando o disco com 12 blocos.")
    sim = Simulator(12)
    print("Estado do Disco:", format_disk(sim.disk.get_blocks_state()))

    # 2. Aloca arquivos A, B, C e D de tamanho 3 cada
    print("\nPasso 2: Alocando 4 arquivos de 3 blocos cada: A, B, C e D.")
    sim.create_file("A", 3)
    sim.create_file("B", 3)
    sim.create_file("C", 3)
    sim.create_file("D", 3)
    print("Estado do Disco:", format_disk(sim.disk.get_blocks_state()))

    # 3. Libera B e D
    print("\nPasso 3: Excluindo os arquivos B e D para fragmentar o espaço livre.")
    sim.delete_file("B")
    sim.delete_file("D")
    print("Estado do Disco:", format_disk(sim.disk.get_blocks_state()))

    # 4. Tenta alocar arquivo E de tamanho 4
    print("\nPasso 4: Tentando criar arquivo E de tamanho 4.")
    print("Nota: Temos 6 blocos livres no total (3 do B e 3 do D).")
    
    success = sim.create_file("E", 4)
    if not success:
        print("\n[FALHA NA ALOCAÇÃO] Não foi possível alocar o arquivo 'E' de tamanho 4.")
        print("Explicação teórica de SO:")
        print("-> Há 6 blocos livres no total, porém o maior espaço contíguo livre tem tamanho 3.")
        print("-> Caracteriza-se FRAGMENTAÇÃO EXTERNA: há memória total suficiente, mas não há um bloco contíguo único para a requisição.")
    else:
        print("\n[SUCESSO] Alocação realizada!")

if __name__ == "__main__":
    run()
