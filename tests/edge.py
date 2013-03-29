from testify import *
from deploy.dag.edge import *
from deploy.dag.vertex import *


class EdgeTestCase(TestCase):

    @class_setup
    def init_the_variable(self):
        self.edge = Edge(Vertex("A"), Vertex("B"))

    def test_str(self):
        assert_equal(str(self.edge), "(A,B,0)")

    def test_str_with_weight(self):
        self.edge.weight = 100
        assert_equal(str(self.edge), "(A,B,100)")

    @class_teardown
    def get_rid_of_the_variable(self):
        self.edge = None

if __name__ == "__main__":
    run()
