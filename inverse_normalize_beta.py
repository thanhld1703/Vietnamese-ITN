from pynini.lib.rewrite import rewrites, top_rewrite
from pynini.lib import pynutil
import pynini
import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Usage: Normalize text inversely from spoken form to written form")
    parser.add_argument(
        "--tag", type=str, nargs='?', help="Class of the input text if the input text is already classified",
        choices=['all', 'cardinal', 'consecnum', 'date', 'sequence', 'decimal', 'measure'], default='all'
    )
    parser.add_argument(
        "input", type=str, help="Input text string"
    )

    return parser.parse_args()


def inverse_normalize(s: str, tag='ALL', verbose=False) -> str:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    reader_classifier = pynini.Far(os.path.join(dir_path, "./far_beta/classify/tokenize_and_classify.far"))
    reader_verbalizer = pynini.Far(os.path.join(dir_path, "./far_beta/verbalize/verbalize.far"))

    if not reader_classifier.find(tag):
        reader_classifier.find('ALL')
    token = top_rewrite(s, reader_classifier.get_fst())
    if verbose:
        print(token)
    if not tag == 'ALL':
        token = pynutil.insert("tokens { ") + token + pynutil.insert(" }")
    return top_rewrite(token, reader_verbalizer.get_fst())


if __name__ == "__main__":
    arg = parse_args()
    print(inverse_normalize(arg.input, arg.tag.upper(), True))
