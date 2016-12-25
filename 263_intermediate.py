import collections
import os
import operator
import string


def load_data():
    with open(os.path.join('data', 'cmudict.txt'), encoding='latin-1') as cmudict, \
         open(os.path.join('data', 'phonemes.txt')) as phonemes:
        words_pronunciation = {}
        for line in cmudict:
            if not line.startswith(tuple(string.punctuation)):
                splitted = line.split()
                word = splitted[0].replace("'", "")
                words_pronunciation[word] = splitted[1:]
        vowels = [line.split()[0] for line in phonemes if line[:-1].endswith('vowel')]
    return words_pronunciation, vowels


def find_rhyme_ending(word_syllables, vowels):
    for index, syllable in enumerate(word_syllables[::-1], 1):
        if syllable[:-1] in vowels and index != len(word_syllables) and word_syllables[-index-1][:-1] not in vowels:
            return word_syllables[-index:]
    if word_syllables[0][:-1] in vowels:
        return word_syllables


def find_common_end_syllables(word1_syllables, word2_syllables):
    common_end_syllables = collections.deque()
    for syllable1, syllable2 in zip(reversed(word1_syllables), reversed(word2_syllables)):
        if syllable1 == syllable2:
            common_end_syllables.appendleft(syllable1)
        else:
            break
    return common_end_syllables


def find_rhymes(word, dictionary, vowels):
    word_syllables = dictionary[word.upper()]
    rhyme_ending = find_rhyme_ending(word_syllables, vowels)
    rhyming_words = {}
    for entry in dictionary:
        common_end_syllables = find_common_end_syllables(dictionary[entry], word_syllables)
        if len(common_end_syllables) < len(rhyme_ending):
            pass
        else:
            rhyming_words[entry] = common_end_syllables
    return rhyming_words


def main():
    words_pronunciation, vowels = load_data()
    print('Read {} words and {} vowels.'.format(len(words_pronunciation), len(vowels)))
    word = input('Which word do you want to rhyme?\n>>> ')
    if not word.upper() in words_pronunciation:
        raise ValueError('No such word in dictionary!')
    rhyming_words = find_rhymes(word, words_pronunciation, vowels)
    with open('rhymes.txt', 'w') as rhymes:
        print('Rhymes found for {}({}):'.format(word, ' '.join(words_pronunciation[word.upper()])),
              file=rhymes)
        for rhyme in sorted(rhyming_words, key=lambda k: len(rhyming_words[k]), reverse=True):
            if word.upper() not in rhyme and '(' not in rhyme:
                print('\t[{}]\t{}: {}'.format(len(rhyming_words[rhyme]),
                                              rhyme,
                                              rhyming_words[rhyme]),
                                       file=rhymes)
    print('Done! Check rhymes.txt')


if __name__ == '__main__':
    main()
