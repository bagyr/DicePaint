__author__ = 'arubtsov'


class Trie(object):

    def __init__(self):
        self.root = dict()

    def add_word(self, word, content):
        curr_dict = self.root
        for letter in word:
            curr_dict = curr_dict.setdefault(letter, {})
        curr_dict.setdefault('_end_', content)

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

    def get_content(self, key):
        curr_dict = self.root
        for letter in key:
            if letter in curr_dict:
                curr_dict = curr_dict[letter]
            else:
                return False
        return curr_dict['_end_']

    def get_variants(self, text):
        curr_dict = self.root
        out = []
        for letter in text:
            if letter in curr_dict:
                curr_dict = curr_dict[letter]
            else:
                return False

        def traverse(word, root):
            for k in root.keys():
                if k != '_end_':
                    traverse(word + k, root[k])
                else:
                    out.append(text + word)

        traverse('', curr_dict)
        return out