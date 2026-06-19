import unittest
from src.models.disk import Disk
from src.models.file import File
from src.allocation.contiguous_allocator import ContiguousAllocator, FirstFitStrategy

class TestContiguousAllocator(unittest.TestCase):
    def test_first_fit_strategy_allocation(self):
        blocks = [None, None, "fileX", None, None, None, "fileY", None]
        # Esperamos achar partição de tamanho 2 no índice 0
        strategy = FirstFitStrategy()
        idx = strategy.find_partition(blocks, 2)
        self.assertEqual(idx, 0)

        # Esperamos achar partição de tamanho 3 no índice 3
        idx = strategy.find_partition(blocks, 3)
        self.assertEqual(idx, 3)

        # Esperamos None para tamanho 4
        idx = strategy.find_partition(blocks, 4)
        self.assertIsNone(idx)

    def test_allocator_allocate_success(self):
        disk = Disk(10)
        allocator = ContiguousAllocator()
        file = File("A", 3)
        
        success = allocator.allocate(disk, file)
        self.assertTrue(success)
        self.assertEqual(file.start_block, 0)
        self.assertEqual(disk.get_blocks_state()[:3], ["A", "A", "A"])

    def test_allocator_allocate_failure(self):
        disk = Disk(5)
        allocator = ContiguousAllocator()
        
        # Ocupa parte do disco
        disk.write_blocks(1, 2, "X")  # bloco 1 e 2 ocupados
        
        file = File("A", 4)
        success = allocator.allocate(disk, file)
        self.assertFalse(success)
        self.assertIsNone(file.start_block)

    def test_allocator_deallocate(self):
        disk = Disk(5)
        allocator = ContiguousAllocator()
        file = File("A", 2)
        
        allocator.allocate(disk, file)
        self.assertEqual(file.start_block, 0)
        
        success = allocator.deallocate(disk, file)
        self.assertTrue(success)
        self.assertIsNone(file.start_block)
        self.assertEqual(disk.get_blocks_state(), [None] * 5)

if __name__ == "__main__":
    unittest.main()
