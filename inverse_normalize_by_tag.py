from pynini.lib.rewrite import rewrites, top_rewrite
from pynini.lib import pynutil
import pynini
import os
import argparse


def parse_args():
    parser = argparse.ArgumentParser(description="Inverse normalize text")
    parser.add_argument("input", type=str, help="input text")
    parser.add_argument("tag", type=str, help="normalize type of input text")
    return parser.parse_args()


def inverse_normalize(s: str, verbose=False) -> str:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    reader_classifier = pynini.Far(os.path.join(dir_path, "far_alt/classify/tokenize_and_classify.far"))
    reader_verbalizer = pynini.Far(os.path.join(dir_path, "far_alt/verbalize/verbalize.far"))
    classifier = reader_classifier.get_fst()
    verbalizer = reader_verbalizer.get_fst()
    token = top_rewrite(s, classifier)
    if verbose:
        print(token)
    return top_rewrite(token, verbalizer)


def inverse_normalize_by_tag(s: str, tag: str, verbose=False) -> str:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    reader_classifier = pynini.Far(os.path.join(dir_path, f"far_alt/{tag}_tagger/{tag}_tagger.far"))
    reader_verbalizer = pynini.Far(os.path.join(dir_path, "far_alt/verbalize/verbalize.far"))
    classifier = reader_classifier.get_fst()
    verbalizer = reader_verbalizer.get_fst()
    token = top_rewrite(s, classifier)
    if verbose:
        print(token)
    token = pynutil.insert("tokens { ") + token + pynutil.insert(" }")
    return top_rewrite(token, verbalizer)


if __name__ == "__main__":
    arg = parse_args()
    if arg.tag == 'all':
        print(inverse_normalize(arg.input, True))
    else:
        print(inverse_normalize_by_tag(arg.input, arg.tag, True))
