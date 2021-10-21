from nemo_text_processing.inverse_text_normalization.utils import get_abs_path
from nemo_text_processing.text_normalization.graph_utils import (
    NEMO_DIGIT,
    GraphFst,
    convert_space,
    delete_space_optional, NEMO_LOWER, NEMO_CHAR, NEMO_SIGMA
)
import pynini
from pynini.lib import pynutil

class AmbiguityFst(GraphFst):
    """
    Finite state transducer for verbalizing consecutive single digit number such as telephone number etc.
        e.g ô tê pê -> consecutive { sequence: "ô tê pê" }
    """

    def __init__(self):
        super().__init__(name="ambiguity", kind="verbalize")
        ambiguity = pynini.string_file(get_abs_path("data/ambiguity.tsv"))
        graph = pynutil.delete("ambiguity: \"") + ambiguity + pynutil.delete("\"")
        self.fst = graph.optimize()

