from nemo_text_processing.inverse_text_normalization.utils import get_abs_path
from nemo_text_processing.text_normalization.graph_utils import (
    GraphFst,
    delete_space_optional, NEMO_SPACE
)
import pynini
from pynini.lib import pynutil

class SequenceFst(GraphFst):
    """
    Finite state transducer for classifying consecutive single character such as abbv etc.
        e.g ô tê pê -> consecutive { sequence: "otp" }
    """
    def __init__(self):
        super().__init__(name="sequence", kind="classify")
        graph_char = pynini.string_file(get_abs_path("data/sequence.tsv"))
        graph = graph_char + pynini.closure(NEMO_SPACE + graph_char, 1)
        self.graph_2_or_more = graph
        graph = pynutil.insert("sequence: \"") + graph + pynutil.insert("\"")
        final_graph = self.add_tokens(graph)
        self.fst = final_graph.optimize()

