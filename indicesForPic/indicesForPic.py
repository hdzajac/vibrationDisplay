from PIL import Image
import numpy as np

def getIndices(frames):
    framesNumber = len(frames[0])
    indices = [-1]*(int(framesNumber/3))
    sequence = np.split(frames, framesNumber/3, 1)
    currentFrame = 0
    for frame in sequence:
        counter = 1

        for row in frame:
            for cell in row:
                if cell[0] == 0 and cell[1] == 0 and cell[2] == 0:
                    indices[currentFrame] = counter
                counter += 1
        currentFrame += 1
    return indices


def main():
    config = open("config", "r")
    for line in config:
        im = Image.open(line.strip('\n') + ".png")  # Can be many different formats.
        pic = np.array(im)
        indices = np.array(getIndices(pic)).transpose()
        np.savetxt(line.strip(), indices, fmt="%d", newline=",")

    config.close()

main()