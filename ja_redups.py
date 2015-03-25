from itertools import product
import re
import sys

"""
A reduplicant generator for Japanese that allows only sequences
valid in "modern standard" Japanese (ie. no CC, wi, we, etc)
TODO: add reporting count of raw possiblities using C and V candidates for a given pattern
"""

class JapaneseReduplicator(object):
    vowels = "aeiou"
    consonants = "rpbtdkgszhmnyw"
    sounds = vowels + consonants
    # these sequences are unattested in modern standard Japanese
    invalid_sequences = {"wi", "we", "wu"}

    def __init__(self, pattern):
       if "CC" in pattern:
           raise ValueError("cannot have a consonant sequence!")
       self.pattern = pattern.upper()
       self.length = len(self.pattern)
       self.vowel_positions = [i for i in range(self.length) if self.pattern[i] == "V"]
       self.consonant_positions = [i for i in range(self.length) if self.pattern[i] == "C"]

    def make_reduplicants(self, letter, position):
        def valid_pattern(pattern):
           redup_candidate = "".join(pattern)
           if pattern[-1] != "n" and self.pattern[-1] == "C" or any(invalid in redup_candidate for invalid in self.invalid_sequences):
               return False
           for i in range(self.length):
               if (i in self.vowel_positions and pattern[i] not in self.vowels):
                   return False
               elif (i in self.consonant_positions and pattern[i] not in self.consonants):
                   return False
           return True

        redups = sorted(set("".join(candidate) for candidate in product(self.sounds, repeat=self.length) if valid_pattern(candidate)))
        return "\n".join(" ".join(d) for d in zip(redups, redups))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print "USAGE:\n\tpython ja_redups.py <pattern> <letter> <index of letter (starts at zero)>\n\t\texample for 'pattern' => CVCV"
        sys.exit(0)

    reduplicator = JapaneseReduplicator(sys.argv[1])
    print reduplicator.make_reduplicants(sys.argv[2], int(sys.argv[-1]))
