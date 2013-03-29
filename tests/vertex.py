from testify import *
from deploy.dag.vertex import *


class VertexTestCase(TestCase):

    @class_setup
    def init_the_variable(self):
        self.vertex = Vertex("Test")

    def test_str(self):
        assert_equal(str(self.vertex), "Test")

    @class_teardown
    def get_rid_of_the_variable(self):
        self.vertex = None

if __name__ == "__main__":
    run()
