from testify import *
from deploy.dag.digraph import *
from deploy.dag.edge import *
from deploy.dag.vertex import *


class DirectedGraphCase(TestCase):

    @setup
    def init_the_variable(self):
        self.dag = DirectedGraph()
        self.va = Vertex("A")
        self.vb = Vertex("B")
        self.edge = Edge(self.va, self.vb)
        self.edge.weight = 100

    def test_init(self):
        assert(not self.dag.edges)
        assert(not self.dag.vertices)

    def test_add_edge(self):
        self.dag.add_edge(self.edge)

        assert_equals(self.dag.edges, {self.va: self.edge})
        assert_equals(self.dag.vertices, set([self.va, self.vb]))

    def test_total_weight(self):
        self.dag.add_edge(self.edge)

        assert_equals(self.dag.calculate_least_cost(), 100)

    def test_more_total_weight(self):
        vc = Vertex("C")
        e2 = Edge(self.vb, vc)
        e2.weight = 123

        self.dag.add_edge(self.edge)
        self.dag.add_edge(e2)
        assert_equals(self.dag.calculate_least_cost(), 223)

    @class_teardown
    def get_rid_of_the_variable(self):
        self.vertex = None

if __name__ == "__main__":
    run()
