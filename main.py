# TODO: Simular arquivos aberto na memoria ram armazenando 
# os arquivos que foram abertos
from datetime import datetime
from typing import Union
from model import Disk, PrincipalMemory, Directory

def main():
    # Inicializa o disco (simulado)
    disk = Disk()

    # Inicializa a memória principal
    pm = PrincipalMemory()

    # Cria um diretório raiz
    root = Directory("root")

    # Testando a criação de arquivos
    print("\n=== Criando Arquivos ===")
    root.create_file("arquivo1.txt", "usuario1", disk)  # Cria arquivo no diretório raiz
    root.create_file("arquivo2.txt", "usuario2", disk)

    # Listar o conteúdo do diretório raiz após a criação dos arquivos
    print("\n=== Listando Conteúdo do Diretório Raiz ===")
    root.list_contents()  # Deve mostrar os arquivos criados

    # Testando a criação de subdiretórios
    print("\n=== Criando Subdiretórios ===")
    root.create_directory("dir1")  # Cria um subdiretório
    root.create_directory("dir2")

    # Listando o conteúdo do diretório raiz após a criação dos subdiretórios
    print("\n=== Listando Conteúdo do Diretório Raiz ===")
    root.list_contents()  # Deve mostrar arquivos e subdiretórios

    # Navegando para o subdiretório "dir1"
    print("\n=== Navegando para 'dir1' ===")
    dir1 = root.navigate_to("dir1")
    dir1.list_contents()  # Deve estar vazio inicialmente

    # Criando um arquivo dentro de "dir1"
    print("\n=== Criando Arquivo Dentro de 'dir1' ===")
    dir1.create_file("arquivo3.txt", "usuario1", disk)
    dir1.list_contents()  # Deve listar o arquivo "arquivo3.txt"

    # Navegando de volta para o diretório raiz
    print("\n=== Navegando de Volta para o Diretório Raiz ===")
    root = dir1.navigate_to("..")
    root.list_contents()  # Deve mostrar o conteúdo original do diretório raiz

    # Testando movimentação de arquivos
    print("\n=== Movendo 'arquivo1.txt' para 'dir2' ===")
    dir2 = root.navigate_to("dir2")
    root.move_file("arquivo1.txt", dir2)

    # Listar conteúdo após a movimentação
    print("\n=== Conteúdo de 'dir2' Após Mover 'arquivo1.txt' ===")
    dir2.list_contents()  # "arquivo1.txt" deve estar em dir2

    # Testando a abertura de um arquivo, leitura e escrita
    print("\n=== Abrindo, Lendo e Escrevendo no Arquivo ===")
    file = root.files.get("arquivo2.txt")  # Pega referência ao arquivo "arquivo2.txt"
    if file:
        file.open(pm)  # Abre o arquivo e adiciona na memória principal
        file.write("Olá, este é o conteúdo do arquivo.")  # Escreve no arquivo
        print("Conteúdo do arquivo após a escrita:", file.read())  # Lê o conteúdo do arquivo
        file.write(" Adicionando mais dados.")  # Escreve mais dados
        print("Conteúdo do arquivo após mais escrita:", file.read())  # Lê o novo conteúdo
        file.close(pm)  # Fecha o arquivo

    # Listando arquivos na memória principal
    print("\n=== Arquivos na Memória Principal ===")
    pm.list()  # Lista todos os arquivos abertos na memória

    # Testando a exclusão de arquivos
    print("\n=== Excluindo 'arquivo2.txt' ===")
    if file:
        file.delete()  # Deleta o arquivo e libera os blocos de dados
        root.list_contents()  # "arquivo2.txt" deve ser removido do diretório raiz

if __name__ == "__main__":
    main()
