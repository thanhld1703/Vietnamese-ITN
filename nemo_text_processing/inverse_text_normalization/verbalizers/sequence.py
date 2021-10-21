from nemo_text_processing.inverse_text_normalization.utils import get_abs_path
from nemo_text_processing.text_normalization.graph_utils import (
    NEMO_DIGIT,
    GraphFst,
    delete_space_optional, NEMO_GRAPH, NEMO_SIGMA, NEMO_CHAR, NEMO_LOWER
)
import pynini
from pynini.lib import pynutil

class SequenceFst(GraphFst):
    """
    Finite state transducer for verbalizing consecutive single digit number such as telephone number etc.
        e.g ô tê pê -> consecutive { sequence: "ô tê pê" }
    """
    def __init__(self):
        super().__init__(name="sequence", kind="verbalize")
        graph = pynutil.delete("sequence: \"") + pynini.closure(delete_space_optional + NEMO_CHAR, 1) + pynutil.delete("\"")
        final_graph = self.delete_tokens(graph)
        self.fst = final_graph.optimize()

