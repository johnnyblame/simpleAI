import nltk
from difflib import get_close_matches

test = "На столі було. Скільки всього фруктів залишилось на столі?"
fruits = ['апельсин', 'яблуко', 'груша', 'мандарин', 'банан']
actions_plus = ["є", "було", "поклав"]
action = ["залишилось"]
actions_minus = ["з'їв", "забрав"]


class SimpleAI:
    def __init__(self):
        self.num_of_fruits_start = 0
        self.num_of_fruits = 0
        self.stop_word = 'Скільки'
        self.conditions = {}
        self.question = []
        self.start_state = {}
        self.response = ''
        self.error_case = 0

    def sentence_analyzer(self, text):
        sentences = nltk.sent_tokenize(text)
        self.starting_handler(sentences[0])
        for sentence in sentences[1:]:
            if sentence.startswith(self.stop_word):
                self.question_handler(sentence)
            else:
                w = nltk.word_tokenize(sentence)
                self.action_analyzer(w)
        if len(self.question) == 0:
            self.error_case = 1
            self.error_handler()
        elif len(self.conditions) == 0:
            self.error_case = 2
            self.error_handler()
        return self.response

    def question_handler(self, sentence):
        words = nltk.word_tokenize(sentence)
        for i in words:
            if len(get_close_matches(i, fruits)) > 0:
                self.question.append(i)
            if i in action or i in actions_plus or i in actions_minus:
                self.question.append(i)
            if i == 'фруктів':
                self.question.append(i)
        self.final_constructor(self.question)

    def starting_handler(self, sentence):
        description = nltk.word_tokenize(sentence)
        for word in description:
            f_m = get_close_matches(word, fruits)
            if len(f_m) > 0:
                num_or_not = description[description.index(word) - 1]
                try:
                    self.conditions[f_m[0]] = int(num_or_not)
                    self.start_state[f_m[0]] = int(num_or_not)
                    self.num_of_fruits_start += int(num_or_not)
                except ValueError:
                    pass

    def action_analyzer(self, sentence):
        w_m = []
        for word in sentence:
            f_m = get_close_matches(word, fruits)
            a_m = get_close_matches(word, actions_minus)
            if len(a_m) > 0:
                w_m.append(a_m)
            a_p = get_close_matches(word, actions_plus)
            if len(a_p) > 0:
                w_m.append(a_p)
            if len(f_m) > 0:
                num_or_not = sentence[sentence.index(word) - 1]
                try:
                    if w_m[-1][0] in actions_minus:
                        self.conditions[f_m[0]] -= int(num_or_not)
                    elif w_m[-1][0] in actions_plus:
                        self.conditions[f_m[0]] += int(num_or_not)
                except ValueError:
                    pass
        self.num_of_fruits = self.num_of_fruits_start - sum(self.conditions.values())
        return w_m

    def error_handler(self):
        if self.error_case == 1:
            self.response = 'У задачі повинні бути питання, які починаються зі слова "Скільки".'
        elif self.error_case == 2:
            self.response = 'У задачі відсутня умова з фруктами. Повинна бути присутня умова про хлопчика,' \
                            ' який виконує дії з фруктами.'
        print(self.response)

    def final_constructor(self, question_list):
        final = ''
        if len(get_close_matches(self.question[0], fruits)) > 0 or self.question[0] == 'фруктів':
            self.question.reverse()
        for word in question_list:
            if action[0] in self.question:
                if len(get_close_matches(word, fruits)) > 0:
                    final = 'На столі залишилось {} {}.'.format(self.conditions[get_close_matches(word, fruits)[0]],
                                                                word)
                elif word == 'фруктів':
                    final = 'На столі залишилось {} {}.'.format(self.num_of_fruits_start - self.num_of_fruits, word)
            elif self.question[0] in actions_minus:
                if len(get_close_matches(word, fruits)) > 0:
                    final = 'Хлопчик {} {} {}.'.format(self.question[0],
                                                       self.start_state[get_close_matches(word, fruits)[0]]
                                                       - self.conditions[get_close_matches(word, fruits)[0]], word)
                elif word == 'фруктів':
                    final = 'Хлопчик {} {} {}'.format(self.question[0], self.num_of_fruits, word)
            elif self.question[0] in actions_plus:
                if len(get_close_matches(word, fruits)) > 0:
                    final = 'Хлопчик {} {} {}.'.format(self.question[0],
                                                       self.start_state[get_close_matches(word, fruits)[0]]
                                                       + self.conditions[get_close_matches(word, fruits)[0]], word)
                elif word == 'фруктів':
                    final = 'Хлопчик {} {} {}.'.format(self.question[0], self.num_of_fruits_start + self.num_of_fruits,
                                                       word)

        self.response = final
        if len(self.conditions) != 0:
            print(self.response)
        return final


s = SimpleAI()
s.sentence_analyzer(test)
