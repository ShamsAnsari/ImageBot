import cv2
import sys
import pickle
import random

class Scrambler:
    def __init__(self, path):
        self.path = path
        self.img = cv2.imread(path)
        self.SCRAMBLE_SIZE = 50

    def swap(self, img, x1, y1, x2, y2, width, height):
        roi_1 = img[y1:y1 + height, x1:x1 + width]
        roi_2 = img[y2:y2 + height, x2:x2 + width].copy()

        img[y2:y2 + height, x2:x2 + width] = roi_1
        img[y1:y1 + height, x1:x1 + width] = roi_2

    def scramble(self):
        width, height, channel = self.img.shape
        num_r = num_c = self.SCRAMBLE_SIZE
        box_width = width // num_c
        box_height = height // num_r
        scrambled_image = self.img.copy()

        boxes = []
        for r in range(num_r):
            for c in range(num_c):
                boxes.append([r, c])
        random.shuffle(boxes)

        key = []
        key.append([num_r, num_c, box_width, box_height])

        while len(boxes) > 1:
            r1, c1 = boxes.pop(0)
            r2, c2 = boxes.pop(0)
            x1 = c1 * box_width
            y1 = r1 * box_height
            x2 = c2 * box_width
            y2 = r2 * box_height
            self.swap(scrambled_image, x1, y1, x2, y2, box_width, box_height)
            key.append([[r1, c1], [r2, c2]])

        return scrambled_image, key

    def unscramble(self, key):
        unscrambled_image = self.img.copy()
        num_r, num_c, box_width, box_height = key.pop(0)
        for i in key:
            r1, c1, r2, c2 = i[0][0], i[0][1], i[1][0], i[1][1]
            x1, y1, x2, y2 = c1 * box_height, r1 * box_width, c2 * box_height, r2 * box_width
            self.swap(unscrambled_image, x1, y1, x2, y2, box_width, box_height)
        return unscrambled_image


def main():
    if sys.argv[1].lower() == "scramble":
        scrambler = Scrambler(sys.argv[2])
        scrambled_image, key = scrambler.scramble()

        filename, type = sys.argv[2].split(".")

        pickle.dump(key, open(filename + "_key.p", "wb"))
        cv2.imwrite(filename + "_scrambled." + type, scrambled_image)

    elif sys.argv[1].lower() == "unscramble":
        scrambler = Scrambler(sys.argv[2])
        key_path = sys.argv[3]
        unscrambled_image = scrambler.unscramble(pickle.load(open(key_path, "rb")))
        cv2.imwrite("unscrambled_img.png", unscrambled_image)

