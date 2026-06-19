import unittest
from src.simulation.simulator import Simulator

class TestSimulator(unittest.TestCase):
    def test_simulator_create_and_delete(self):
        sim = Simulator(10)
        
        # Cria arquivo
        success = sim.create_file("A", 4)
        self.assertTrue(success)
        self.assertIn("A", sim.files)
        self.assertEqual(sim.files["A"].start_block, 0)
        
        # Lista arquivos
        files = sim.list_files()
        self.assertEqual(len(files), 1)
        self.assertEqual(files[0].name, "A")
        
        # Deleta arquivo
        del_success = sim.delete_file("A")
        self.assertTrue(del_success)
        self.assertNotIn("A", sim.files)
        self.assertEqual(len(sim.list_files()), 0)

    def test_simulator_duplicate_file_error(self):
        sim = Simulator(10)
        sim.create_file("A", 2)
        with self.assertRaises(ValueError):
            sim.create_file("A", 3)

if __name__ == "__main__":
    unittest.main()
