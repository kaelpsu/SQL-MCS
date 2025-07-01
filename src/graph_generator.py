import sqlglot
from sqlglot import exp
import graph_structures
from graph_structures import Graph  # Importa a classe Graph do módulo structures
import sql_extractor
from sql_extractor import get_clauses_from_ast
import matplotlib.pyplot as plt

from visualizer import visualize_custom_graph # Opcional, para visualização

def generate_graph_from_sql(sql_string: str):
    """
    Versão melhorada do Algoritmo 2.
    Gera um grafo estruturado a partir de uma string SQL.

    Args:
        sql_string: A consulta SQL a ser processada.

    Returns:
        Um objeto de grafo networkx representando a consulta.
    """
    try:
        ast = sqlglot.parse_one(sql_string)
    except Exception as e:
        print(f"Erro ao fazer o parsing da query: {e}")
        return None

    G = Graph()

    # Dicionário para mapear nomes lógicos (ex: 'users') para IDs numéricos (ex: 0)
    name_to_id_map = {}

    # Cria um mapa para resolver aliases de tabelas
    alias_map = {}
    for table in ast.find_all(exp.Table):
        # Mapeia o alias para o nome real da tabela
        if table.alias:
            alias_map[table.alias] = table.name
        # Mapeia o próprio nome da tabela para ele mesmo, para tabelas sem alias
        alias_map[table.name] = table.name

    # 1. Adiciona nós para cada tabela
    # Usamos os valores do mapa de alias para evitar adicionar o alias como uma tabela
    for real_table_name in set(alias_map.values()):
        if real_table_name not in name_to_id_map:
            table_id = G.add_node(node_type='TABLE', label=real_table_name)
            name_to_id_map[real_table_name] = table_id

    # 2. Adiciona nós para cada coluna e cria arestas para suas tabelas
    for column in ast.find_all(exp.Column):
        column_name = column.name
        # Resolve o alias da tabela para encontrar o nome real
        table_alias = column.table or list(alias_map.keys())[0]
        real_table_name = alias_map.get(table_alias)
        
        if not real_table_name: continue # Ignora colunas que não conseguimos mapear
        
        column_node_name = f"{real_table_name}.{column_name}"
        if column_node_name not in name_to_id_map:
            column_id = G.add_node(node_type='COLUMN', label=column_name)
            name_to_id_map[column_node_name] = column_id
            
            # Adiciona aresta da tabela para a coluna
            if real_table_name in name_to_id_map:
                table_id = name_to_id_map[real_table_name]
                G.add_edge(table_id, column_id)

    # 3. Adiciona nós de filtro baseados na cláusula WHERE
    where_clause = ast.find(exp.Where)
    if where_clause:
        in_nodes, equals_nodes, notnull_nodes = get_clauses_from_ast(where_clause.this)

        # Mapeia colunas de volta para seus IDs no grafo
        all_columns = {c.name: alias_map.get(c.table) for c in ast.find_all(exp.Column)}
        
        # Para cada coluna em uma cláusula, cria um nó de filtro e o conecta
        for col_name in equals_nodes:
            table_name = all_columns.get(col_name)
            column_node_name = f"{table_name}.{col_name}"
            if column_node_name in name_to_id_map:
                column_id = name_to_id_map[column_node_name]
                filter_id = G.add_node(node_type='FILTER', label='EQUALS')
                G.add_edge(column_id, filter_id)

        for col_name in in_nodes:
            table_name = all_columns.get(col_name)
            column_node_name = f"{table_name}.{col_name}"
            if column_node_name in name_to_id_map:
                column_id = name_to_id_map[column_node_name]
                filter_id = G.add_node(node_type='FILTER', label='IN')
                G.add_edge(column_id, filter_id)

        for col_name in notnull_nodes:
            table_name = all_columns.get(col_name)
            column_node_name = f"{table_name}.{col_name}"
            if column_node_name in name_to_id_map:
                column_id = name_to_id_map[column_node_name]
                filter_id = G.add_node(node_type='FILTER', label='NOT_NULL')
                G.add_edge(column_id, filter_id)
            
    return G

# --- Demonstração de uso ---
if __name__ == "__main__":
    sql_query = "SELECT u.id, u.name FROM users u WHERE u.status = 'active' AND u.age IS NOT NULL"
    
    print(f"Gerando grafo para a query: {sql_query}\n")
    my_graph = generate_graph_from_sql(sql_query)

    if my_graph:
        print("--- Representação do Grafo ---")
        print(my_graph)
        
        print("\n--- Nós do Grafo Gerado ---")
        for node_id in my_graph.nodes:
            print(my_graph.nodes[node_id])
        
        print("\n--- Arestas do Grafo Gerado (Lista de Adjacência) ---")
        for node_id, neighbors in my_graph.adjacency_list.items():
            if neighbors:
                print(f"Nó {node_id} -> {neighbors}")
                
        visualize_custom_graph(my_graph)