import unittest
from src.models.disk import Disk

class TestDisk(unittest.TestCase):
    def test_disk_initialization(self):
        disk = Disk(10)
        self.assertEqual(disk.total_blocks, 10)
        self.assertEqual(disk.get_blocks_state(), [None] * 10)

    def test_disk_invalid_initialization(self):
        with self.assertRaises(ValueError):
            Disk(0)
        with self.assertRaises(ValueError):
            Disk(-5)

    def test_write_and_clear_blocks(self):
        disk = Disk(10)
        disk.write_blocks(2, 3, "fileA")
        self.assertEqual(disk.get_block_status(2), "fileA")
        self.assertEqual(disk.get_block_status(3), "fileA")
        self.assertEqual(disk.get_block_status(4), "fileA")
        self.assertIsNone(disk.get_block_status(1))
        self.assertIsNone(disk.get_block_status(5))

        disk.clear_blocks(2, 3)
        self.assertEqual(disk.get_blocks_state(), [None] * 10)

    def test_write_blocks_out_of_bounds(self):
        disk = Disk(10)
        with self.assertRaises(ValueError):
            disk.write_blocks(8, 3, "fileA")
        with self.assertRaises(ValueError):
            disk.write_blocks(-1, 2, "fileA")

    def test_write_blocks_overlapping(self):
        disk = Disk(10)
        disk.write_blocks(2, 3, "fileA")
        with self.assertRaises(ValueError):
            disk.write_blocks(4, 2, "fileB")

    def test_is_range_free(self):
        disk = Disk(10)
        disk.write_blocks(2, 3, "fileA")
        self.assertTrue(disk.is_range_free(0, 2))
        self.assertFalse(disk.is_range_free(1, 2))
        self.assertTrue(disk.is_range_free(5, 5))

if __name__ == "__main__":
    unittest.main()
