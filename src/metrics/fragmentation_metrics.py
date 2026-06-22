from typing import Dict, Union

from src.models.disk import Disk


MetricValue = Union[int, float]


class FragmentationMetrics:
    """Calcula métricas instantâneas a partir do estado de um disco."""

    def __init__(self, disk: Disk) -> None:
        self.disk = disk

    def get_free_space(self) -> int:
        """Retorna a quantidade total de blocos livres."""
        return sum(block is None for block in self.disk.get_blocks_state())

    def get_largest_free_region(self) -> int:
        """Retorna o tamanho da maior sequência contígua de blocos livres."""
        largest_region = 0
        current_region = 0

        for block in self.disk.get_blocks_state():
            if block is None:
                current_region += 1
                largest_region = max(largest_region, current_region)
            else:
                current_region = 0

        return largest_region

    def calculate_occupancy_rate(self) -> float:
        """Retorna o percentual de blocos ocupados no disco."""
        used_blocks = self.disk.total_blocks - self.get_free_space()
        return 100.0 * used_blocks / self.disk.total_blocks

    def calculate_external_fragmentation(self) -> float:
        """Retorna o percentual do espaço livre fora da maior região livre."""
        free_blocks = self.get_free_space()
        if free_blocks == 0:
            return 0.0

        largest_region = self.get_largest_free_region()
        return 100.0 * (1.0 - largest_region / free_blocks)

    def generate_report(self) -> Dict[str, MetricValue]:
        """Consolida contagens e taxas do estado atual do disco."""
        free_blocks = self.get_free_space()
        return {
            "total_blocks": self.disk.total_blocks,
            "used_blocks": self.disk.total_blocks - free_blocks,
            "free_blocks": free_blocks,
            "largest_free_region": self.get_largest_free_region(),
            "occupancy_rate": self.calculate_occupancy_rate(),
            "external_fragmentation": self.calculate_external_fragmentation(),
        }
