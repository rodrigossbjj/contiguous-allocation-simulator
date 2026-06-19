from typing import List, Optional

class Disk:
    def __init__(self, total_blocks: int) -> None:
        """
        Representação física do disco (vetor de blocos).
        :param total_blocks: Capacidade total do disco em blocos.
        """
        if total_blocks <= 0:
            raise ValueError("O disco deve conter pelo menos um bloco.")
        self.total_blocks: int = total_blocks
        self._blocks: List[Optional[str]] = [None] * total_blocks

    def write_blocks(self, start_block: int, size: int, file_name: str) -> None:
        """
        Grava o identificador do arquivo no intervalo contíguo especificado.
        Levanta ValueError se violar limites ou tentar sobrescrever blocos ocupados.
        """
        if start_block < 0 or start_block + size > self.total_blocks:
            raise ValueError("O intervalo especificado ultrapassa os limites do disco.")
        if size <= 0:
            raise ValueError("O tamanho a ser gravado deve ser maior que zero.")
        if not file_name or not isinstance(file_name, str) or file_name.strip() == "":
            raise ValueError("Nome do arquivo inválido para gravação.")

        # Verificar se todos os blocos no intervalo estão livres
        if not self.is_range_free(start_block, size):
            raise ValueError("Alguns blocos no intervalo selecionado já estão ocupados.")

        for i in range(start_block, start_block + size):
            self._blocks[i] = file_name.strip()

    def clear_blocks(self, start_block: int, size: int) -> None:
        """
        Libera (seta para None) o intervalo contíguo especificado.
        """
        if start_block < 0 or start_block + size > self.total_blocks:
            raise ValueError("O intervalo especificado ultrapassa os limites do disco.")
        if size <= 0:
            raise ValueError("O tamanho a ser limpo deve ser maior que zero.")

        for i in range(start_block, start_block + size):
            self._blocks[i] = None

    def is_range_free(self, start_block: int, size: int) -> bool:
        """
        Verifica se todos os blocos no intervalo [start_block, start_block + size[ estão livres.
        """
        if start_block < 0 or start_block + size > self.total_blocks:
            return False
        return all(self._blocks[i] is None for i in range(start_block, start_block + size))

    def get_block_status(self, block_index: int) -> Optional[str]:
        """
        Retorna o nome do arquivo no bloco, ou None se livre.
        """
        if block_index < 0 or block_index >= self.total_blocks:
            raise IndexError("Índice do bloco fora dos limites do disco.")
        return self._blocks[block_index]

    def get_blocks_state(self) -> List[Optional[str]]:
        """Retorna uma cópia do estado atual dos blocos do disco."""
        return list(self._blocks)
