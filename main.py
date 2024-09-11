# TODO: Simular arquivos aberto na memoria ram armazenando 
# os arquivos que foram abertos
from model import Disk, File, PrincipalMemory

principal_memory = PrincipalMemory()
disk = Disk()
file1 = File("a.txt", "arthur", disk)
file2 = File("b.txt", "jon", disk)
file3 = File("c.txt", "jon&arthur", disk)

file1.open(principal_memory)
file1.write("1" * 24)
print(file1.read())

file2.open(principal_memory)
file2.write("2" * 5)
print(file2.read())

file3.open(principal_memory)
file3.write("3" * 5)
print(file3.read())

file1.write("1" * 2)
print(file1.read())

file3.write("5" * 10)
print(file3.read())

file1.close(principal_memory)
file2.close(principal_memory)
file3.close(principal_memory)
