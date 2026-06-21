import os
from src.models.disk import Disk


class DiskRenderer:

    def __init__(self):
        self.block_width = 5  # largura de cada célula

    def render(self, disk: Disk):
        blocks = disk.get_blocks_state()

        #os.system("cls" if os.name == "nt" else "clear")

        self._print_header()
        self._print_disk(blocks)
        self._print_indices(blocks)
        self._print_footer(blocks)

    def _print_header(self):
        print("\n🧠 CONTIGUOUS ALLOCATION SIMULATOR")
        print("=" * 60 + "\n")

    def _print_disk(self, blocks):
        size = len(blocks)

        print("┌" + "─────┬" * (size - 1) + "─────┐")

        print("│", end="")
        for b in blocks:
            label = "-" if b is None else b[0]
            print(f" {label:^3} │", end="")
        print()

        print("└" + "─────┴" * (size - 1) + "─────┘")

    def _print_indices(self, blocks):
        print("\n Índices:")
        print(" ", end="")

        for i in range(len(blocks)):
            print(f"{i:^5}", end=" ")

        print("\n")

    def _print_footer(self, blocks):
        used = {}

        for b in blocks:
            if b is not None:
                used[b] = used.get(b, 0) + 1

        if not used:
            print("📦 Disco vazio\n")
            return

        print("📌 Legenda (arquivos alocados):")
        for name, count in used.items():
            print(f"  - {name}: {count} bloco(s)")
        print()