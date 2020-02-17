from os import system, name
import random

board = ['''
   ____
  |    |
  |
  |
  |
  |
 _|_
|   |______
|__________|''', '''
   ____
  |    |
  |    O
  |
  |
  |
 _|_
|   |______
|__________|''', '''
   ____
  |    |
  |    O
  |    |
  |
  |
 _|_
|   |______
|__________|''', '''
   ____
  |    |
  |    O
  |   /|
  |
  |
 _|_
|   |______
|__________|''', '''
   ____
  |    |
  |    O
  |   /|\\
  |
  |
 _|_
|   |______
|__________|''', '''
   ____
  |    |
  |    O
  |   /|\\
  |    |
  |
 _|_
|   |______
|__________|''', '''
   ____
  |    |
  |    O
  |   /|\\
  |    |
  |   /
 _|_
|   |______
|__________|''', '''
   ____
  |    |
  |    O
  |   /|\\
  |    |
  |   / \\
 _|_
|   |______
|__________|''']


def randomWord():
    with open("words.txt", "rt") as words_file:
        words_list = words_file.readlines()

    return words_list[random.randint(0, len(words_list))].strip()


def show_title():
    print("-" * 27)
    print((" " * 5) + "The Hangman Game!")
    print("-" * 27, end="")


def clear_console():
    if name == "nt":
        _ = system("cls")

    elif name == "posix":
        _ = system("clear")


class Hangman:

    def __init__(self, word):
        self.word = word
        self.word_arr = []
        self.wrong_letters = []
        self.status = 1

        for i in range(len(self.word)):
            self.word_arr.append([self.word[i], False])

    def show_board(self):
        print(board[len(self.wrong_letters)])

    def show_word(self):
        print("\nThe word is:", end=" ")

        for i in range(len(self.word_arr)):
            if self.word_arr[i][1]:
                print(self.word_arr[i][0], end=" ")
            else:
                print("_", end=" ")

    def update_display(self, correct_letter):
        for i in range(len(self.word_arr)):
            if self.word_arr[i][0] == correct_letter:
                self.word_arr[i][1] = True

    def check_status(self):
        if False not in [self.word_arr[i][1] for i in range(len(self.word_arr))]:
            self.status = 2
        elif len(self.wrong_letters) == (len(board) - 1):
            self.status = 3

        return self.status

    def guess_letter(self, attempted_letter):
        if attempted_letter in self.word:
            self.update_display(attempted_letter)
        else:
            self.wrong_letters.append(attempted_letter)

        self.check_status()

    def show_attempted_letters(self):
        print(f"\n\nWrong letters: {' - '.join(self.wrong_letters)}")


if __name__ == "__main__":
    clear_console()
    game = Hangman(randomWord())

    while game.check_status() == 1:
        show_title()
        game.show_board()
        game.show_word()
        game.show_attempted_letters()

        print("\n" + ("-" * 27))

        while True:
            letter = str(input('\nTry a letter: ')).upper()

            if len(letter) > 1:
                print("Try just one letter at a time.")
                continue
            elif letter in game.wrong_letters:
                print(f"You have already tried the letter {letter.upper()}.")
                continue
            elif letter in [game.word_arr[i][0] for i in range(len(game.word_arr)) if game.word_arr[i][1] is True]:
                print(f"You have already tried the letter {letter.upper()}.")
            else:
                break

        game.guess_letter(letter)
        clear_console()

    show_title()
    game.show_board()
    game.show_word()
    game.show_attempted_letters()

    print("\n" + ("-" * 27))

    if game.status == 2:
        print("\nYou win!")
    elif game.status == 3:
        print("\nYou loose!")
        print(f"\nThe word was: {' '.join(game.word)}")

    print("\n" + ("-" * 27))
