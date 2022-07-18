'''
Obtenido de
https://github.com/nur-ag/syltippy
GNU General Public License v3.0
'''


# -*- coding: utf-8 -*-

VOWEL_SET = set('AEIOUaeiouÃ€ÃÃ„ÃˆÃ‰Ã‹ÃŒÃÃÃ’Ã“Ã–Ã™ÃšÃœÃ Ã¡Ã¤Ã¨Ã©Ã«Ã¬Ã­Ã¯Ã²Ã³Ã¶Ã¹ÃºÃ¼')

# vowel groups
OPEN_PLAIN = set('aeo')
OPEN_ACCENTED = set('Ã¡Ã Ã©Ã¨Ã³Ã²')
OPEN_FULL = OPEN_PLAIN | OPEN_ACCENTED
CLOSED_PLAIN = set('i')
CLOSED_ACCENTED = set('Ã­Ã¬ÃºÃ¹')

# consonant groups
BEFORE_L_GROUP = set('bvckfgpt')
BEFORE_R_GROUP = set('bvcdkfgpt')
FOREIGN_GROUP = set('slrnc')
CONSONANT_PAIRS = set(['pt', 'ct', 'cn', 'ps', 'mn', 'gn', 'ft', 'pn', 'cz', 'ts', 'ts'])


def is_consonant(character):
    '''Returns if a character is a consonant or not.'''
    return character not in VOWEL_SET


def syllabize(word):
    '''Processes a word, returning syllables and stressed syllable index.'''
    pos = 0
    positions = []
    length = len(word)
    stress_found = False
    stressed = 0

    # go through all syllables and process the words
    while pos < length:
        positions.append(pos)
        pos = onset(word, pos)
        pos, stress = nucleus(word, pos)
        pos = coda(word, pos)

        if stress:
            stress_found = True
            stressed = len(positions) - 1
    positions.append(length)

    # compute the syllables
    syllabes = [word[s:e] for (s, e) in zip(positions, positions[1:])]

    # if stress was not found, compute it
    num_syllables = len(syllabes)
    if not stress_found:
        if num_syllables < 2: # monosyllabic words
            stressed = 0
        else:
            end_letter = word[-1].lower()
            if (not is_consonant(end_letter) or end_letter == 'y') or \
               (end_letter in 'ns' and not is_consonant(word[-2])):
                stressed = num_syllables - 2
            else:
                stressed = num_syllables - 1

    return syllabes


def onset(word, pos):
    '''Finds the end of the onset/attack of the syllable.'''
    last_consonant = 'a'
    length = len(word)

    while pos < length and is_consonant(word[pos]) and word[pos].lower() != 'y':
        last_consonant = word[pos]
        pos += 1

    if length <= pos:
        return pos

    c1 = word[pos].lower()
    if pos < length - 1:
        if c1 == '':
            if last_consonant == 'q':
                pos += 1
            elif last_consonant == 'g':
                c2 = word[pos + 1].lower()
                if c2 in 'eÃ©iÃ­':
                    pos += 1
        elif c1 == 'Ã¼' and last_consonant == 'g':
            pos += 1
    return pos


def nucleus(word, pos):
    '''Finds the end of the nucleus of the syllable.'''
    previous = 0
    length = len(word)
    stress_found = False

    # Doesn't it have nucleus?!
    if pos >= length:
        return (pos, stress_found)

    # Jumps a letter 'y' to the starting of nucleus, it is as consonant
    if word[pos].lower() == 'y':
        pos += 1

    # Open-vowel or close-vowel with written accent
    if pos < length:
        cr = word[pos].lower()
        if cr in OPEN_ACCENTED:
            stress_found = True
            previous = 0
            pos += 1
        elif cr in OPEN_PLAIN:
            previous = 0
            pos += 1
        elif cr in CLOSED_ACCENTED or cr == 'Ã¼':
            stress_found = True
            return (pos + 1, stress_found)
        elif cr in CLOSED_PLAIN:
            previous = 2
            pos += 1

    # If 'h' has been inserted in the nucleus then it doesn't determine diphthong neither hiatus
    aitch = False;
    if pos < length:
        cr = word[pos].lower()
        if cr == 'h':
            pos += 1
            aitch = True

    # Second vowel
    if pos < length:
        cr = word[pos].lower()
        if cr in OPEN_FULL: # open vowel
            if cr in OPEN_ACCENTED:
                stress_found = True
            if previous == 0:
                if aitch:
                    pos -= 1
                return (pos, stress_found)
            else:
                pos += 1
        elif cr in CLOSED_ACCENTED: # Diphthong
            stress_found = True
            if previous != 0:
                pos += 1
            elif aitch:
                pos -= 1
            return (pos, stress_found)
        elif cr in CLOSED_PLAIN or cr == 'Ã¼':
            if pos < length - 1:
                cr = word[pos + 1].lower()
                if not is_consonant(cr):
                    if word[pos - 1].lower() == 'h':
                        pos -= 1
                    return (pos, stress_found)

            if word[pos].lower() != word[pos - 1].lower():
                pos += 1

            # It is a descendent diphthong
            return (pos, stress_found)

    # Third vowel?
    if pos < length:
        if word[pos].lower() in CLOSED_PLAIN:
            return (pos + 1, stress_found)

    return (pos, stress_found)


def coda(word, pos):
    '''Finds the end of the coda of the syllable, and of the syllable itself.'''
    length = len(word)
    if pos >= length or not is_consonant(word[pos]):
        return pos
    elif pos == length - 1:
        return pos + 1

    c1 = word[pos].lower()
    c2 = word[pos + 1].lower()
    if not is_consonant(c2):
        return pos

    if pos < length - 2:
        c3 = word[pos + 2].lower()

        if not is_consonant(c3):
            # ll, ch, rr before vowel
            if c1 == 'l' and c2 == 'l':
                return pos
            if c1 == 'c' and c2 == 'h':
                return pos
            if c1 == 'r' and c2 == 'r':
                return pos

            # A consonant + 'h' begins a syllable, except for groups sh and rh
            if c1 != 's' and c1 != 'r' and c2 == 'h':
                return pos

            # If the letter 'y' is preceded by the some
            #      letter 's', 'l', 'r', 'n' or 'c' then
            #      a new syllable begins in the previous consonant
            # else it begins in the letter 'y'
            if c2 == 'y' :
                if c1 in FOREIGN_GROUP:
                    return pos
                return pos + 1

            # groups: gl - kl - bl - vl - pl - fl - tl
            if c1 in BEFORE_L_GROUP and c2 == 'l':
                return pos

            # groups: gr - kr - dr - tr - br - vr - pr - fr
            if c1 in BEFORE_R_GROUP and c2 == 'r':
                return pos

            return pos + 1
        else:
            # Three consonants to the end, foreign words?
            if pos + 3 == length:
                if c2 == 'y':
                    if c1 in FOREIGN_GROUP:
                        return pos

                    # 'y' at the end as vowel with c2 or 3 consonants at the end
                    if c3 == 'y':
                        return pos + 1
                    else:
                        return pos + 3

            # y as vowel
            if c2 == 'y':
                if c1 in FOREIGN_GROUP:
                    return pos
                return pos + 1

            # The groups pt, ct, cn, ps, mn, gn, ft, pn, cz, tz and ts begin a syllable
            # when preceded by other consonant
            if word[pos + 1: pos + 3] in CONSONANT_PAIRS:
                return pos + 1

            # The consonantal groups formed by a consonant
            # following the letter 'l' or 'r' can't be
            # separated and they always begin syllable
            # 'ch' or 'y' as vowel
            if (c3 == 'l' or c3 == 'r') or \
               (c2 == 'c' and c3 == 'h') or \
               (c3 == 'y'):
                return pos + 1
            else:
                return pos + 2
    else:
        if c2 == 'y':
            return pos

        # The word ends with two consonants
        return pos + 2
