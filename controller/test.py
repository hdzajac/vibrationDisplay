import serial # pySerial
import struct # packing bytes to string
import json # loading test jsons
import os   # OS related file reading
import datetime # For the filename
from time import sleep # To not take input while waiting for the vibration to finish
from random import randint # For random test sequences
from random import seed

# Constants
TEST_DIRECTORY = "./tests/"
RESULT_DIRECTORY = "./results/"
PORT = "COM5" # might be "COM3" on Windows

LETTERS = {
'A':
[1,4,7,10,13,-1,-1,1,2,6,9,12,15,-1,-1,7,8,9,-1,-1,-1],
'B':
[1,4,7,10,13,-1,-1,1,2,6,8,7,-1,-1,7,8,12,14,13,-1,-1,-1],
'C':
[6,2,4,7,10,14,12,-1,-1,-1],
'D':
[1,4,7,10,13,-1,-1,1,2,6,9,12,14,13,-1,-1,-1],
'E':
[1,4,7,10,13,-1,-1,1,2,3,-1,-1,7,8,9,-1,-1,13,14,15,-1,-1,-1],
'F':
[1,4,7,10,13,-1,-1,1,2,3,-1,-1,7,8,9,-1,-1,-1],
'G':
[6,2,4,7,10,14,12,-1,-1,8,9,12,15,-1,-1,-1],
'H':
[1,4,7,10,13,-1,-1,3,6,9,12,15,-1,-1,7,8,9,-1,-1,-1],
'I':
[2,5,8,11,14,-1,-1,-1],
'J':
[1,2,3,6,9,12,14,10,-1,-1,-1],
'K':
[1,4,7,10,13,-1,-1,3,6,8,7,-1,-1,7,8,12,15,-1,-1,-1],
'L':
[1,4,7,10,13,-1,-1,13,14,15,-1,-1,-1],
'M':
[1,4,7,10,13,-1,-1,1,5,8,-1,-1,3,5,8,-1,-1,3,6,9,12,15,-1,-1,-1],
'N':
[1,4,7,10,13,-1,-1,4,8,11,15,-1,-1,3,6,9,12,15,-1,-1,-1],
'O':
[2,4,7,10,14,12,9,6,2,4,-1,-1,-1],
'P':
[1,4,7,10,13,-1,-1,1,2,6,8,7,-1,-1,-1],
'Q':
[2,4,7,10,14,12,9,6,2,4,-1,-1,11,15,-1,-1,-1],
'R':
[1,4,7,10,13,-1,-1,1,2,6,8,7,-1,-1,7,11,15,-1,-1,-1],
'S':
[6,2,4,8,12,14,10,-1,-1,-1],
'T':
[1,2,3,-1,-1,2,5,8,11,14,-1,-1,-1],
'U':
[1,4,7,10,13,14,15,12,9,6,3,-1,-1,-1],
'V':
[1,4,7,11,14,-1,-1,14,11,9,6,3,-1,-1,-1],
'W':
[1,4,7,10,13,-1,-1,13,11,8,-1,-1,8,11,15,-1,-1,15,12,9,6,3,-1,-1,-1],
'X':
[1,4,8,12,15,-1,-1,3,6,8,10,13,-1,-1,-1],
'Y':
[1,4,8,-1,-1,3,6,8,-1,-1,-1,8,11,14,-1,-1,-1],
'Z':
[1,2,3,-1,-1,3,6,8,10,13,-1,-1,13,14,15,-1,-1,-1]
}

# Helper functions
def read_number(text):
    while True:
        try:
            number = int(input(text))
            return number
        except ValueError:
            print("Input not a number!")

def hasLetter(test):
    # Returns whether test has letters left
    # For SEQ tests, we only check if array wasn't exhausted
    # For RAND tests, we check if we need to take more letters for the test
    if test["type"] == "SEQ":
        return len(test["letters"]) > 0
    else:
        return test["num_letters"] > 0

def getLetter(test):
    # Returns a letter from the test
    # For SEQ tests, takes first element and removes it from the list
    # For RAND tests, takes a random element from the list (can repeat)
    if test["type"] == "RAND":
        ret = test["letters"][randint(0, len(test["letters"]) - 1)]
        test["num_letters"] -= 1
        return ret
    else:
        ret = test["letters"][0]
        test["letters"] = test["letters"][1:]
        return ret

def write_letter(s, delay, letter):
    arr = LETTERS[letter.upper()]
    # print("arr:" + str(arr))
    # Write delay
    if connected:
        s.write(struct.pack('>b', delay))
        # Write out bytes
        for b in arr:
            s.write(struct.pack('>b', b))

        sleep(len(arr) * delay * 2 / 1000)
    else:
        print("--Arduino not connected, writing normal string to file")
        arduino.write(str(delay))
        arduino.write(str(arr))
        arduino.write('\n')
        # I know I can use format, but I've already written this :)
        # Feel free to change it
        # Could've written it while writing this fancy comment
        # Sue me
        # <3
        print("--No sleep. GUARANA BITCH")


################################ START #########################################
# Open comm to Arduino
connected = False
arduino = open("arduino.txt", "w")
try:
    arduino = serial.Serial(PORT, 9600)
    connected = True
except serial.serialutil.SerialException as e:
    print("Could not connect to arduino: " + PORT)
    print(e)
    print("Using arduino.txt as file output instead of serial")


# Setup
# Get all available tests
tests = [s.replace('.json', '') for s in os.listdir(TEST_DIRECTORY)]
# Idea is that we can enter the test number, and let the user
# enter the information about themselves, so this makes a lot more sense
# if it is entered first
test_type = read_number("Enter test-type from [{0}]: ".format(','.join(tests)))
age = read_number("Enter your age: ")
gender = input("Gender: ")

# Normalize gender to 1 letter M or F
# Could pose the issue of "Other" gender
# But fuck that (maybe?)
if 'F' in gender or 'f' in gender:
    gender = 'F'
else:
    gender = 'M'

# Load test
with open(TEST_DIRECTORY + '{0}.json'.format(test_type, 'r')) as fp:
    test = json.load(fp)

# Execute test
test_time = datetime.datetime.now().strftime("%m-%d-%H-%M")
guesses = []

seed(datetime.datetime.now())

while (hasLetter(test)):

    target = getLetter(test)
    vibrations = 0

    entered = '?'

    input("Press enter key to feel the vibration :^)")

    while not entered.isalpha():
        vibrations += 1
        write_letter(arduino, test["delay"], target)
        entered = input("Enter a letter or input '?' to feel the pattern again!")

    # entered a letter
    entered = entered.upper()
    guesses.append((target,entered,vibrations))

    if entered == target:
        print("Correct!")
    else:
        print("Wrong... the correct letter was " + target + "! :(")

# Write test result to file
outfile = open(RESULT_DIRECTORY + '{0}-{1}-{2}-{3}.csv'.format(test_type, age, gender, test_time), "w")
outfile.write("letter,guessed_letter,repetitions_requested\n")
for entry in guesses:
    outfile.write("{0},{1},{2}\n".format(entry[0], entry[1], entry[2]))
outfile.close()
