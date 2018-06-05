import json

# constants
TESTS_FOLDER = "./tests/"
test = {}
test["ID"] = int(input("Test ID: "))
test["letters"] = list(input("Enter letters to test. eg: \"ABCD \""))
test["delay"] = int(input("Enter delay: "))
test["type"] = input("Enter type: [RAND/SEQ]")
test["num_letters"] = int(input("Number of letters: "))

with open(TESTS_FOLDER+ "{0}.json".format(test["ID"]), 'w') as fp:
    json.dump(test, fp)
