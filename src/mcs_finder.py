import networkx as nx
import matplotlib.pyplot as plt
from graph_structures import Graph
from graph_generator import generate_graph_from_sql
from vf2 import VF2Matcher
from visualizer import visualize_custom_graph

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

### Casos de Teste ###
if __name__ == "__main__":
    # --- Função de ajuda para executar e imprimir um teste ---
    def run_test_case(title, sql_a, sql_b):
        print(f"--- {title} ---")
        
        graph_a = generate_graph_from_sql(sql_a)
        graph_b = generate_graph_from_sql(sql_b)

        print(f"Grafo A (da query A): {graph_a}")
        print(f"Grafo B (da query B): {graph_b}")

        mcs = find_maximum_common_subgraph(graph_a, graph_b)

        if mcs and len(mcs.nodes) > 0:
            similarity = calculate_similarity_percentage(graph_a, graph_b, mcs)
            print(f"Query A: {sql_a}")
            print(f"Query B: {sql_b}")
            print(f"\n✅ Nível de Equivalência: {similarity:.2f}%")
            print(f"   (Encontrado um MCS com {len(mcs.nodes)} nós)")
            visualize_custom_graph(mcs, f"MCS - {title}") # Descomente para ver o grafo
        else:
            print("\n❌ Nível de Equivalência: 0.00%")
            print("   (Nenhum subgrafo comum significativo encontrado)")
        print("-" * (len(title) + 4))


    # --- CASO 1: Isomorfismo Completo (100% de similaridade) ---
    sql_iso_1 = "SELECT id, name FROM users WHERE status = 'active'"
    sql_iso_2 = "SELECT name, id FROM users WHERE status = 'active'"
    run_test_case("CASO 1: Isomorfismo Completo", sql_iso_1, sql_iso_2)


    # --- CASO 2: Subconsulta Direta (Alta similaridade) ---
    sql_sub_1 = "SELECT u.id, u.name, u.email FROM users u WHERE u.status = 'active' AND u.age > 25"
    sql_sub_2 = "SELECT u.name FROM users u WHERE u.status = 'active'"
    run_test_case("CASO 2: Subconsulta Direta", sql_sub_1, sql_sub_2)


    # --- CASO 3: Similaridade Parcial (Média similaridade) ---
    sql_part_1 = "SELECT id, name, email FROM users WHERE status = 'active'"
    sql_part_2 = "SELECT id, name, age FROM users WHERE status = 'active'"
    run_test_case("CASO 3: Similaridade Parcial", sql_part_1, sql_part_2)


    # --- CASO 4: Rótulos Diferentes (Baixa/Nula similaridade) ---
    sql_diff_1 = "SELECT c.name, o.amount FROM customers c JOIN orders o ON c.id = o.customer_id WHERE c.state = 'CA'"
    sql_diff_2 = "SELECT u.name, p.price FROM users u JOIN products p ON u.id = p.user_id WHERE u.status = 'active'"
    run_test_case("CASO 4: Rótulos Diferentes", sql_diff_1, sql_diff_2)

    # --- CASO 5: Rótulos Totalmente Diferentes (Nenhuma similaridade) ---
    sql_diff_1 = "SELECT c.address, o.amount FROM customers c JOIN orders o ON c.id = o.customer_id WHERE c.state = 'CA'"
    sql_diff_2 = "SELECT u.name, p.price FROM users u JOIN products p ON u.cpf > p.user_id WHERE u.status IS NOT 'active'"
    run_test_case("CASO 4: Rótulos Diferentes", sql_diff_1, sql_diff_2)