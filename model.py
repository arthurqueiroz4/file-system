from datetime import datetime
from typing import Any

BLOCK_LEN = 5


class Disk:
    def __init__(self) -> None:
        self.length: int = 0
        self.length_max = 100000
        self.blocks: list[str] = [""] * self.length_max

    def store(self, data: str) -> int:
        len_before_appending = self.length
        if self.length == self.length_max:
            raise Exception("Disk papocou")
        for char in data:
            self.blocks[self.length] = char
            self.length += 1

        self.length += BLOCK_LEN - self.length % BLOCK_LEN
        return len_before_appending

    def get(self, index) -> str:
        return "".join(self.blocks[index : index + BLOCK_LEN])

    def release(self, index: int, length: int) -> None:
        """
        Libera os blocos de dados no disco, apagando-os a partir de um índice.

        Args:
            index (int): Índice inicial do dado a ser liberado.
            length (int): Quantidade de blocos a serem liberados.
        """
        for i in range(index, index + length):
            self.blocks[i] = ""


class IndexNode:
    def __init__(self):
        self.length = 0
        self.pointers: list[int] = []  # list of integer/index


class PrincipalMemory:
    def __init__(self):
        self.files: list[File] = []
        self.threshold = 5

    def put(self, file):
        if len(self.files) == self.threshold:
            _ = self.files.pop(0)
        self.files.append(file)

    def remove(self, file):
        self.files.remove(file)

    def list(self):
        [print(file) for file in self.files]


class File:
    def __init__(self, name: str, owner: str, disk: Disk):
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.owner = owner
        self.index_node = IndexNode()
        self.is_open = False
        self.disk = disk

    def open(self, pm: PrincipalMemory):
        pm.put(self)
        self.is_open = True

    def delete(self):
        """Deleta o arquivo, liberando os blocos de dados do disco e limpando o i-node."""
        for pointer in self.index_node.pointers:
            self.disk.release(pointer, BLOCK_LEN)
        self.index_node.pointers.clear()
        self.index_node.length = 0
        print(f"Arquivo {self.name} deletado com sucesso.")

    def close(self, pm: PrincipalMemory):
        pm.remove(self)
        self.is_open = False

    def read(self):
        if not self.is_open:
            raise Exception("File should be open for be read")

        result = ""
        for pointer in self.index_node.pointers:
            result += self.disk.get(pointer)
        return result

    def write(self, data: str):
        if not self.is_open:
            raise Exception("File should be open for be written")

        self.index_node.length += len(data)
        pointer_start = self.disk.store(data)

        # TODO: Testar isso com -> Escrever arquivo intercalados
        for index in range(pointer_start, pointer_start + len(data), BLOCK_LEN):
            self.index_node.pointers.append(index)


class Directory:
    def __init__(self, name: str):
        """
        Inicializa um diretório com nome, arquivos e subdiretórios vazios, e uma referência ao diretório pai.

        Args:
            name (str): Nome do diretório.
        """
        self.name = name
        self.files: dict[str, File] = {}
        self.subdirectories: dict[str, Directory] = {}
        self.parent: Union[Directory, None] = None

    def create_file(self, file_name: str, owner: str, disk: Disk):
        """
        Cria um novo arquivo dentro do diretório.

        Args:
            file_name (str): Nome do arquivo.
            owner (str): Proprietário do arquivo.
            disk (Disk): Disco onde os dados do arquivo serão armazenados.

        Raises:
            Exception: Se o arquivo já existir.
        """
        pass

    def create_directory(self, dir_name: str):
        """
        Cria um novo subdiretório dentro do diretório atual.

        Args:
            dir_name (str): Nome do novo subdiretório.

        Raises:
            Exception: Se o subdiretório já existir.
        """
        pass

    def list_contents(self):
        """Lista os arquivos e subdiretórios presentes no diretório."""
        pass

    def move_file(self, file_name: str, target_directory: "Directory"):
        """
        Move um arquivo para outro diretório.

        Args:
            file_name (str): Nome do arquivo a ser movido.
            target_directory (Directory): Diretório de destino.

        Raises:
            Exception: Se o arquivo não for encontrado.
        """
        pass

    def navigate_to(self, dir_name: str) -> "Directory":
        """
        Navega para um subdiretório específico ou para o diretório pai.

        Args:
            dir_name (str): Nome do diretório de destino (".." para o diretório pai ou "." para o atual).

        Returns:
            Directory: Diretório de destino.

        Raises:
            Exception: Se o subdiretório não for encontrado.
        """
        pass
