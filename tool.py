class FlashCards:

    def __init__(self):
        self.menu = ['1. Add flashcards',
                     '2. Practice flashcards',
                     '3. Exit']
        self.card_menu = ['1. Add a new flashcard', '2. Exit']
        self.flashcards = dict()

    def top_menu(self):
        self.print("\n".join(self.menu))

    def flash_menu(self):
        self.print("\n".join(self.card_menu))

    def add(self):
        while True:
            self.flash_menu()
            val = input()
            try:
                num = int(val)
                if num == 1:
                    self.add_card()
                elif num == 2:
                    break
                else:
                    raise ValueError
            except ValueError:
                self.print(f"{val} is not an option")

    def add_card(self):
        question, answer = "", ""
        print()
        while not question:
            question = input("Question:\n").strip()
        while not answer:
            answer = input("Answer:\n").strip()
        self.flashcards[question] = answer

    def print_answer(self, question):
        self.print(f"Answer: {self.flashcards[question]}")

    def ask_question(self, question):
        self.print(f"Question: {question}")
        option = input('Please press "y" to see the answer or press "n" to skip:\n')
        if option == 'y':
            self.print_answer(question)

    def practice(self):
        if not self.flashcards:
            self.print('There is no flashcard to practice!')
        else:
            for question in self.flashcards:
                self.ask_question(question)

    def play(self):
        while True:
            self.top_menu()
            val = input()
            try:
                num = int(val)
                if num == 1:
                    self.add()
                elif num == 2:
                    self.practice()
                elif num == 3:
                    self.print("Bye!")
                    break
                else:
                    raise ValueError
            except ValueError:
                self.print(f"{val} is not an option")

    def print(self, message):
        print()
        print(message)


if __name__ == '__main__':
    app = FlashCards()
    app.play()
