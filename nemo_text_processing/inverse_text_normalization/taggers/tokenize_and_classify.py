# Copyright (c) 2021, NVIDIA CORPORATION.  All rights reserved.
# Copyright 2015 and onwards Google, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from nemo_text_processing.inverse_text_normalization.taggers.ambiguity import AmbiguityFst
from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst
from nemo_text_processing.inverse_text_normalization.taggers.fraction import FractionFst
from nemo_text_processing.inverse_text_normalization.taggers.date import DateFst
from nemo_text_processing.inverse_text_normalization.taggers.decimal import DecimalFst
from nemo_text_processing.inverse_text_normalization.taggers.electronic import ElectronicFst
from nemo_text_processing.inverse_text_normalization.taggers.measure import MeasureFst
from nemo_text_processing.inverse_text_normalization.taggers.money import MoneyFst
from nemo_text_processing.inverse_text_normalization.taggers.ordinal import OrdinalFst
from nemo_text_processing.inverse_text_normalization.taggers.punctuation import PunctuationFst
from nemo_text_processing.inverse_text_normalization.taggers.sequence import SequenceFst
from nemo_text_processing.inverse_text_normalization.taggers.telephone import TelephoneFst
from nemo_text_processing.inverse_text_normalization.taggers.time import TimeFst
from nemo_text_processing.inverse_text_normalization.taggers.whitelist import WhiteListFst
from nemo_text_processing.inverse_text_normalization.taggers.word import WordFst
from nemo_text_processing.text_normalization.graph_utils import GraphFst, delete_extra_space, delete_space_optional
from nemo_text_processing.inverse_text_normalization.taggers.consec_num import ConsecutiveNumberFst


try:
    import pynini
    from pynini.lib import pynutil

    PYNINI_AVAILABLE = True
except (ModuleNotFoundError, ImportError):
    PYNINI_AVAILABLE = False


class ClassifyFst(GraphFst):
    """
    Final class that composes all other classification grammars. This class can process an entire sentence, that is lower cased.
    For deployment, this grammar will be compiled and exported to OpenFst Finate State Archiv (FAR) File. 
    More details to deployment at NeMo/tools/text_processing_deployment.
    """

    def __init__(self):
        super().__init__(name="tokenize_and_classify", kind="classify")

        cardinal = CardinalFst()
        cardinal_graph = cardinal.fst

        ambiguity = AmbiguityFst()
        ambiguity_graph = ambiguity.fst

        # ordinal = OrdinalFst(cardinal)
        # ordinal_graph = ordinal.fst

        decimal = DecimalFst(cardinal, keep_quantity=False)
        decimal_graph = decimal.fst

        fraction_graph = FractionFst(cardinal).fst
        measure_graph = MeasureFst(cardinal=cardinal, decimal=decimal).fst
        word_graph = WordFst().fst
        time_graph = TimeFst(cardinal).fst
        money_graph = MoneyFst(cardinal=cardinal, decimal=decimal).fst
        whitelist_graph = WhiteListFst().fst
        punct_graph = PunctuationFst().fst
        # electronic_graph = ElectronicFst().fst
        # telephone_graph = TelephoneFst().fst
        consec_num = ConsecutiveNumberFst()
        consec_num_graph = consec_num.fst
        sequence = SequenceFst()
        sequence_graph = sequence.fst
        date_graph = DateFst(cardinal=cardinal, consec_num=consec_num).fst

        classify = (
            pynutil.add_weight(whitelist_graph, 1.01)
            | pynutil.add_weight(ambiguity_graph, 1.01)
            | pynutil.add_weight(fraction_graph, 1.1)
            | pynutil.add_weight(time_graph, 1.1)
            | pynutil.add_weight(date_graph, 1.09)
            | pynutil.add_weight(decimal_graph, 1.1)
            | pynutil.add_weight(measure_graph, 1.101)
            | pynutil.add_weight(cardinal_graph, 1.1)
        #     | pynutil.add_weight(ordinal_graph, 1.1)
            | pynutil.add_weight(money_graph, 1.1)
        #     | pynutil.add_weight(telephone_graph, 1.1)
        #     | pynutil.add_weight(electronic_graph, 1.1)
            | pynutil.add_weight(consec_num_graph, 1.11)
            | pynutil.add_weight(sequence_graph, 1.11)
            | pynutil.add_weight(word_graph, 100)
            | pynutil.add_weight(punct_graph, weight=1.1)
        )

        # punct = pynutil.insert("tokens { ") + pynutil.add_weight(punct_graph, weight=1.1) + pynutil.insert(" }")
        token = pynutil.insert("tokens { ") + classify + pynutil.insert(" }")
        # token_plus_punct = (
        #     pynini.closure(punct + pynutil.insert(" ")) + token + pynini.closure(pynutil.insert(" ") + punct)
        # )

        graph = token + pynini.closure(delete_extra_space + token)
        graph = delete_space_optional + graph + delete_space_optional


        self.fst = graph.optimize()
