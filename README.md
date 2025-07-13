# Análise de Similaridade de Consultas SQL via Subgrafo Máximo Comum

Este projeto oferece uma ferramenta para analisar e quantificar a similaridade entre duas consultas SQL. Ele transforma as consultas em representações de grafos hierárquicos e, em seguida, utiliza uma implementação do algoritmo VF2 para encontrar o Subgrafo Máximo Comum (MCS) entre eles. O tamanho do MCS é usado para calcular uma métrica percentual de equivalência.

## 🚀 Funcionalidades Principais

- **Parsing Robusto de SQL**: Utiliza a biblioteca sqlglot para converter strings SQL em Árvores de Sintaxe Abstrata (AST), lidando de forma nativa com aliases e estruturas complexas.
- **Geração de Grafo Hierárquico**: Converte a AST em um grafo direcionado com uma estrutura de árvore lógica (QUERY -> TABLE -> COLUMN -> FILTER), utilizando uma estrutura de dados customizada.
- **Busca por Subgrafo Máximo Comum (MCS)**: Implementa uma versão customizada do algoritmo VF2 para encontrar o maior subgrafo estrutural e semanticamente comum entre duas consultas.
- **Cálculo de Similaridade Percentual**: Fornece uma métrica quantitativa (0% a 100%) que indica o grau de equivalência entre as consultas, normalizado pelo tamanho da menor consulta.
- **Visualização de Grafos**: Utiliza matplotlib e networkx para gerar visualizações claras dos grafos e dos subgrafos comuns encontrados.

## 📂 Estrutura do Projeto

```
/src
|-- main.py                     # Ponto de entrada, executa os testes e a análise
|-- vf2.py                      # Contém a implementação do VF2 e a lógica de busca pelo MCS
|-- graph_generator.py          # Contém a lógica para converter SQL em um grafo
|-- graph_structures.py         # Define as classes customizadas `Node` e `Graph`
|-- requirements.txt            # Lista de dependências do projeto
|/testes
|   |-- caso_1.txt              # Arquivo de teste com duas queries
|   |-- caso_2.txt              # Outro arquivo de teste

```

## ⚙️ Instalação e Dependências

Para executar este projeto, é recomendado o uso de um ambiente virtual para gerenciar as dependências.

### Clone o repositório:

```bash
git clone https://github.com/kaelpsu/SQL-MCS.git
cd SQL-MCS
```

### Crie e ative um ambiente virtual (opcional):

```bash
# Para Unix/macOS
python3 -m venv venv
source venv/bin/activate
```

### Instale as dependências a partir do arquivo requirements.txt:

```bash
pip install -r requirements.txt
```

As principais dependências são:

- **sqlglot**: Para o parsing de SQL.
- **networkx**: Usado como ponte para a visualização de grafos.
- **matplotlib**: Para gerar os gráficos e visualizações.

## ▶️ Como Executar

O script principal é projetado para ser executado via linha de comando, recebendo como argumento o caminho para um arquivo de texto que contém as duas consultas SQL a serem comparadas. As consultas dentro do arquivo devem ser separadas por um ponto e vírgula (`;`).

### Comando de Execução:

```bash
python main.py /tests/caso_x.txt
```

### Exemplo:

```bash
python main.py tests/caso_isomorfismo.txt
```

O script irá imprimir no terminal a análise dos grafos, o nível de equivalência percentual e, opcionalmente, exibir uma janela com a visualização do Subgrafo Máximo Comum encontrado.

## 🛠️ Como Funciona (Detalhes Técnicos)

O processo é dividido em três etapas principais:

### 1. Parsing e Geração do Grafo

A função `generate_tree_from_sql` recebe uma string SQL. Primeiro, o `sqlglot` a transforma em uma AST. Em seguida, o código percorre essa árvore para construir um grafo hierárquico, garantindo que a estrutura reflita a lógica da consulta:

- A raiz é a própria **QUERY**.
- Seus filhos são as **tabelas (TABLE)**.
- Os filhos das tabelas são as **colunas (COLUMN)**.
- Os filhos das colunas são os **filtros (FILTER)** aplicados a elas.

Essa estrutura garante que a comparação posterior seja robusta a variações sintáticas.

### 2. Busca pelo Subgrafo Máximo Comum (MCS)

A classe `VF2Matcher` foi implementada do zero seguindo os princípios do algoritmo VF2, mas com uma modificação crucial: em vez de parar no primeiro isomorfismo encontrado, ela explora o espaço de busca para encontrar o maior mapeamento parcial válido.

Ela utiliza uma função de correspondência semântica (`node_match`) que garante que dois nós só possam ser mapeados se tiverem o mesmo tipo (TABLE, COLUMN, etc.) e o mesmo rótulo (users, id, etc.). Isso impede o casamento de entidades diferentes (ex: users.id com orders.id).

### 3. Cálculo da Similaridade

Após encontrar o MCS, uma métrica de similaridade é calculada para quantificar o resultado:

```
Similaridade (%) = (Número de Nós no MCS / Número de Nós no Grafo Menor) * 100
```

Esta fórmula responde à pergunta: "Qual a porcentagem da consulta menor que está contida na consulta maior?".

Um resultado de **100%** indica que a consulta menor é um subconjunto completo (ou isomorfa) da maior, sinalizando uma forte equivalência ou redundância.