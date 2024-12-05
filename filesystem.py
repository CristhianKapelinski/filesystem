class Bloco:
    """Representa um bloco no disco virtual."""
    def __init__(self):
        self.ocupado = False
        self.conteudo = None

class Arquivo:
    """Representa um arquivo no sistema de arquivos."""
    def __init__(self, nome, tamanho, blocos):
        self.nome = nome
        self.tamanho = tamanho
        self.blocos = blocos
        self.conteudo = ""

class Diretorio:
    """Representa um diretório no sistema de arquivos."""
    def __init__(self, nome):
        self.nome = nome
        self.subdiretorios = {}
        self.arquivos = {}

class SistemaArquivos:
    """Simula um sistema de arquivos com alocação contígua."""
    def __init__(self, tamanho_disco):
        self.tamanho_disco = tamanho_disco
        self.disco = [Bloco() for _ in range(tamanho_disco)]
        self.raiz = Diretorio("/")
        self.diretorio_atual = self.raiz
        self.caminho_atual = "/"
        self.log = []

    def encontrar_blocos_livres(self, tamanho):
        """Encontra uma sequência de blocos livres para alocação contígua."""
        livres = 0
        inicio = -1
        for i in range(self.tamanho_disco):
            if not self.disco[i].ocupado:
                if livres == 0:
                    inicio = i
                livres += 1
                if livres == tamanho:
                    return list(range(inicio, inicio + tamanho))
            else:
                livres = 0
        return None

    def mostrar_memoria(self):
        """Exibe o estado atual da memória (disco) com detalhes sobre a ocupação de cada bloco."""
        print("Estado atual do disco virtual:")
        print("Legenda: [  ] = Livre | Nome do Arquivo = Ocupado\n")
        
        # Criação de um mapa dos blocos ocupados
        mapa_blocos = ["  " for _ in range(self.tamanho_disco)]
        for arquivo in self.diretorio_atual.arquivos.values():
            for bloco in arquivo.blocos:
                # Nome abreviado para exibição
                nome_abreviado = arquivo.nome[:2] if len(arquivo.nome) > 2 else arquivo.nome
                mapa_blocos[bloco] = nome_abreviado
        
        # Mostra os blocos em uma grade de 10 por linha
        linhas = [
            "".join(f"[{mapa_blocos[i]}]" for i in range(j, min(j + 10, self.tamanho_disco)))
            for j in range(0, self.tamanho_disco, 10)
        ]
        for linha in linhas:
            print(linha)
        print("-" * 40)

    def mkdir(self, nome):
        """Cria um novo diretório."""
        if nome in self.diretorio_atual.subdiretorios:
            print(f"Erro: Diretório '{nome}' já existe.")
            return
        self.diretorio_atual.subdiretorios[nome] = Diretorio(nome)
        self.log.append(f"Comando: mkdir {nome}\n- Diretório criado: {nome}")
        print(f"Diretório '{nome}' criado com sucesso.")

    def create(self, nome, tamanho):
        """Cria um novo arquivo."""
        if nome in self.diretorio_atual.arquivos:
            print(f"Erro: Arquivo '{nome}' já existe.")
            return
        blocos = self.encontrar_blocos_livres(tamanho)
        if not blocos:
            espaco_livre = sum(1 for bloco in self.disco if not bloco.ocupado)
            if espaco_livre >= tamanho:
                print(f"Erro: Espaço insuficiente devido à fragmentação para criar o arquivo '{nome}'.")
                self.log.append(f"Comando: create {nome} {tamanho}\n- Erro: Fragmentação externa (espaço livre: {espaco_livre} blocos, requerido: {tamanho}).")
            else:
                print(f"Erro: Espaço insuficiente para criar o arquivo '{nome}'.")
                self.log.append(f"Comando: create {nome} {tamanho}\n- Erro: Espaço insuficiente (espaço livre: {espaco_livre} blocos, requerido: {tamanho}).")
            self.mostrar_memoria()
            return
        for bloco in blocos:
            self.disco[bloco].ocupado = True
        novo_arquivo = Arquivo(nome, tamanho, blocos)
        self.diretorio_atual.arquivos[nome] = novo_arquivo
        self.log.append(f"Comando: create {nome} {tamanho}\n- Arquivo criado: {nome}\n- Blocos alocados: {blocos}")
        print(f"Arquivo '{nome}' criado com sucesso.")
        self.mostrar_memoria()

    def cd(self, nome):
        """Navega para um diretório."""
        if nome == "..":
            # Volta ao diretório raiz (simplificado para este caso)
            if self.diretorio_atual.nome != "/":
                self.diretorio_atual = self.raiz
                self.caminho_atual = "/"
            print("Navegando para o diretório raiz.")
        elif nome in self.diretorio_atual.subdiretorios:
            self.diretorio_atual = self.diretorio_atual.subdiretorios[nome]
            self.caminho_atual += f"{nome}/"
            print(f"Navegando para o diretório '{nome}'.")
        else:
            print(f"Erro: Diretório '{nome}' não encontrado.")
        self.log.append(f"Comando: cd {nome}")

    def ls(self):
        """Lista o conteúdo do diretório atual."""
        print("Conteúdo do diretório atual:")
        for subdir in self.diretorio_atual.subdiretorios:
            print(f"[DIR] {subdir}")
        for arquivo in self.diretorio_atual.arquivos:
            print(f"[FILE] {arquivo}")
        self.log.append("Comando: ls")

    def delete(self, nome):
        """Exclui um arquivo ou diretório."""
        if nome in self.diretorio_atual.arquivos:
            arquivo = self.diretorio_atual.arquivos.pop(nome)
            for bloco in arquivo.blocos:
                self.disco[bloco].ocupado = False
            self.log.append(f"Comando: delete {nome}\n- Arquivo '{nome}' excluído\n- Blocos liberados: {arquivo.blocos}")
            print(f"Arquivo '{nome}' excluído com sucesso.")
        elif nome in self.diretorio_atual.subdiretorios:
            del self.diretorio_atual.subdiretorios[nome]
            self.log.append(f"Comando: delete {nome}\n- Diretório '{nome}' excluído")
            print(f"Diretório '{nome}' excluído com sucesso.")
        else:
            print(f"Erro: '{nome}' não encontrado.")
        self.mostrar_memoria()
    
    def info(self):
        """Exibe informações do sistema de arquivos."""
        espaco_usado = sum(1 for bloco in self.disco if bloco.ocupado)
        espaco_livre = self.tamanho_disco - espaco_usado
        print(f"Tamanho total do disco: {self.tamanho_disco} blocos")
        print(f"Espaço usado: {espaco_usado} blocos")
        print(f"Espaço livre: {espaco_livre} blocos")
        self.log.append(f"Comando: info\n- Tamanho: {self.tamanho_disco}\n- Usado: {espaco_usado}\n- Livre: {espaco_livre}")
        self.mostrar_memoria()

    def write(self, nome, dados):
        """Escreve dados em um arquivo."""
        if nome not in self.diretorio_atual.arquivos:
            print(f"Erro: Arquivo '{nome}' não encontrado.")
            return
        arquivo = self.diretorio_atual.arquivos[nome]
        arquivo.conteudo = dados
        self.log.append(f"Comando: write {nome}\n- Dados escritos: {dados}")
        print(f"Dados escritos no arquivo '{nome}'.")

    def read(self, nome):
        """Lê dados de um arquivo."""
        if nome not in self.diretorio_atual.arquivos:
            print(f"Erro: Arquivo '{nome}' não encontrado.")
            return
        arquivo = self.diretorio_atual.arquivos[nome]
        print(f"Conteúdo do arquivo '{nome}': {arquivo.conteudo}")
        self.log.append(f"Comando: read {nome}")


# Loop interativo para comandos do usuário
def interface_linha_de_comando():
    tamanho_disco = 100  # Tamanho do disco virtual em blocos
    sistema = SistemaArquivos(tamanho_disco)

    print("Bem-vindo ao Simulador de Sistema de Arquivos!")
    print("Digite 'exit' para sair.")
    
    while True:
        comando = input(f"{sistema.caminho_atual}> ").strip()
        if comando == "exit":
            print("Encerrando o simulador. Até logo!")
            file = open("log.txt", "w")
            for linha in sistema.log:
                file.write(linha + "\n")
            file.close()
            break
        
        args = comando.split()
        cmd = args[0]

        if cmd == "mkdir" and len(args) > 1:
            sistema.mkdir(args[1])
        elif cmd == "create" and len(args) > 2:
            try:
                tamanho = int(args[2])
                sistema.create(args[1], tamanho)
            except ValueError:
                print("Erro: Tamanho inválido.")
        elif cmd == "cd" and len(args) > 1:
            sistema.cd(args[1])
        elif cmd == "ls":
            sistema.ls()
        elif cmd == "delete" and len(args) > 1:
            sistema.delete(args[1])
        elif cmd == "info":
            sistema.info()
        elif cmd == "write" and len(args) > 2:
            sistema.write(args[1], " ".join(args[2:]))
        elif cmd == "read" and len(args) > 1:
            sistema.read(args[1])
        else:
            print("Comando desconhecido ou argumentos insuficientes.")

# Inicia a interface de linha de comando
interface_linha_de_comando()
