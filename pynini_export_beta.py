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


import os
import time
import sys
import shutil
from typing import Dict


from nemo_text_processing.inverse_text_normalization.taggers.tokenize_and_classify import ClassifyFst as ITNClassifyFst
from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst as CardinalITNClassifyFst
from nemo_text_processing.inverse_text_normalization.taggers.decimal import DecimalFst as DecimalITNClassifyFst
from nemo_text_processing.inverse_text_normalization.taggers.consec_num import ConsecutiveNumberFst as ConsecNumITNClassifyFst
from nemo_text_processing.inverse_text_normalization.taggers.date import DateFst as DateITNClassifyFst
from nemo_text_processing.inverse_text_normalization.taggers.sequence import SequenceFst as SequenceITNClassifyFst
from nemo_text_processing.inverse_text_normalization.taggers.time import TimeFst as TimeITNClassifyFst
from nemo_text_processing.inverse_text_normalization.taggers.measure import MeasureFst as MeasureITNClassifyFst

from nemo_text_processing.inverse_text_normalization.verbalizers.verbalize_final import VerbalizeFinalFst as ITNVerbalizeFst
from nemo_text_processing.text_normalization.taggers.tokenize_and_classify import ClassifyFst as TNClassifyFst
from nemo_text_processing.text_normalization.verbalizers.verbalize import VerbalizeFst as TNVerbalizeFst

import argparse
import pynini
from pynini.export import export

# This script exports compiled grammars inside nemo_text_processing
# into OpenFst finite state archive files tokenize_and_classify.far_v1.0 and verbalize.far_v1.0
# for production purposes


def _generator_main(file_name: str, graphs: Dict[str, pynini.FstLike]):
    """
    Exports graph as OpenFst finite state archive (FAR) file with given file name and rule name. 

    Args:
        file_name: exported file name
        graph: Pynini WFST graph to be exported
        rule_name: rule name for graph in created FAR file

    """
    exporter = export.Exporter(file_name)
    for rule, graph in graphs.items():
        exporter[rule] = graph.optimize()
    exporter.close()
    print(f'Created {file_name}')


def itn_grammars(**kwargs):
    d = {}
    if not kwargs["is_reduced"]:
        d['classify'] = {
            'ALL': ITNClassifyFst().fst,
            'CARDINAL': CardinalITNClassifyFst().fst,
            'CONSECNUM': ConsecNumITNClassifyFst().fst,
            'DECIMAL': DecimalITNClassifyFst(CardinalITNClassifyFst()).fst,
            'DATE': DateITNClassifyFst(CardinalITNClassifyFst(), ConsecNumITNClassifyFst()).fst,
            'TIME': TimeITNClassifyFst(CardinalITNClassifyFst()).fst,
            'SEQUENCE': SequenceITNClassifyFst().fst,
            'MEASURE': MeasureITNClassifyFst(CardinalITNClassifyFst(), DecimalITNClassifyFst(CardinalITNClassifyFst())).fst
        }
    else:
        d['classify'] = {'ALL': ITNClassifyFst().fst}
    # d['verbalize'] = {'ALL': ITNVerbalizeFst().fst, 'REDUP': pynini.accep("REDUP")}
    d['verbalize'] = {'ALL': ITNVerbalizeFst().fst}
    return d


def tn_grammars(**kwargs):
    d = {}
    d['classify'] = {'TOKENIZE_AND_CLASSIFY': TNClassifyFst(input_case=kwargs["input_case"], deterministic=True).fst}
    d['verbalize'] = {'ALL': TNVerbalizeFst(deterministic=True).fst, 'REDUP': pynini.accep("REDUP")}
    return d


def export_grammars(output_dir, grammars):
    """
    Exports tokenizer_and_classify and verbalize Fsts as OpenFst finite state archive (FAR) files. 

    Args:
        output_dir: directory to export FAR files to. Subdirectories will be created for tagger and verbalizer respectively.
    """

    for category, graphs in grammars.items():
        out_dir = os.path.join(output_dir, category)
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
            time.sleep(1)
        if category == "classify":
            category = "tokenize_and_classify"
        _generator_main(f"{out_dir}/{category}.far", graphs)


def parse_args():
    parser = argparse.ArgumentParser(description="Export normalization grammar")
    parser.add_argument(
        "--output_dir", help="output directory for grammars", required=True, type=str)
    parser.add_argument(
        "--grammars", help="grammars to be exported", choices=["tn_grammars", "itn_grammars"], type=str, required=True
    )
    parser.add_argument(
        "--input_case", help="input capitalization", choices=["lower_cased", "cased"], default="cased", type=str
    )
    parser.add_argument(
        "--force", help="actively delete the output directory if it existed", action="store_true"
    )
    parser.add_argument(
        "--reduced", help="export the total composition rule", action="store_true"
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    output_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), args.output_dir)

    if os.path.isdir(output_dir) and not args.force:
        print("Delete old far folder before export. Else using --force option")
        exit(0)

    if os.path.isdir(output_dir) and args.force:
        print("Deleting old far folder before export ...")
        shutil.rmtree(args.output_dir)

    export_grammars(output_dir=output_dir, grammars=locals()[args.grammars](input_case=args.input_case, is_reduced=args.reduced))
