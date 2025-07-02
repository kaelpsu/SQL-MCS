import networkx as nx
import matplotlib.pyplot as plt
from src.graph_structures import Graph
from src.graph_generator import generate_graph_from_sql

def convert_to_networkx(custom_graph: Graph) -> nx.DiGraph:
    """
    Converte um objeto do nosso Graph personalizado para um DiGraph do networkx.
    """
    g_nx = nx.DiGraph()
    if not custom_graph:
        return g_nx

    # Adiciona nós com seus atributos para a correspondência semântica
    for node_id, node_obj in custom_graph.nodes.items():
        g_nx.add_node(node_id, type=node_obj.node_type, label=node_obj.label)

    # Adiciona as arestas
    for from_id, neighbors in custom_graph.adjacency_list.items():
        for to_id in neighbors:
            g_nx.add_edge(from_id, to_id)
            
    return g_nx

def node_match(node1_attrs, node2_attrs):
    """
    Função de correspondência semântica para o VF2.
    Retorna True se os nós forem considerados equivalentes.
    """
    return (node1_attrs['type'] == node2_attrs['type'] and 
            node1_attrs['label'] == node2_attrs['label'])

def find_maximum_common_subgraph(g1: Graph, g2: Graph):
    if g1.__len__() < g2.__len__():
        g1, g2 = g2, g1 

    nx_g1 = convert_to_networkx(g1)
    nx_g2 = convert_to_networkx(g2)
    
    if nx_g1.number_of_nodes() == 0 or nx_g2.number_of_nodes() == 0:
        print("Um ou ambos os grafos estão vazios.")
        return None

    gm = nx.algorithms.isomorphism.DiGraphMatcher(nx_g1, nx_g2, node_match=node_match)

    # Verifica se o grafo menor (g2) é isomorfo a um subgrafo do maior (g1)
    if not gm.subgraph_is_isomorphic():
        print("Nenhum subgrafo comum (isomórfico) encontrado.")
        return None

    largest_mapping = next(gm.subgraph_isomorphisms_iter())
            
    # --- A CORREÇÃO ESTÁ AQUI ---
    # Pegamos as CHAVES (keys) do mapeamento, que são os nós de g1.
    mcs_nodes = list(largest_mapping.keys())
    mcs_graph = nx_g1.subgraph(mcs_nodes)
    
    return mcs_graph

def visualize_networkx_graph(nx_graph: nx.DiGraph, title: str):
    """
    Função adaptada para visualizar um grafo networkx diretamente.
    """
    if not nx_graph or nx_graph.number_of_nodes() == 0:
        print("Grafo vazio para visualização.")
        return

    color_map = {'TABLE': 'skyblue', 'COLUMN': 'lightgreen', 'FILTER': 'salmon'}
    node_colors = [color_map.get(data['type'], 'grey') for _, data in nx_graph.nodes(data=True)]
    labels = nx.get_node_attributes(nx_graph, 'label')
    
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(nx_graph, seed=42, k=0.9)
    nx.draw(nx_graph, pos, labels=labels, with_labels=True, node_color=node_colors,
            node_size=3000, font_size=10, font_weight='bold', arrowsize=20)
    plt.title(title, size=16)
    plt.show()

### Casos de Teste ###
if __name__ == "__main__":
    # --- Caso de Teste 1: Subconsulta Direta ---
    print("--- CASO DE TESTE 1: Subconsulta Direta ---")
    sql1 = "SELECT u.id, u.name, u.email FROM users u WHERE u.status = 'active' AND u.age > 25"
    sql2 = "SELECT u.name FROM users u WHERE u.status = 'active'"

    # Gerar os grafos a partir das consultas SQL
    graph1 = generate_graph_from_sql(sql1)
    graph2 = generate_graph_from_sql(sql2)

    print(f"Grafo 1 (da query 1): {graph1}")
    print(f"Grafo 2 (da query 2): {graph2}")

    # Encontrar e exibir o MCS
    mcs = find_maximum_common_subgraph(graph1, graph2)

    if mcs:
        print("\n✅ Subgrafo Máximo Comum (MCS) Encontrado!")
        print(f"Nós no MCS: {list(mcs.nodes(data=True))}")
        print(f"Arestas no MCS: {list(mcs.edges())}")
        visualize_networkx_graph(mcs, "MCS - Caso de Teste 1")

    # --- Caso de Teste 2: Estruturas Parcialmente Diferentes ---
    print("\n\n--- CASO DE TESTE 2: Estrutura Similar, Rótulos Diferentes ---")
    sql3 = "SELECT c.name, o.amount FROM customers c JOIN orders o ON c.id = o.customer_id WHERE c.state = 'CA'"
    sql4 = "SELECT u.name, p.price FROM users u JOIN products p ON u.id = p.user_id WHERE u.status = 'active'"

    graph3 = generate_graph_from_sql(sql3)
    graph4 = generate_graph_from_sql(sql4)

    mcs2 = find_maximum_common_subgraph(graph3, graph4)
    
    if mcs2:
        print("\n✅ Subgrafo Máximo Comum (MCS) Encontrado!")
        print(f"Nós no MCS: {list(mcs2.nodes(data=True))}")
        print(f"Arestas no MCS: {list(mcs2.edges())}")
        visualize_networkx_graph(mcs2, "MCS - Caso de Teste 2")
    else:
        print("\n❌ Nenhum MCS encontrado, como esperado, pois as tabelas e filtros são diferentes.")