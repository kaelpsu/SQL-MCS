import argparse
import os
from graph_generator import generate_graph_from_sql
from graph_generator import generate_graph_from_sql
from visualizer import visualize_custom_graph
from mcs_finder import find_maximum_common_subgraph, calculate_similarity_percentage

def read_queries_from_file(filepath: str) -> list:
    """
    Lê duas queries de um arquivo de texto.
    As queries devem ser separadas por um ponto e vírgula ';'.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            # Filtra strings vazias que podem surgir de múltiplos ';'
            queries = [q.strip() for q in content.split(';') if q.strip()]
            if len(queries) != 2:
                print(f"Erro: O arquivo '{filepath}' deve conter exatamente 2 queries SQL separadas por ';'.")
                return None
            return queries
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filepath}' não encontrado.")
        return None
    except Exception as e:
        print(f"Ocorreu um erro ao ler o arquivo: {e}")
        return None

def main():
    """
    Ponto de entrada principal para a execução da bateria de testes.
    """
    parser = argparse.ArgumentParser(
        description="Compara duas queries SQL de um arquivo e calcula sua similaridade."
    )
    parser.add_argument(
        "files",
        metavar="ARQUIVO",
        nargs='+', # Aceita um ou mais argumentos de arquivo
        help="Caminho para um ou mais arquivos .txt contendo as queries a serem comparadas."
    )
    parser.add_argument(
        '--no-visualize',
        action='store_true',
        help="Desativa a exibição da janela de visualização do grafo MCS."
    )

    args = parser.parse_args()

    for filepath in args.files:
        print(f"--- Processando Caso de Teste: {os.path.basename(filepath)} ---")
        
        queries = read_queries_from_file(filepath)
        if not queries:
            print("-" * (len(os.path.basename(filepath)) + 29) + "\n")
            continue

        sql_a, sql_b = queries
        
        # Geração dos grafos
        graph_a = generate_graph_from_sql(sql_a)
        graph_b = generate_graph_from_sql(sql_b)

        print(f"Query A: {sql_a}")
        print(f"Query B: {sql_b}")
        print(f"Grafo A: {graph_a}")
        print(f"Grafo B: {graph_b}")

        # Encontrar MCS e calcular similaridade
        mcs = find_maximum_common_subgraph(graph_a, graph_b)

        if mcs and len(mcs.nodes) > 0:
            similarity = calculate_similarity_percentage(graph_a, graph_b, mcs)
            print(f"\n✅ Nível de Equivalência: {similarity:.2f}%")
            print(f"   (Encontrado um MCS com {len(mcs.nodes)} nós)")
            if not args.no_visualize:
                visualize_custom_graph(mcs, f"MCS - {os.path.basename(filepath)}")
        else:
            print("\n❌ Nível de Equivalência: 0.00%")
            print("   (Nenhum subgrafo comum significativo encontrado)")
        
        print("-" * (len(os.path.basename(filepath)) + 29) + "\n")


if __name__ == "__main__":
    main()