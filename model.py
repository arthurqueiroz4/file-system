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
from datetime import datetime
from typing import Any, Union

BLOCK_LEN = 5

class Disk():
    def __init__(self) -> None:
        """Inicializa o disco com tamanho máximo e blocos vazios."""
        self.length: int = 0
        self.length_max = 100000
        self.blocks: list[str] = [''] * self.length_max

    def store(self, data: str) -> int:
        """
        Armazena uma string no disco, dividindo-a em blocos.
        
        Args:
            data (str): Dados a serem armazenados no disco.

        Returns:
            int: Índice inicial no disco onde os dados foram armazenados.
        """
        len_before_appending = self.length
        if self.length == self.length_max:
            raise Exception("Disk papocou")
        for char in data:
            self.blocks[self.length] = char
            self.length += 1

        self.length += BLOCK_LEN - self.length % BLOCK_LEN
        return len_before_appending
 
    def get(self, index) -> str:
        """
        Recupera os dados armazenados no disco a partir de um índice específico.
        
        Args:
            index (int): Índice inicial no disco.

        Returns:
            str: Dados recuperados.
        """
        return ''.join(self.blocks[index: index + BLOCK_LEN])

    def release(self, index: int, length: int) -> None:
        """
        Libera os blocos de dados no disco, apagando-os a partir de um índice.

        Args:
            index (int): Índice inicial do dado a ser liberado.
            length (int): Quantidade de blocos a serem liberados.
        """
        for i in range(index, index + length):
            self.blocks[i] = ''


class IndexNode():
    def __init__(self):
        """Inicializa um i-node com comprimento zero e sem ponteiros."""
        self.length = 0
        self.pointers: list[int] = []


class PrincipalMemory():
    def __init__(self):
        """Inicializa a memória principal com uma lista vazia de arquivos e um limite de armazenamento."""
        self.files: list[File] = [] 
        self.threshold = 5

    def put(self, file):
        """
        Adiciona um arquivo à memória principal, removendo o mais antigo se o limite for atingido.
        
        Args:
            file (File): Arquivo a ser adicionado.
        """
        if len(self.files) == self.threshold:
            _ = self.files.pop(0)
        self.files.append(file)

    def remove(self, file):
        """
        Remove um arquivo da memória principal.

        Args:
            file (File): Arquivo a ser removido.
        """
        self.files.remove(file)

    def list(self):
        """Lista todos os arquivos atualmente na memória principal."""
        [print(file) for file in self.files]


class File():
    def __init__(self, name: str, owner: str, disk : Disk):
        """
        Inicializa um arquivo com nome, proprietário, datas de criação e atualização, 
        um i-node e um estado indicando se o arquivo está aberto ou não.

        Args:
            name (str): Nome do arquivo.
            owner (str): Proprietário do arquivo.
            disk (Disk): Disco onde o arquivo está armazenado.
        """
        self.name = name
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.owner = owner
        self.index_node = IndexNode()
        self.is_open = False
        self.disk = disk

    def open(self, pm: PrincipalMemory):
        """
        Abre o arquivo e o adiciona à memória principal.

        Args:
            pm (PrincipalMemory): Memória principal onde o arquivo será armazenado.
        """
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
        """
        Fecha o arquivo e o remove da memória principal.

        Args:
            pm (PrincipalMemory): Memória principal de onde o arquivo será removido.
        """
        pm.remove(self)
        self.is_open = False

    def read(self):
        """
        Lê os dados do arquivo usando os ponteiros armazenados no i-node.

        Returns:
            str: Dados lidos do arquivo.

        Raises:
            Exception: Se o arquivo não estiver aberto.
        """
        if not self.is_open:
            raise Exception("File should be open for be read")

        result = ''
        for pointer in self.index_node.pointers:
            result += self.disk.get(pointer)
        return result

    def write(self, data: str):
        """
        Escreve dados no arquivo e atualiza o i-node com os blocos onde os dados estão armazenados.

        Args:
            data (str): Dados a serem escritos no arquivo.

        Raises:
            Exception: Se o arquivo não estiver aberto.
        """
        if not self.is_open:
            raise Exception("File should be open for be written")

        self.index_node.length += len(data)
        pointer_start = self.disk.store(data)

        for index in range(pointer_start, pointer_start + len(data), BLOCK_LEN):
            self.index_node.pointers.append(index)


class Directory():
    def __init__(self, name: str):
        """
        Inicializa um diretório com nome, arquivos e subdiretórios vazios, 
        e uma referência ao diretório pai.

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
        if file_name in self.files:
            raise Exception("File already exists.")
        file = File(file_name, owner, disk)
        self.files[file_name] = file
        print(f"Arquivo {file_name} criado com sucesso.")

    def create_directory(self, dir_name: str):
        """
        Cria um novo subdiretório dentro do diretório atual.

        Args:
            dir_name (str): Nome do novo subdiretório.

        Raises:
            Exception: Se o subdiretório já existir.
        """
        if dir_name in self.subdirectories:
            raise Exception("Directory already exists.")
        new_dir = Directory(dir_name)
        new_dir.parent = self
        self.subdirectories[dir_name] = new_dir
        print(f"Diretório {dir_name} criado com sucesso.")

    def list_contents(self):
        """Lista os arquivos e subdiretórios presentes no diretório."""
        print(f"Conteúdo do diretório {self.name}:")
        print("Arquivos:")
        for file_name in self.files:
            print(f"- {file_name}")
        print("Subdiretórios:")
        for dir_name in self.subdirectories:
            print(f"- {dir_name}")

    def move_file(self, file_name: str, target_directory: 'Directory'):
        """
        Move um arquivo para outro diretório.

        Args:
            file_name (str): Nome do arquivo a ser movido.
            target_directory (Directory): Diretório de destino.

        Raises:
            Exception: Se o arquivo não for encontrado.
        """
        if file_name not in self.files:
            raise Exception(f"Arquivo {file_name} não encontrado.")
        file = self.files.pop(file_name)
        target_directory.files[file_name] = file
        print(f"Arquivo {file_name} movido para {target_directory.name} com sucesso.")

    def navigate_to(self, dir_name: str) -> 'Directory':
        """
        Navega para um subdiretório específico ou para o diretório pai.

        Args:
            dir_name (str): Nome do diretório de destino (".." para o diretório pai ou "." para o atual).

        Returns:
            Directory: Diretório de destino.

        Raises:
            Exception: Se o subdiretório não for encontrado.
        """
        if dir_name == "..":
            return self.parent if self.parent else self
        if dir_name == ".":
            return self
        if dir_name in self.subdirectories:
            return self.subdirectories[dir_name]
        raise Exception(f"Diretório {dir_name} não encontrado.")
