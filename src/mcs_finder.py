from graph_structures import Graph
from vf2 import VF2Matcher

def find_maximum_common_subgraph(g1: Graph, g2: Graph):
    if not g1.nodes or not g2.nodes:
        print("Um ou ambos os grafos estão vazios.")
        return None

    # 1. Instancia nosso matcher local
    matcher = VF2Matcher(g1, g2)

    # 2. Encontra o maior mapeamento possível
    mcs_mapping = matcher.find_mcs_mapping()

    if not mcs_mapping:
        print("Nenhum subgrafo comum encontrado.")
        return None
    
    # 3. Usa o mapeamento para construir o subgrafo
    # As chaves do mapeamento são os nós do grafo que foi usado como base (g1 no matcher)
    if matcher.swapped:
        mcs_nodes_ids = list(mcs_mapping.keys())
        mcs_custom_graph = g2.subgraph(mcs_nodes_ids)
    else:
        mcs_nodes_ids = list(mcs_mapping.keys())
        mcs_custom_graph = g1.subgraph(mcs_nodes_ids)
    
    # 4. Converte para networkx apenas para visualização
    return mcs_custom_graph

def calculate_similarity_percentage(g1: Graph, g2: Graph, mcs_graph):
    """
    Calcula o nível de equivalência percentual com base no MCS.

    Args:
        g1: O primeiro grafo original (sua classe Graph).
        g2: O segundo grafo original (sua classe Graph).
        mcs_graph: O grafo MCS resultante.

    Returns:
        A porcentagem de similaridade.
    """
    # Determina o tamanho do MCS

    size_mcs = len(mcs_graph.nodes)

    if size_mcs == 0:
        return 0.0

    # Pega o tamanho dos grafos originais
    size_g1 = len(g1.nodes)
    size_g2 = len(g2.nodes)

    # Usa o tamanho do menor grafo como denominador para a porcentagem
    denominator = min(size_g1, size_g2)

    if denominator == 0:
        return 0.0

    similarity = (size_mcs / denominator) * 100
    return similarity