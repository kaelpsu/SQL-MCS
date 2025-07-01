import matplotlib.pyplot as plt
import networkx as nx

def visualize_custom_graph(custom_graph: 'Graph'):
    """
    Converte a estrutura de grafo personalizada para um grafo networkx e o visualiza
    usando matplotlib.

    Args:
        custom_graph: Uma instância da sua classe Graph.
    """
    if not custom_graph or not custom_graph.nodes:
        print("Grafo vazio, nada para visualizar.")
        return

    # 1. Converter para um grafo networkx
    G_nx = nx.DiGraph() # Usamos DiGraph para respeitar a direção das arestas

    # Adiciona os nós com seus atributos
    for node_id, node_obj in custom_graph.nodes.items():
        G_nx.add_node(node_id, type=node_obj.node_type, label=node_obj.label)

    # Adiciona as arestas
    for from_id, neighbors in custom_graph.adjacency_list.items():
        for to_id in neighbors:
            G_nx.add_edge(from_id, to_id)

    # 2. Preparar estilos para a visualização
    # Define um mapa de cores para cada tipo de nó
    color_map = {
        'TABLE': 'skyblue',
        'COLUMN': 'lightgreen',
        'FILTER': 'salmon'
    }
    node_colors = [color_map.get(data['type'], 'grey') for _, data in G_nx.nodes(data=True)]

    # Pega os rótulos para exibição
    labels = nx.get_node_attributes(G_nx, 'label')

    # 3. Calcular um layout para os nós
    # O layout de mola (spring) é ótimo para ver a estrutura de clusters
    pos = nx.spring_layout(G_nx, seed=42, k=0.9)

    # 4. Desenhar o grafo com matplotlib
    plt.figure(figsize=(14, 9)) # Cria uma figura maior
    
    nx.draw(G_nx, pos, 
            with_labels=True, 
            labels=labels, 
            node_color=node_colors, 
            node_size=2500, 
            font_size=9, 
            font_weight='bold',
            arrowsize=20)
    
    plt.title("Visualização do Grafo da Consulta SQL", size=16)
    plt.show()