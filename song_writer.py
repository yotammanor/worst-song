# -*- coding: utf-8 -*-

# from numpy import random as numpy_random
import random
import logging
import re

DEFAULT_NUM_OF_WORDS_IN_SONG = 50
MIN_LENGTH_OF_SENTENCE = 2
MAX_LEN_OF_ROW = 30
DEFAULT_NUM_OF_VERSES = 3
MAX_LEN_OF_TITLE_ROW = 4

STRUCTURE_OF_LAST_ROW = {1: [1], 2: [1, 1], 3: [1, 1, 1], 4: [2, 1, 1],
                         5: [3, 1, 1], 6: [3, 1, 1, 1], 7: [3, 2, 1, 1],
                         8: [4, 2, 1, 1], 9: [4, 3, 1, 1], 10: [5, 3, 1, 1]}


class SongWriter(object):
    def __init__(self, material):
        self.material = material
        self.song = ''

    def write(self):
        self.randomize_song_from_sentences()
        self.split_song_to_lines()
        return self.song

    def get_song_title(self):
        first_row = self.song.splitlines()[0]
        first_row = first_row.strip().\
            replace(u'.', u'').\
            replace(u'،', u'').\
            replace(',', '').\
            replace(':', '')
        return ' '.join(first_row.split(' ')[:MAX_LEN_OF_TITLE_ROW])

    def split_song_to_lines(self):
        self.splitlines_on_symbol(u',', threshold_percent=80)
        self.splitlines_on_symbol(u'،', threshold_percent=80)
        self.splitlines_on_symbol(u'.', threshold_percent=95)
        self.splitlines_on_symbol(u'?', threshold_percent=100)
        self.splitlines_on_symbol(u'!', threshold_percent=100)
        self.split_on_max_length()
        self.split_to_verses()
        self.split_last_sentence()

    def split_to_verses(self):
        split_song = ''
        song_parts = [x.strip() for x in self.song.split('\n') if
                      x.strip() and len(x.strip()) > MIN_LENGTH_OF_SENTENCE]
        rows_in_each_verse = len(
            song_parts) / DEFAULT_NUM_OF_VERSES
        verse = ''
        extra_lines = len(song_parts) % DEFAULT_NUM_OF_VERSES
        for i in xrange(0, DEFAULT_NUM_OF_VERSES):
            if not i:
                verse = '\n'.join(
                    song_parts[:extra_lines]) + '\n'
            verse += '\n'. \
                join(song_parts[
                     (rows_in_each_verse * i) + extra_lines:
                     (rows_in_each_verse * (i + 1)) + extra_lines]
                     )

            split_song += verse + '\n\n'
            verse = ''
        self.song = split_song.strip()

    def split_last_sentence(self):
        song_parts = [x.strip() for x in self.song.split('\n') if
                      x.strip() and len(x.strip()) > MIN_LENGTH_OF_SENTENCE]
        last_sentence = song_parts[-1]
        split_song = self.song.replace(last_sentence, '')
        words = [x for x in last_sentence.split(' ')]
        len_of_first_part = (len(words) / 10) * 10
        first_part = words[:len_of_first_part]
        for j in xrange(0, len_of_first_part, 5):
            new_row = ' '.join(first_part[j:j + 5])
            split_song += new_row + '\n'
        second_part = words[len_of_first_part:]
        structure = STRUCTURE_OF_LAST_ROW[len(words) % 10]
        start_point = 0
        for row_length in structure:
            new_row = ''
            for j in xrange(start_point, start_point + row_length, 1):
                new_row = ' '.join([new_row, second_part[j]])
            start_point += row_length
            split_song += new_row + '\n'

        self.song = split_song.strip()

    def split_on_max_length(self):
        song_parts = [x.strip() for x in self.song.split('\n') if
                      x.strip() and len(x.strip()) > MIN_LENGTH_OF_SENTENCE]
        split_song = ''
        for i, part in enumerate(song_parts):
            if len(part) <= MAX_LEN_OF_ROW:
                split_song += part + '\n'
            else:
                split_point = (len(part) / 2) + random.randint(-5, 5)
                words = [x for x in part.split(' ')]
                part_length = 0
                for word in words:
                    split_song += word + ' '
                    part_length += len(word)
                    if part_length >= split_point:
                        split_song += '\n'
                        part_length = 0
                split_song += '\n'

        self.song = split_song.strip()

    def splitlines_on_symbol(self, symbol, threshold_percent=100):
        song_parts = [x.strip() for x in self.song.split(symbol) if
                      x.strip() and len(x.strip()) > MIN_LENGTH_OF_SENTENCE]
        split_song = u''
        for i, part in enumerate(song_parts):
            if random.randint(1, 100) <= threshold_percent:
                split_song += u'{}\n'.format(symbol) + part
            else:
                split_song += u'{} '.format(symbol) + part
            if i == 0:
                split_song = split_song[1:]
        if self.song[-1] == symbol:
            split_song += symbol
        self.song = split_song.strip()

    def randomize_flat_song(self, len_of_song=DEFAULT_NUM_OF_WORDS_IN_SONG):
        bag_of_words = self._material_as_bag_of_words()
        for i in xrange(0, len_of_song):
            self.song += u' ' + random.choice(bag_of_words)

    def randomize_song_from_sentences(self,
                                      len_of_song=DEFAULT_NUM_OF_WORDS_IN_SONG):
        bag_of_sentences = self._material_as_bag_of_sentences()
        while len([x for x in self.song.split(' ') if
                   x.strip() and x.strip().isalpha()]) <= len_of_song:
            self.song += random.choice(bag_of_sentences)

    def _material_as_bag_of_words(self):
        words = []
        for status_content in self.material:
            if status_content:
                for word in status_content.split(' '):
                    words.append(word)

        return words

    def _material_as_bag_of_sentences(self):
        sentences = []
        for status in self.material:
            if status:
                sentences += [x for x in split_into_sentences(status) if
                              len(x) > MIN_LENGTH_OF_SENTENCE]
        return sentences


caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"


def split_into_sentences(text):
    text = u" " + text + u"  "
    text = text.replace(u"\n", u" ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]",
                  "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(caps + "[.]" + caps + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + caps + "[.]", " \\1<prd>", text)
    if u"”" in text: text = text.replace(u".”", u"”.")
    if "\"" in text: text = text.replace(".\"", "\".")
    if "!" in text: text = text.replace("!\"", "\"!")
    if "?" in text: text = text.replace("?\"", "\"?")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences
