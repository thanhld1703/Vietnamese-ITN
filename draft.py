import pynini
import pywrapfst
import sys
import time
from pynini.lib.rewrite import rewrites
from nemo_text_processing.inverse_text_normalization.inverse_normalize import InverseNormalizer

print(InverseNormalizer().inverse_normalize("hai chín", verbose=True))
# print(sys.path)