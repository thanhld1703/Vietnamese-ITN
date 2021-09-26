from nemo_text_processing.inverse_text_normalization.utils import get_abs_path
from nemo_text_processing.text_normalization.graph_utils import (
    NEMO_DIGIT,
    GraphFst,
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
        graph = (
                pynutil.delete("ambiguity:")
                + delete_space_optional
                + pynutil.delete("\"")
                + pynini.closure(NEMO_CHAR, 1)
                + pynutil.delete("\"")
        )
        graph = graph @ pynini.cdrewrite(pynini.cross(u"\u00A0", " "), "", "", NEMO_SIGMA)
        self.fst = graph.optimize()

