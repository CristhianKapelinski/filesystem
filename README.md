
# Simulador de Sistema de Arquivos

Este é um simulador de sistema de arquivos escrito em Python que utiliza uma estrutura de alocação contígua para gerenciar arquivos e diretórios em um disco virtual. O programa é acessado através de uma interface de linha de comando, permitindo criar diretórios e arquivos, navegar na estrutura de diretórios, e manipular o conteúdo armazenado no disco.

## Funcionalidades

O simulador implementa as seguintes funcionalidades:
1. **Criar diretórios (`mkdir`)**: Cria novos diretórios no sistema de arquivos.
2. **Criar arquivos (`create`)**: Cria arquivos no disco, alocando blocos contíguos.
3. **Navegar entre diretórios (`cd`)**: Permite navegar entre diretórios.
4. **Listar conteúdo (`ls`)**: Lista arquivos e subdiretórios no diretório atual.
5. **Exibir árvore de diretórios (`tree`)**: Mostra toda a estrutura hierárquica de diretórios e arquivos.
6. **Ler e escrever arquivos (`read` e `write`)**: Manipula o conteúdo lógico de arquivos.
7. **Excluir arquivos ou diretórios (`delete`)**: Remove arquivos ou diretórios.
8. **Exibir informações do disco (`info`)**: Mostra o uso de espaço no disco e a memória disponível.
9. **Exibir estado da memória (`mostrar_memoria`)**: Mostra graficamente os blocos de memória.

## Estruturas de Dados

### 1. **Bloco**
Cada bloco representa uma unidade do disco virtual e contém:
- `ocupado`: Indica se o bloco está ocupado.
- `conteudo`: Nome abreviado do arquivo que ocupa o bloco.

### 2. **Arquivo**
Cada arquivo contém:
- `nome`: Nome completo do arquivo.
- `tamanho`: Número de blocos ocupados.
- `blocos`: Lista de índices dos blocos ocupados no disco.
- `conteudo`: Dados armazenados no arquivo.

### 3. **Diretorio**
Cada diretório contém:
- `nome`: Nome do diretório.
- `subdiretorios`: Dicionário de subdiretórios.
- `arquivos`: Dicionário de arquivos no diretório.

### 4. **SistemaArquivos**
Gerencia o disco e a hierarquia de arquivos/diretórios, utilizando:
- `disco`: Lista de blocos representando o disco virtual.
- `raiz`: Diretório raiz do sistema.
- `diretorio_atual`: Diretório em uso atualmente.
- `caminho_atual`: Caminho do diretório atual.
- `log`: Lista de logs das operações realizadas.

## Comandos Suportados

### Navegação
- **`cd <caminho>`**: Navega para o diretório especificado.
- **`ls`**: Lista arquivos e subdiretórios no diretório atual.
- **`tree`**: Exibe toda a estrutura de diretórios e arquivos a partir da raiz.

### Manipulação de Diretórios e Arquivos
- **`mkdir <nome>`**: Cria um novo diretório.
- **`create <nome> <tamanho>`**: Cria um novo arquivo com o nome e tamanho especificados.
- **`delete <nome>`**: Exclui o arquivo ou diretório especificado.
- **`write <nome> <conteudo>`**: Escreve conteúdo em um arquivo.
- **`read <nome>`**: Lê o conteúdo de um arquivo.

### Informações do Sistema
- **`info`**: Exibe o tamanho total, espaço usado, e espaço livre no disco.
- **`mostrar_memoria`**: Mostra os blocos do disco e os arquivos que os ocupam.

### Finalização
- **`exit`**: Finaliza a execução do programa e grava os logs em um arquivo `log.txt`.

## Exemplo de Uso

1. **Criação de Diretórios e Arquivos**
   ```bash
   mkdir docs
   cd docs
   mkdir teste
   cd teste
   create A1.txt 20
   ```

2. **Exclusão de Arquivo**
   ```bash
   delete A1.txt
   ```

3. **Exibição de Estado**
   ```bash
   info
   tree
   ```

## Requisitos

- Python 3.6 ou superior.

## Como Executar

1. Clone ou baixe o código para sua máquina local.
2. Execute o programa no terminal com o comando:
   ```bash
   python3 filesystem.py
   ```

3. Use os comandos na interface para interagir com o sistema de arquivos.

## Logs

Todas as operações realizadas são registradas em um arquivo `log.txt` gerado ao sair do programa com o comando `exit`.

## Estrutura do Disco Virtual

- Cada bloco no disco é representado graficamente em uma grade de 10 por linha.
- Os blocos livres são exibidos como `[  ]`.
- Os blocos ocupados mostram o nome abreviado do arquivo (por exemplo, `[A1]`).

## Limitações

1. O método de alocação é contíguo, podendo levar a fragmentação externa.
2. Não há suporte para permissões ou atributos avançados de arquivos.
3. A exclusão de diretórios não verifica se há arquivos dentro.
