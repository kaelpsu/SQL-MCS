import unittest

from src.graph_structures import Node, Graph  

class TestNode(unittest.TestCase):
    def test_repr(self):
        node = Node(1, 'type', 'label')
        expected = "Node(id=1, type='type', label='label')"
        self.assertEqual(repr(node), expected)

    def test_eq_same_id(self):
        node1 = Node(1, 'type1', 'label1')
        node2 = Node(1, 'type2', 'label2')
        self.assertEqual(node1, node2)

    def test_eq_different_id(self):
        node1 = Node(1, 'type', 'label')
        node2 = Node(2, 'type', 'label')
        self.assertNotEqual(node1, node2)

    def test_eq_not_node(self):
        node = Node(1, 'type', 'label')
        self.assertNotEqual(node, object())

    def test_hash(self):
        node1 = Node(1, 'type', 'label')
        node2 = Node(1, 'type', 'label')
        self.assertEqual(hash(node1), hash(node2))

class TestGraph(unittest.TestCase):
    def setUp(self):
        self.graph = Graph()

    def test_add_node(self):
        nid1 = self.graph.add_node('t1', 'l1')
        nid2 = self.graph.add_node('t2', 'l2', value=123)
        self.assertEqual(nid1, 0)
        self.assertEqual(nid2, 1)
        self.assertEqual(len(self.graph), 2)
        self.assertIsInstance(self.graph.get_node(nid1), Node)
        self.assertIsNone(self.graph.get_node(99))

    def test_add_edge_and_neighbors(self):
        a = self.graph.add_node('t', 'a')
        b = self.graph.add_node('t', 'b')
        self.graph.add_edge(a, b)
        self.assertIn(b, self.graph.get_neighbors(a))
        self.assertEqual(self.graph.get_neighbors(b), set())

    def test_add_edge_invalid(self):
        a = self.graph.add_node('t', 'a')
        with self.assertRaises(ValueError):
            self.graph.add_edge(a, 99)
        with self.assertRaises(ValueError):
            self.graph.add_edge(99, a)

    def test_predecessors(self):
        a = self.graph.add_node('t', 'a')
        b = self.graph.add_node('t', 'b')
        c = self.graph.add_node('t', 'c')
        self.graph.add_edge(a, b)
        self.graph.add_edge(c, b)
        preds = self.graph.get_predecessors(b)
        self.assertEqual(preds, {a, c})
        self.assertEqual(self.graph.get_predecessors(a), set())

    def test_repr_and_len(self):
        self.assertEqual(repr(self.graph), "Graph(nodes=0, edges=0)")
        a = self.graph.add_node('x', 'y')
        b = self.graph.add_node('x', 'z')
        self.graph.add_edge(a, b)
        self.assertEqual(len(self.graph), 2)
        self.assertEqual(repr(self.graph), "Graph(nodes=2, edges=1)")

if __name__ == '__main__':
    unittest.main()
