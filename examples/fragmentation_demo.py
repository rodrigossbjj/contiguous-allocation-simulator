import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.simulation.simulator import Simulator
from src.visualization.disk_render import DiskRenderer


def run():
    renderer = DiskRenderer()

    print("\n🧠 CENÁRIO 2: FRAGMENTAÇÃO EXTERNA\n")
    time.sleep(1)

    sim = Simulator(12)

    renderer.render(sim.disk)
    time.sleep(1)

    print("\nAlocando A, B, C, D...\n")
    sim.create_file("A", 3)
    sim.create_file("B", 3)
    sim.create_file("C", 3)
    sim.create_file("D", 3)

    renderer.render(sim.disk)
    time.sleep(1)

    print("\nRemovendo B e D...\n")
    sim.delete_file("B")
    sim.delete_file("D")

    renderer.render(sim.disk)
    time.sleep(1)

    print("\nTentando alocar E (tamanho 4)...\n")
    success = sim.create_file("E", 4)

    renderer.render(sim.disk)
    time.sleep(1)

    if not success:
        print("\n❌ FRAGMENTAÇÃO EXTERNA DETECTADA")
        print("Memória total livre existe, mas não contígua.\n")


if __name__ == "__main__":
    run()