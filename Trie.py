__author__ = 'arubtsov'


class Trie(object):

    def __init__(self):
        self.root = dict()

    def add_word(self, word):
        curr_dict = self.root
        for letter in word:
            curr_dict = curr_dict.setdefault(letter, {})
        curr_dict.setdefault('_end_', '_end_')

    def get_word(self, text):
        curr_dict = self.root
        predict = ''
        for letter in text:
            if letter in curr_dict:
                curr_dict = curr_dict[letter]
                predict += letter
            else:
                return False
        while '_end_' not in curr_dict:
            if len(curr_dict) == 1:
                letter = curr_dict.keys().pop()
                predict += letter
                curr_dict = curr_dict[letter]
            else:
                return False
        return predict

    def get_variants(self, text):
        curr_dict = self.root
        out = []
        i = 0
        for letter in text:
            if letter in curr_dict:
                curr_dict = curr_dict[letter]
                i += 1
            else:
                return False

        def traverse(word, root):
            if '_end_' in root:
                out.append(word)
                return
            for k in root.keys():
                word += k
                traverse(word, root[k])

        traverse(text[i:], curr_dict)
        return out
