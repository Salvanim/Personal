import itertools

def generate_combinations(list_1, label_1, list_2, label_2, pattern):
    """
    Generates combinations based on the pattern, yielding results instead of storing them.
    """
    # Mapping labels to their corresponding lists
    list_map = {label_1: list_1, label_2: list_2}

    # Create generator for each pattern combination
    for combo in itertools.product(*[list_map[label] for label in pattern]):
        yield ''.join(combo)

def generate_syllable_combinations(length, current_combination=""):
    """
    Generates patterns using 'C' and 'V' labels recursively as a generator.
    """
    if len(current_combination) == length:
        yield current_combination
    else:
        yield from generate_syllable_combinations(length, current_combination + "V")
        yield from generate_syllable_combinations(length, current_combination + "C")

# Use reduced lists of consonants and vowels for memory efficiency
consonants = [
    "m̥", "m", "ɱ̊", "ɱ", "n̼", "n̥", "n", "ɳ̊", "ɳ", "ɲ̊", "ɲ", "ŋ̊", "ŋ", "ɴ̥", "ɴ",
    "p", "b", "p̪", "b̪", "t̼", "d̼", "t̪", "d̪", "t", "d", "ʈ", "ɖ", "c", "ɟ", "k", "ɡ", "q", "ɢ", "ʡ", "ʔ",
    "t̪s̪", "d̪z̪", "ts", "dz", "t̠ʃ", "d̠ʒ", "tʂ", "dʐ", "tɕ", "dʑ",
    "pɸ", "bβ", "p̪f", "b̪v", "t̪θ", "d̪ð", "tɹ̝̊", "dɹ̝", "t̠ɹ̠̊˔", "d̠ɹ̠˔", "cç", "ɟʝ", "kx", "ɡɣ", "qχ", "ɢʁ", "ʡʜ", "ʡʢ", "ʔh",
    "s", "z", "ʃ", "ʒ", "ʂ", "ʐ", "ɕ", "ʑ",
    "ɸ", "β", "f", "v", "θ̼", "ð̼", "θ", "ð", "θ̠", "ð̠", "ɹ̠̊˔", "ɹ̠˔", "ɻ̊˔", "ɻ˔", "ç", "ʝ", "x", "ɣ", "χ", "ʁ", "ħ", "ʕ", "h", "ɦ",
    "β̞", "ʋ", "ð̞", "ɹ", "ɹ̠", "ɻ", "j", "ɰ", "ʁ̞", "ʔ̞",
    "ⱱ̟", "ⱱ", "ɾ̼", "ɾ̥", "ɾ", "ɽ̊", "ɽ", "ɢ̆", "ʡ̆",
    "ʙ̥", "ʙ", "r̥", "r", "r̠", "ɽ̊r̥", "ɽr", "ʀ̥", "ʀ", "ʜ", "ʢ",
    "tɬ", "dɮ", "tꞎ", "d𝼅", "c𝼆", "ɟʎ̝", "k𝼄", "ɡʟ̝",
    "ɬ", "ɮ", "ꞎ", "𝼅", "𝼆", "ʎ̝", "𝼄", "ʟ̝",
    "l̪", "l", "l̠", "ɭ", "ʎ", "ʟ", "ʟ̠",
    "ɺ̥", "ɺ", "𝼈̥", "𝼈", "ʎ̆", "ʟ̆"
]
vowels = [
    # Close (High) Vowels
    "i", "y", "ɨ", "ʉ", "ɯ", "u",

    # Near-close Vowels
    "ɪ", "ʏ", "ʊ",

    # Close-mid Vowels
    "e", "ø", "ɘ", "ɵ", "ɤ", "o",

    # Mid Vowels
    "ə",

    # Open-mid Vowels
    "ɛ", "œ", "ɜ", "ɞ", "ʌ", "ɔ",

    # Near-open Vowels
    "æ", "ɐ",

    # Open (Low) Vowels
    "a", "ɶ", "ɑ", "ɒ"
]
string = ""
compleateCombinationList = []
# Generate and print combinations for each pattern up to length 2 or 3
for length in range(1, 4):  # Adjust length here to keep memory low
    for pattern in generate_syllable_combinations(length):
        for combination in generate_combinations(consonants, 'C', vowels, 'V', pattern):
            string += combination + " "

print(string)
