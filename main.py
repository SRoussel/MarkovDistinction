from collections import defaultdict, Counter
import numpy
import os
from PIL import Image
import random

# The width/height of the image to be generated
PIXEL_DIM = 100

# Constant for shaping arrays with rgb values
NUM_COLORS = 3


def jpg_to_array(pathname):
    """Converts a jpg file to a pixel array"""
    with Image.open(pathname) as image:
        return numpy.array(image)[:, :, :NUM_COLORS]


def valid(pixel, shape):
    """Determines whether a pixel is valid for a given array shape"""
    return 0 <= pixel[0] < shape[0] and 0 <= pixel[1] < shape[1]


def get_neighbors(x, y):
    """Finds the eight neighboring pixels of (x, y) by index"""
    return [(x, y + 1),
            (x, y - 1),
            (x + 1, y + 1),
            (x + 1, y),
            (x + 1, y - 1),
            (x - 1, y + 1),
            (x - 1, y),
            (x - 1, y - 1)]


class MarkovChain:
    """
    Represents a Markov chain of pixels and their neighbors

    Attributes
    ----------
    filename : basestring
        the filename of the jpg
    chain : dict
        the dictionary representation of the Markov chain
    image : numpy.array
        the pixel array for the given image
    shape: int tuple
        the dimensions of the array (width, height, rgb)
    """

    def __init__(self, filename):
        self.filename = filename
        self.chain = defaultdict(Counter)
        self.image = jpg_to_array(filename)
        self.shape = numpy.shape(self.image)

    def train(self):
        """Trains the Markov chain"""
        print("Training " + self.filename + "...")
        for x in range(0, self.shape[0]):
            for y in range(0, self.shape[1]):
                for neighbor in get_neighbors(x, y):
                    if valid(neighbor, self.shape):
                        pixel = self.image[x][y]
                        neighbor = self.image[neighbor[0]][neighbor[1]]
                        pixel_tuple = tuple(pixel)
                        neighbor_tuple = tuple(neighbor)
                        self.chain[pixel_tuple][neighbor_tuple] += 1


class ImageGenerator:
    """
    Generates an image
    
    markov : MarkovChain
        the Markov chain with which to generate
        
    pixel_array : numpy.array
        the array of pixels for the image
    
    candidates : list
        the next pixels to be drawn

    drawn_pixels : set
        the pixels which have been drawn
    """

    def __init__(self, markov):
        self.markov = markov
        self.pixel_array = numpy.zeros((PIXEL_DIM, PIXEL_DIM, NUM_COLORS), dtype=numpy.uint8)
        self.candidates = []
        self.drawn_pixels = set()

    def draw_random(self):
        """Draws a random pixel with a random color from our markov chain"""
        initial_x = random.randint(0, PIXEL_DIM - 1)
        initial_y = random.randint(0, PIXEL_DIM - 1)
        self.pixel_array[initial_x][initial_y] = random.choice(list(self.markov.chain.keys()))
        self.candidates.append((initial_x, initial_y))

    def generate(self):
        """Generates an image"""
        self.draw_random()
        total_pixels = PIXEL_DIM * PIXEL_DIM
        print("Generating...")

        while self.candidates and len(self.drawn_pixels) < total_pixels:
            pixel = self.candidates.pop()
            self.drawn_pixels.add(pixel)
            pixel_color = self.pixel_array[pixel[0]][pixel[1]]

            keys = list(self.markov.chain[tuple(pixel_color)].keys())
            counts = numpy.array(list(self.markov.chain[tuple(pixel_color)].values()))
            key_indices = numpy.arange(len(keys))

            # If we somehow don't have any keys, generate a new random pixel
            if len(key_indices) == 0:
                self.draw_random()
                continue

            # Normalize the counts from our Markov chain into percentages
            percents = counts / counts.sum()

            # Add the neighbors to the list of pixels to draw
            neighbors = get_neighbors(pixel[0], pixel[1])
            for neighbor in neighbors:
                if neighbor not in self.drawn_pixels and valid(neighbor, numpy.shape(self.pixel_array)):
                    self.candidates.append(neighbor)
                    # This is the crucial step: choose our colors by the probability distribution in the Markov chain
                    self.pixel_array[neighbor[0]][neighbor[1]] = keys[numpy.random.choice(key_indices, p=percents)]

    def draw(self, out_path):
        """Saves the image"""
        Image.fromarray(self.pixel_array).save(out_path)


def main():
    for filename in os.listdir("assets"):
        if filename.endswith(".jpg"):
            markov = MarkovChain("assets/" + filename)
            markov.train()

            generator = ImageGenerator(markov)
            generator.generate()
            generator.draw("examples/" + filename)


if __name__ == "__main__":
    main()
