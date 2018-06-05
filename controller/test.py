import serial # pySerial
import struct # packing bytes to string
import json # loading test jsons
import os   # OS related file reading

# Constants
TEST_DIRECTORY = "./tests/"

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
[1,4,7,11,14,-1,-1,3,6,9,11,14,-1,-1,-1],
'W':
[1,4,7,10,13,-1,-1,13,11,8,-1,-1,8,11,15,-1,-1,15,12,9,6,3,-1,-1,-1],
'X':
[1,4,8,12,15,-1,-1,3,6,8,10,13,-1,-1,-1],
'Y':
[1,4,8,-1,-1,3,6,8,-1,-1,-1,8,11,14,-1,-1,-1],
'Z':
[1,2,3,-1,-1,3,6,8,10,13,-1,-1,13,14,15,-1,-1,-1]
}

PORT = "/dev/ttyACM0" # might be "COM3" on Windows

# Helper functions
def read_number(text):
    while True:
        try:
            number = int(input(text))
            return number
        except ValueError:
            print("Input not a number!")


# Tests
def test0(s):
    print("Starting test0")



################################ START #########################################
# Open comm to Arduino
connected = False
arduino = 0
try:
    arduino = serial.Serial(PORT, 9600)
    connected = True
except serial.serialutil.SerialException as e:
    print("Could not connect to arduino: " + PORT)
    print(e)


# Setup
# Get all available tests
tests = [s.replace('.json', '') for s in os.listdir(TEST_DIRECTORY)]
age = read_number("Enter your age: ")
gender = input("Gender: ")
test_type = read_number("Enter test-type from [{0}]: ".format(','.join(tests)))

# Load test
with open(TEST_DIRECTORY + '{0}.json'.format(test_type, 'r')) as fp:
    test = json.load(fp)

# Execute test
input("Press enter key to start")

# for i in range(0, test['num_letters']):

#
def write_letter(s, letter):
    arr = LETTERS[letter[0].upper()]
    # print("arr:" + str(arr))

    # Write out bytes
    for b in arr:
        s.write(struct.pack('>b', b))

