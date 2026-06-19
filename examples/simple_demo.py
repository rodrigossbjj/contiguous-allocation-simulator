import sys
import os

# Adiciona o diretório raiz ao path para importar o simulador
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.simulation.simulator import Simulator

def format_disk(blocks) -> str:
    return "".join(f"[{b if b is not None else '.'}]" for b in blocks)

def run() -> None:
    print("==================================================")
    print("    CENÁRIO 1: ALOCAÇÃO E EXCLUSÃO SIMPLES       ")
    print("==================================================")

    # 1. Inicializa o simulador com 16 blocos
    print("\nPasso 1: Inicializando o disco com 16 blocos.")
    sim = Simulator(16)
    print("Estado do Disco:", format_disk(sim.disk.get_blocks_state()))

    # 2. Aloca arquivos A, B e C
    print("\nPasso 2: Alocando arquivos A (4 blocos), B (4 blocos) e C (4 blocos).")
    sim.create_file("A", 4)
    sim.create_file("B", 4)
    sim.create_file("C", 4)
    print("Estado do Disco:", format_disk(sim.disk.get_blocks_state()))

    # 3. Exclui o arquivo B (no meio)
    print("\nPasso 3: Excluindo o arquivo B (meio do disco) gerando um 'buraco'.")
    sim.delete_file("B")
    print("Estado do Disco:", format_disk(sim.disk.get_blocks_state()))

if __name__ == "__main__":
    run()
