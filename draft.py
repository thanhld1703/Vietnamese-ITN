import unittest
import pynini
import sys
print(sys.path)
from nemo_text_processing.inverse_text_normalization.taggers.cardinal import CardinalFst
class TestCardinalFst(unittest.TestCase):
    graph = CardinalFst().fst
    
    def test_2_digits(self):
        cardinal = CardinalFst()
        word_list = [
            "mười",
            "mười hai",
            "mười lăm",
            "hai mươi",
            "bốn mươi lăm",
            "chín bảy",
            "ba mốt"
        ]
        for word in word_list:
            self.assertEqual(word, self.convert_str(word))
    
    def convert_str(self, s):
        return pynini.project(self.graph @ pynini.accep(s), "output")

if __name__ == "__main__":
    TestCardinalFst().test_2_digits()