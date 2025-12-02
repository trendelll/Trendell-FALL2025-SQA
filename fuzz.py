import random
import string
import json
import math

# Functions
def safe_div(a, b):
    return a / b

def reverse_string(s):
    return s[::-1]

def parse_json(txt):
    return json.loads(txt)

def sqrt_value(x):
    return math.sqrt(x)

def list_index(lst, idx):
    return lst[idx]

# Input generators

def rand_num():
    return random.choice([
        random.randint(-1000, 1000),
        random.uniform(-1000, 1000),
        None,
        "not_a_number",
    ])

def rand_string():
    size = random.randint(0, 50)
    return ''.join(random.choice(string.printable) for _ in range(size))

def rand_json():
    if random.random() < 0.5:
        return rand_string()  # malformed JSON
    return json.dumps({"val": rand_num(), "text": rand_string()})

def rand_list():
    size = random.randint(0, 20)
    return [rand_num() for _ in range(size)]

# Fuzzing loop

def fuzz():
    bugs = []

    for i in range(5000):  # run 5k iterations
        # safe_div fuzz
        try:
            safe_div(rand_num(), rand_num())
        except Exception as e:
            bugs.append(("safe_div", str(e)))

        # reverse_string fuzz
        try:
            reverse_string(random.choice([rand_string(), rand_num(), rand_list()]))
        except Exception as e:
            bugs.append(("reverse_string", str(e)))

        # parse_json fuzz
        try:
            parse_json(rand_json())
        except Exception as e:
            bugs.append(("parse_json", str(e)))

        # sqrt_value fuzz
        try:
            sqrt_value(rand_num())
        except Exception as e:
            bugs.append(("sqrt_value", str(e)))

        # list_index fuzz
        try:
            lst = rand_list()
            idx = random.randint(-10, 30)
            list_index(lst, idx)
        except Exception as e:
            bugs.append(("list_index", str(e)))

    # record results
    with open("fuzz_report.txt", "w") as f:
        for fn, err in bugs:
            f.write(f"{fn} error: {err}\n")

if __name__ == "__main__":
    fuzz()
