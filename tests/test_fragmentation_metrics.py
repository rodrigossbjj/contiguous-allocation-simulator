import unittest

from src.metrics.fragmentation_metrics import FragmentationMetrics
from src.models.disk import Disk


class TestFragmentationMetrics(unittest.TestCase):
    def test_empty_disk(self):
        metrics = FragmentationMetrics(Disk(10))

        self.assertEqual(metrics.get_free_space(), 10)
        self.assertEqual(metrics.get_largest_free_region(), 10)
        self.assertEqual(metrics.calculate_occupancy_rate(), 0.0)
        self.assertEqual(metrics.calculate_external_fragmentation(), 0.0)

    def test_full_disk(self):
        disk = Disk(8)
        disk.write_blocks(0, 8, "A")
        metrics = FragmentationMetrics(disk)

        self.assertEqual(metrics.get_free_space(), 0)
        self.assertEqual(metrics.get_largest_free_region(), 0)
        self.assertEqual(metrics.calculate_occupancy_rate(), 100.0)
        self.assertEqual(metrics.calculate_external_fragmentation(), 0.0)

    def test_single_free_region(self):
        disk = Disk(10)
        disk.write_blocks(0, 3, "A")
        metrics = FragmentationMetrics(disk)

        self.assertEqual(metrics.get_free_space(), 7)
        self.assertEqual(metrics.get_largest_free_region(), 7)
        self.assertEqual(metrics.calculate_external_fragmentation(), 0.0)

    def test_multiple_free_regions(self):
        disk = Disk(10)
        disk.write_blocks(2, 2, "A")
        disk.write_blocks(7, 1, "B")
        metrics = FragmentationMetrics(disk)

        self.assertEqual(metrics.get_free_space(), 7)
        self.assertEqual(metrics.get_largest_free_region(), 3)
        self.assertAlmostEqual(
            metrics.calculate_external_fragmentation(),
            100.0 * (1.0 - 3 / 7),
        )

    def test_largest_free_region_can_be_at_disk_end(self):
        disk = Disk(12)
        disk.write_blocks(1, 2, "A")
        disk.write_blocks(5, 2, "B")
        metrics = FragmentationMetrics(disk)

        self.assertEqual(metrics.get_largest_free_region(), 5)

    def test_project_fragmentation_scenario(self):
        disk = Disk(12)
        disk.write_blocks(0, 3, "A")
        disk.write_blocks(3, 3, "B")
        disk.write_blocks(6, 3, "C")
        disk.write_blocks(9, 3, "D")
        disk.clear_blocks(3, 3)
        disk.clear_blocks(9, 3)
        metrics = FragmentationMetrics(disk)

        self.assertEqual(metrics.get_free_space(), 6)
        self.assertEqual(metrics.get_largest_free_region(), 3)
        self.assertEqual(metrics.calculate_occupancy_rate(), 50.0)
        self.assertEqual(metrics.calculate_external_fragmentation(), 50.0)

    def test_report_content_and_types(self):
        disk = Disk(5)
        disk.write_blocks(1, 2, "A")
        report = FragmentationMetrics(disk).generate_report()

        self.assertEqual(
            set(report),
            {
                "total_blocks",
                "used_blocks",
                "free_blocks",
                "largest_free_region",
                "occupancy_rate",
                "external_fragmentation",
            },
        )
        self.assertEqual(report["total_blocks"], 5)
        self.assertEqual(report["used_blocks"], 2)
        self.assertEqual(report["free_blocks"], 3)
        self.assertEqual(report["largest_free_region"], 2)
        for key in ("total_blocks", "used_blocks", "free_blocks", "largest_free_region"):
            self.assertIsInstance(report[key], int)
        for key in ("occupancy_rate", "external_fragmentation"):
            self.assertIsInstance(report[key], float)


if __name__ == "__main__":
    unittest.main()
