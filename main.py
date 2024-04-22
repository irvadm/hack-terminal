# https://i.ytimg.com/vi/Sa4RUpXgzT4/maxresdefault.jpg

import random
import sys


TOTAL_ROWS = 16
WORDS = ["SHOT", "HURT", "SELL", "GIVE", "SURE", "GEAR", "SENT", "FIRE", "GLOW", "WEEK", "ONES", "SICK"]
WORD_LENGTH = len(WORDS[0]) # Length of a word in WORDS
TOTAL_WORDS = len(WORDS) # Number of words in WORDS
MIN_WORDS = 5 # WORDS must have at least 5 words, I just picked 5
assert TOTAL_WORDS >= MIN_WORDS, "Not enough words." 

# All words in WORDS must have the same length
for word in WORDS:
    assert len(word) == WORD_LENGTH, "A doesn't match the required word length."

GARBAGE_CHARS = "'.,;`][\\/%}{)(*#@?$=<>-_!^:\""
GARBAGE_STRING_LENGTH = 12
MIN_ADDRESS = 0x9430


def create_rows():
    rows = []
    for _ in range(TOTAL_ROWS):
        rows.append({
            "address1": None,
            "garbage1": "",
            "address2": None,
            "garbage2": ""
        })
    return rows


def draw_rows(rows):
    for row in rows:
        row_content = (
            row["address1"] + " " +
            row["garbage1"] + " " +
            row["address2"] + " " +
            row["garbage2"]
        )
        print(row_content)


def run():
    # Initialize rows
    rows = create_rows()

    # Create memory addresses
    addresses = []
    address = MIN_ADDRESS
    for _ in range(TOTAL_ROWS):
        addresses.append(address)
        address += GARBAGE_STRING_LENGTH

    # Add memory addresses to rows
    for i, row in enumerate(rows):
        row["address1"] = hex(addresses[i])
        row["address2"] = hex(addresses[i] + (TOTAL_ROWS * GARBAGE_STRING_LENGTH))

    # Add garbage string
    num_words = random.randint(MIN_WORDS, TOTAL_WORDS) # Random number of words to insert into garbage strings
    word_indices = [i for i in range(0, TOTAL_WORDS)]
    random.shuffle(word_indices)
    random_words = []
    for i in range(num_words):
        random_words.append(WORDS[i])

    # Pick secret word
    secret_word = random.choice(random_words) 

    # How do we allocate the words to the rows without looping through all the rows
    random_indices = list(range(TOTAL_ROWS * 2))
    random.shuffle(random_indices)
    garbage_indices = random_indices[:num_words]
    for i, row in enumerate(rows):
        garbage1_index = i
        garbage2_index = i + TOTAL_ROWS
        if garbage1_index in garbage_indices:
            word = random_words.pop()
            word_index = random.randint(0, GARBAGE_STRING_LENGTH - WORD_LENGTH)
            before_word = "".join([random.choice(GARBAGE_CHARS) for _ in range(0, word_index)])
            after_word = "".join([random.choice(GARBAGE_CHARS) for _ in range(word_index + WORD_LENGTH, GARBAGE_STRING_LENGTH)])
            row["garbage1"] = before_word + word + after_word
        else:
            row["garbage1"] = "".join([random.choice(GARBAGE_CHARS) for _ in range(GARBAGE_STRING_LENGTH)])
        if garbage2_index in garbage_indices:
            word = random_words.pop()
            word_index = random.randint(0, GARBAGE_STRING_LENGTH - WORD_LENGTH)
            before_word = "".join([random.choice(GARBAGE_CHARS) for _ in range(0, word_index)])
            after_word = "".join([random.choice(GARBAGE_CHARS) for _ in range(word_index + WORD_LENGTH, GARBAGE_STRING_LENGTH)])
            row["garbage2"] = before_word + word + after_word
        else:
            row["garbage2"] = "".join([random.choice(GARBAGE_CHARS) for _ in range(GARBAGE_STRING_LENGTH)])


    draw_rows(rows)
    attempts = 3
    while True:
        while attempts > 0:
            try:
                print(f"Attempt(s): {attempts}")
                guess = input("> ").upper()
                if guess == secret_word:
                    print(">You've hacked the terminal!")
                    return
                else:
                    attempts -= 1
                    likeness = 0
                    for char in guess:
                        if char in secret_word:
                            likeness += 1
                    print(f"> Entry denied. Likeness={likeness}")
            except KeyboardInterrupt:
                sys.exit(0)
        print("Locked out")
        return

if __name__ == "__main__":
    run()



