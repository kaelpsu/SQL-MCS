# Imports e suas classes de Grafo e Funções Geradoras
from graph_structures import Graph
from graph_generator import generate_graph_from_sql

# ==============================================================================
# Implementação do Algoritmo VF2
# ==============================================================================

class VF2Matcher:
    """
    Implementa o algoritmo VF2 para verificar o isomorfismo entre dois grafos,
    sendo compatível com a estrutura de grafo personalizada.
    """
    def __init__(self, g1: 'Graph', g2: 'Graph'):
        # Garante que g1 seja o grafo maior para otimização
        if len(g1.nodes) < len(g2.nodes):
            self.g1, self.g2 = g2, g1
            self.swapped = True
        else:
            self.g1, self.g2 = g1, g2
            self.swapped = False
        
        self.best_mapping = {}
        self.mapping = {}

    def _is_consistent(self, u1, v2):
        """
        Verifica a consistência semântica e estrutural ao adicionar o par (u1, v2).
        Isso combina as checagens ConsPT e CutPT.
        """
        # 1. Checagem de consistência semântica
        node1 = self.g1.nodes[u1]
        node2 = self.g2.nodes[v2]
        if node1.node_type != node2.node_type or node1.label != node2.label:
            return False

        # 2. Checagem de consistência estrutural (look-back)
        # Verifica se a vizinhança com os nós já mapeados é a mesma.
        for neighbor1 in self.g1.adjacency_list[u1]:
            if neighbor1 in self.mapping:
                if self.mapping[neighbor1] not in self.g2.adjacency_list[v2]:
                    return False
        
        for predecessor1 in self.g1.get_predecessors(u1):
            if predecessor1 in self.mapping:
                if self.mapping[predecessor1] not in self.g2.get_predecessors(v2):
                    return False

        # 3. Regras de corte / viabilidade (look-ahead / CutPT)
        t1_out = sum(1 for n in self.g1.adjacency_list[u1] if n in self.g1_term_out)
        t2_out = sum(1 for n in self.g2.adjacency_list[v2] if n in self.g2_term_out)
        if t1_out > t2_out:
            return False

        t1_in = sum(1 for n in self.g1.get_predecessors(u1) if n in self.g1_term_in)
        t2_in = sum(1 for n in self.g2.get_predecessors(v2) if n in self.g2_term_in)
        if t1_in > t2_in:
            return False
        
        return True

    def _compute_candidate_pairs(self):
        """
        Calcula o conjunto de pares candidatos (Pm) para estender o mapeamento.
        """
        if self.mapping:
            # Conjuntos terminais de saída (T1(m) e T2(m))
            self.g1_term_out = set()
            mapped_g1_nodes = self.mapping.keys()
            for u1 in mapped_g1_nodes:
                self.g1_term_out.update(self.g1.adjacency_list[u1])
            self.g1_term_out -= set(mapped_g1_nodes)

            self.g2_term_out = set()
            mapped_g2_nodes = self.mapping.values()
            for v2 in mapped_g2_nodes:
                self.g2_term_out.update(self.g2.adjacency_list[v2])
            self.g2_term_out -= set(mapped_g2_nodes)
            
            # Conjuntos terminais de entrada
            self.g1_term_in = set()
            for u1 in mapped_g1_nodes:
                 self.g1_term_in.update(self.g1.get_predecessors(u1))
            self.g1_term_in -= set(mapped_g1_nodes)
            
            self.g2_term_in = set()
            for v2 in mapped_g2_nodes:
                 self.g2_term_in.update(self.g2.get_predecessors(v2))
            self.g2_term_in -= set(mapped_g2_nodes)

            # Se houver nós terminais, os candidatos vêm deles
            if self.g1_term_out and self.g2_term_out:
                return sorted([(u, v) for u in self.g1_term_out for v in self.g2_term_out])

        # Se não, os candidatos são todos os nós não mapeados (primeira iteração)
        unmapped_g1 = set(self.g1.nodes.keys()) - set(self.mapping.keys())
        unmapped_g2 = set(self.g2.nodes.keys()) - set(self.mapping.values())
        return sorted([(u, v) for u in unmapped_g1 for v in unmapped_g2])

    def _solve(self):
        """
        Função recursiva principal que implementa o backtracking.
        """
        if len(self.mapping) > len(self.best_mapping):
            self.best_mapping = self.mapping.copy()

        candidate_pairs = self._compute_candidate_pairs()
        
        for u1, v2 in candidate_pairs:
            if self._is_consistent(u1, v2):
                self.mapping[u1] = v2
                self._solve() # Continua a busca recursivamente
                del self.mapping[u1] # Backtrack

    def find_mcs_mapping(self):
        """
        Ponto de entrada para iniciar a busca pelo MCS.
        """
        self.mapping = {}
        self.best_mapping = {}
        self.g1_term_in = self.g1_term_out = self.g2_term_in = self.g2_term_out = set()
        self._solve()
        
        # Se os grafos foram trocados, inverte o mapeamento final
        if self.swapped:
            return {v: k for k, v in self.best_mapping.items()}
        return self.best_mapping