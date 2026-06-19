from typing import Optional

class File:
    def __init__(self, name: str, size: int) -> None:
        """
        Representação lógica de um arquivo.
        :param name: Nome único identificador (ex: "arqA").
        :param size: Tamanho em quantidade de blocos.
        """
        if not name or not isinstance(name, str) or name.strip() == "":
            raise ValueError("O nome do arquivo não pode ser vazio ou inválido.")
        if size <= 0:
            raise ValueError("O tamanho do arquivo deve ser maior que zero.")
            
        self.name: str = name.strip()
        self.size: int = size
        self.start_block: Optional[int] = None  # Definido apenas quando alocado

    @property
    def is_allocated(self) -> bool:
        return self.start_block is not None

    def __repr__(self) -> str:
        return f"File(name={self.name!r}, size={self.size}, start={self.start_block})"
