from numpy import random as numpy_random
import random
import logging

DEFAULT_NUM_OF_WORDS_IN_SONG = 80


class SongWriter(object):
    def __init__(self, material):
        self.material = material
        self.song = ''

    def randomize_flat_song(self, len_of_song=DEFAULT_NUM_OF_WORDS_IN_SONG):
        bag_of_words = self._material_as_bag_of_word()

        for i in xrange(0, len_of_song):
            self.song += ' ' + random.choice(bag_of_words)

    def _material_as_bag_of_word(self):
        words = []
        for status_content in self.material:
            if status_content:
                for word in status_content.split(' '):
                    words.append(word)

        return words

    def write(self):
        self.randomize_flat_song()
        return self.song
