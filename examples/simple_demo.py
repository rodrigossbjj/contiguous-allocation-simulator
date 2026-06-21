import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.simulation.simulator import Simulator
from src.visualization.disk_render import DiskRenderer


def run():
    renderer = DiskRenderer()

    print("\n🧠 CENÁRIO 1: ALOCAÇÃO E EXCLUSÃO SIMPLES\n")
    time.sleep(1)

    sim = Simulator(16)

    renderer.render(sim.disk)
    time.sleep(1)

    print("\nAlocando A, B, C...\n")
    sim.create_file("A", 4)
    renderer.render(sim.disk)
    time.sleep(1)

    sim.create_file("B", 4)
    renderer.render(sim.disk)
    time.sleep(1)

    sim.create_file("C", 4)
    renderer.render(sim.disk)
    time.sleep(1)

    print("\nRemovendo B...\n")
    sim.delete_file("B")
    renderer.render(sim.disk)
    time.sleep(1)


if __name__ == "__main__":
    run()