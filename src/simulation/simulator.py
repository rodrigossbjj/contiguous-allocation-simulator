from typing import Dict, List, Optional
from src.models.disk import Disk
from src.models.file import File
from src.allocation.contiguous_allocator import ContiguousAllocator, AllocationStrategy

class Simulator:
    def __init__(self, disk_size: int, strategy: Optional[AllocationStrategy] = None) -> None:
        """
        Orquestrador central do simulador de alocação.
        :param disk_size: Tamanho do disco em blocos.
        :param strategy: Estratégia de alocação (opcional).
        """
        self.disk: Disk = Disk(disk_size)
        self.allocator: ContiguousAllocator = ContiguousAllocator(strategy)
        self.files: Dict[str, File] = {}

    def create_file(self, name: str, size: int) -> bool:
        """
        Tenta criar e alocar um arquivo de tamanho 'size' blocos.
        :param name: Nome único do arquivo.
        :param size: Tamanho em blocos.
        :return: True se alocado com sucesso, False caso contrário.
        """
        name_clean = name.strip()
        if name_clean in self.files:
            raise ValueError(f"Arquivo com nome '{name_clean}' já existe.")

        file = File(name_clean, size)
        success = self.allocator.allocate(self.disk, file)
        
        if success:
            self.files[name_clean] = file
            return True
        return False

    def delete_file(self, name: str) -> bool:
        """
        Tenta remover e desalocar o arquivo com o nome 'name'.
        :param name: Nome do arquivo a ser deletado.
        :return: True se deletado com sucesso, False caso não seja encontrado.
        """
        name_clean = name.strip()
        if name_clean not in self.files:
            return False

        file = self.files[name_clean]
        self.allocator.deallocate(self.disk, file)
        del self.files[name_clean]
        return True

    def list_files(self) -> List[File]:
        """
        Retorna uma lista de todos os arquivos cadastrados/alocados.
        """
        return list(self.files.values())
