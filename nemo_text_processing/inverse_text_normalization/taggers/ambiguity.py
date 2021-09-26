from nemo_text_processing.inverse_text_normalization.utils import get_abs_path
from nemo_text_processing.text_normalization.graph_utils import (
    GraphFst,
    delete_space_optional, NEMO_LOWER,
)
import pynini
from pynini.lib import pynutil

class AmbiguityFst(GraphFst):
    """
    Finite state transducer for classifying consecutive single character such as abbv etc.
        e.g ô tê pê -> consecutive { sequence: "otp" }
    """
    def __init__(self):
        super().__init__(name="ambiguity", kind="classify")

        ambiguity = pynini.string_file(get_abs_path("data/ambiguity.tsv"))
        graph = pynutil.insert("ambiguity: \"") + ambiguity + pynutil.insert("\"")
        self.fst = graph.optimize()

        # super().__init__(name="word", kind="classify")
        # word = pynutil.insert("name: \"") + pynini.closure(NEMO_NOT_SPACE, 1) + pynutil.insert("\"")
        # self.fst = word.optimize()

