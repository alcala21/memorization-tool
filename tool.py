from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Card(Base):
    __tablename__ = 'flashcard'
    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    box = Column(Integer)


engine = create_engine('sqlite:///flashcard.db?check_same_thread=False')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


class FlashCards:

    def __init__(self):
        self.top_menu = ['1. Add flashcards',
                     '2. Practice flashcards',
                     '3. Exit']
        self.card_menu = ['1. Add a new flashcard', '2. Exit']
        self.question_menu = ['press "y" to see the answer:',
                            'press "n" to skip:',
                            'press "u" to update:']
        self.update_menu = ['press "d" to delete the flashcard:',
                            'press "e" to edit the flashcard:']
        self.learning_menu = ['press "y" if your answer is correct:',
                            'press "n" if your answer is wrong:']

    def show_menu(self, _menu, blank_line=True):
        if blank_line:
            self.print("\n".join(_menu))
        else:
            print("\n".join(_menu))

    def add(self):
        while True:
            self.show_menu(self.card_menu)
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

        new_card = Card(question=question, answer=answer, box=1)
        session.add(new_card)
        session.commit()

    def delete_card(self, card):
        session.delete(card)
        session.commit()

    def edit_card(self, card):
        self.print(f"current question: {card.question}")
        card.question = input("please write a new question:\n")
        self.print(f"current answer: {card.answer}")
        card.answer = input("please write a new answer:\n")
        session.commit()

    def update_card(self, card):
        while True:
            self.show_menu(self.update_menu)
            val = input()
            if val == 'd':
                self.delete_card(card)
                break
            elif val == 'e':
                self.edit_card(card)
                break
            else:
                self.print(f"{val} is not an option")

    def show_card(self, card):
        self.print(f"Answer: {card.answer}")
        while True:
            self.show_menu(self.learning_menu, blank_line=False)
            val = input()
            if val == 'y':
                if card.box == 3:
                    self.delete_card(card)
                else:
                    card.box += 1
                    session.commit()
                break
            elif val == 'n':
                card.box = 1
                session.commit()
                break
            else:
                self.print(f"{val} is not an option")

    def ask_question(self, card):
        self.print(f"Question: {card.question}")
        while True:
            self.show_menu(self.question_menu, blank_line=False)
            val = input()
            if val == 'y':
                self.show_card(card)
                break
            elif val == 'n':
                break
            elif val == 'u':
                self.update_card(card)
                break
            else:
                self.print(f"{val} is not an option")

    def practice(self):
        questions = session.query(Card).all()
        if len(questions) == 0:
            self.print('There is no flashcard to practice!')
        else:
            for card in questions:
                self.ask_question(card)

    def play(self):
        while True:
            self.show_menu(self.top_menu)
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
