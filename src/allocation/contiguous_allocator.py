from typing import List, Optional, Protocol
from src.models.disk import Disk
from src.models.file import File

class AllocationStrategy(Protocol):
    def find_partition(self, blocks: List[Optional[str]], size: int) -> Optional[int]:
        """
        Retorna o índice do bloco inicial onde a partição contígua de 'size' blocos livres pode começar.
        Retorna None caso não seja encontrada nenhuma partição adequada.
        """
        ...

class FirstFitStrategy:
    """
    Estratégia First-Fit: Aloca o arquivo na primeira partição livre contígua grande o suficiente.
    """
    def find_partition(self, blocks: List[Optional[str]], size: int) -> Optional[int]:
        current_free_run = 0
        start_index = None
        
        for i, block in enumerate(blocks):
            if block is None:
                if current_free_run == 0:
                    start_index = i
                current_free_run += 1
                if current_free_run == size:
                    return start_index
            else:
                current_free_run = 0
                start_index = None
                
        return None

class ContiguousAllocator:
    def __init__(self, strategy: Optional[AllocationStrategy] = None) -> None:
        """
        :param strategy: Estratégia de alocação a ser utilizada. Padrão: FirstFitStrategy.
        """
        self.strategy: AllocationStrategy = strategy or FirstFitStrategy()

    def allocate(self, disk: Disk, file: File) -> bool:
        """
        Tenta encontrar uma partição livre contígua para o arquivo e gravá-la.
        Retorna True se conseguir alocar, False caso contrário.
        """
        if file.is_allocated:
            raise ValueError(f"O arquivo '{file.name}' já está alocado no bloco {file.start_block}.")
            
        blocks_state = disk.get_blocks_state()
        start_block = self.strategy.find_partition(blocks_state, file.size)
        
        if start_block is None:
            return False
            
        disk.write_blocks(start_block, file.size, file.name)
        file.start_block = start_block
        return True

    def deallocate(self, disk: Disk, file: File) -> bool:
        """
        Libera o espaço ocupado pelo File no Disk.
        Retorna True se bem sucedido.
        """
        if not file.is_allocated:
            raise ValueError(f"O arquivo '{file.name}' não está alocado no disco.")
            
        disk.clear_blocks(file.start_block, file.size)
        file.start_block = None
        return True
