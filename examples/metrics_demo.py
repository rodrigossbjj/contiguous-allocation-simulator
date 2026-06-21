import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.allocation.contiguous_allocator import ContiguousAllocator
from src.metrics.fragmentation_metrics import FragmentationMetrics
from src.models.disk import Disk
from src.models.file import File
from src.visualization.disk_render import DiskRenderer


def run():
    disk = Disk(12)
    allocator = ContiguousAllocator()
    files = [File(name, 3) for name in ("A", "B", "C", "D")]

    for file in files:
        allocator.allocate(disk, file)

    allocator.deallocate(disk, files[1])
    allocator.deallocate(disk, files[3])

    print("\nDisco após remover B e D:")
    DiskRenderer().render(disk)

    print("Relatório de métricas:")
    for metric, value in FragmentationMetrics(disk).generate_report().items():
        print(f"  {metric}: {value}")


if __name__ == "__main__":
    run()
