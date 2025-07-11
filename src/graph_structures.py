class Node:
    """Represents a node in the query graph."""
    def __init__(self, node_id, node_type, label, value=None, is_selected=False):
        self.node_id = node_id
        self.node_type = node_type
        self.label = label
        self.value = value
        self.is_selected = is_selected

    def __repr__(self):
        selected_str = ", selected=True" if self.is_selected else ""
        return (f"Node(id={self.node_id}, type='{self.node_type}', "
                f"label='{self.label}'{selected_str})")

    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.node_id == other.node_id

    def __hash__(self):
        return hash(self.node_id)

class Graph:
    """Represents a query as a directed graph."""
    def __init__(self):
        self.nodes = {}
        self.adjacency_list = {}
        self._next_node_id = 0

    def add_node(self, node_type, label, value=None, is_selected=False):
        """Adds a new node to the graph and returns its ID."""
        node_id = self._next_node_id
        
        
        new_node = Node(node_id, node_type, label, value, is_selected)
        
        self.nodes[node_id] = new_node
        self.adjacency_list[node_id] = set()
        self._next_node_id += 1
        return node_id

    def add_edge(self, from_node_id, to_node_id):
        """Adds a directed edge between two nodes."""
        if from_node_id in self.adjacency_list and to_node_id in self.nodes:
            self.adjacency_list[from_node_id].add(to_node_id)
        else:
            raise ValueError("One or both nodes not in the graph.")

    def get_node(self, node_id):
        """Retrieves a node object by its ID."""
        return self.nodes.get(node_id)

    def get_neighbors(self, node_id):
        """Returns a set of neighbor IDs for a given node."""
        return self.adjacency_list.get(node_id, set())
    
    def get_predecessors(self, node_id):
        """Returns a set of predecessor IDs for a given node."""
        predecessors = set()
        for u, neighbors in self.adjacency_list.items():
            if node_id in neighbors:
                predecessors.add(u)
        return predecessors
    
    def subgraph(self, node_ids_to_keep: list) -> 'Graph':
        """
        Cria um novo grafo contendo apenas os nós especificados e as arestas entre eles.
        """
        new_graph = Graph()
        old_to_new_id_map = {}

        # Adiciona os nós selecionados ao novo grafo
        for old_id in node_ids_to_keep:
            if old_id in self.nodes:
                old_node = self.nodes[old_id]
                new_id = new_graph.add_node(
                    node_type=old_node.node_type,
                    label=old_node.label,
                    value=old_node.value,
                    is_selected=old_node.is_selected
                )
                old_to_new_id_map[old_id] = new_id

        # Adiciona as arestas que existem entre os nós selecionados
        for old_from_id, new_from_id in old_to_new_id_map.items():
            for old_to_id in self.adjacency_list.get(old_from_id, set()):
                if old_to_id in old_to_new_id_map:
                    new_to_id = old_to_new_id_map[old_to_id]
                    new_graph.add_edge(new_from_id, new_to_id)
        
        return new_graph

    def __len__(self):
        return len(self.nodes)

    def __repr__(self):
        return (f"Graph(nodes={len(self.nodes)}, "
                f"edges={sum(len(v) for v in self.adjacency_list.values())})")