"""
***Number guessing game***
Goal: To create a game with multiple difficulties that asks the user to 
guess a random number within a range. Higher difficulty will increase the 
number of guesses, but will also increase the range."""


from random import randint
import winsound
from msvcrt import getch
# try:
#     import tty
#     import termios
# except ImportError:
#     try:
#         import msvcrt
#     except ImportError:
#         raise ImportError("No module available")
#     else:
#         getch = msvcrt.getch


def simple_text_reader(text_file):
    """Simply returns data from a .txt file."""
    with open(text_file, 'rt') as file:
        data = file.read()
        return data


win_text = simple_text_reader('txtfiles/win_text.txt')
loss_text = simple_text_reader('txtfiles/loss_text.txt')
input_line = simple_text_reader('txtfiles/input_line.txt')


def score_reader():
    """Places scores into a list from format 'difficulty:0:0'"""
    array = list()
    with open('txtfiles/scores.txt', 'r') as file:
        data = file.readlines()
        for index, line in enumerate(data):
            line = line.strip().split(':')
            array.append(line)
            line[1] = int(line[1])
            line[2] = int(line[2])
        return array


def score_display():
    """Formats scores from file"""
    data = score_reader()
    for index, datum in enumerate(data):
        score_format = "%s ...... %s/%s" % (datum[0].capitalize(), datum[1], datum[2])
        print(score_format)


def difficulty_chooser():
    # Determines difficulty using a single keypress from the user.
    print("""Please choose a difficulty:\n
    1)...........Easy
    2)...........Medium
    3)...........Hard
    4)...........Very Hard""")
    while True:
        key_input = str(getch())[2:-1]
        if key_input == '1':
            return 'easy'
        elif key_input == '2':
            return 'medium'
        elif key_input == '3':
            return 'hard'
        elif key_input == '4':
            return 'very hard'
        elif key_input == '0':
            return 'debug'
        else:
            print("Please choose from one of the options.")
            continue


def difficulty_setter(difficulty):
    """Sets the difficulty, including both the range of possible integers and the number of guesses allowed"""
    if difficulty == 'easy':
        guess_range = (1, 10)
        guesses = 3
    elif difficulty == 'medium':
        guess_range = (1, 100)
        guesses = 8
    elif difficulty == 'hard' or difficulty == 'very hard':
        guess_range = (1, 1000)
        guesses = 15
    elif difficulty == 'debug' or difficulty == 'debug2':
        print("DEBUG STATE")
        guess_range = (1, 5)
        guesses = 2
    else:
        print("Not a valid difficulty")
    return guess_range, guesses, difficulty


def score_setter(difficulty, outcome):
    data = score_reader()
    if outcome == 'win':
        if difficulty == 'easy':
            data[0][1] += 1
            data[0][2] += 1
        if difficulty == 'medium':
            data[1][1] += 1
            data[1][2] += 1
        if difficulty == 'hard':
            data[2][1] += 1
            data[2][2] += 1
        if difficulty == 'very hard':
            data[3][1] += 1
            data[3][2] += 1
    if outcome == 'lose':
        if difficulty == 'easy':
            data[0][2] += 1
        if difficulty == 'medium':
            data[1][2] += 1
        if difficulty == 'hard':
            data[2][2] += 1
        if difficulty == 'very hard':
            data[3][2] += 1

    string_formatted = []
    for line in data:
        string_formatted.append("%s:%s:%s\n" % (line[0], str(line[1]), str(line[2])))

    with open('txtfiles/scores.txt', 'w') as file:
        file.writelines(string_formatted)


def state_changer(current):
    print("""\n
    1)...........Same Difficulty
    2)...........Change Difficulty
    3)...........Exit Game""")
    key_input = str(getch())[2:-1]
    print(key_input)
    if key_input == '1':
        print("\nSame difficulty.")
        return difficulty_setter(current)
    elif key_input == '2':
        print("\nChanging Difficulty...")
        return difficulty_setter(difficulty_chooser())
    elif key_input == '3':
        exit()


def game_play():
    print("Welcome.")
    difficulty = difficulty_setter(difficulty_chooser())
    while True:
        score_display()
        print("\nThe difficulty is set to", difficulty[2] + ".")
        guess_range = difficulty[0][0], difficulty[0][1]
        to_guess = randint(guess_range[0], guess_range[1])
        low_limit = guess_range[0]  # Lowest number possible. Updates with guesses.
        high_limit = guess_range[1]  # Highest number possible. Updates with guesses.
        guesses = difficulty[1]
        while guesses >= 0:
            print("The number is between", str(low_limit), "and", str(high_limit) + ".")
            try:
                user_guess = int(input(input_line))
            except ValueError:
                print("Enter a valid number.")
                continue
            if user_guess == to_guess:
                print(win_text, end='')
                winsound.PlaySound('sounds/Win.wav', winsound.SND_ASYNC)
                difficulty = state_changer(difficulty[2])
                score_setter(difficulty[2], 'win')
                break
            if guesses == 0:
                print(loss_text, end='')
                winsound.PlaySound('sounds/Lose.wav', winsound.SND_ASYNC)
                difficulty = state_changer(difficulty[2])
                score_setter(difficulty[2], 'lose')
                break
            if user_guess > to_guess:
                print("    - - - - - - - - - - - - - -\n" + str(guesses), "guesses remaining.")
                winsound.PlaySound('sounds/Down.wav', winsound.SND_ASYNC)
                if high_limit >= user_guess and difficulty[2] != 'very hard':
                    high_limit = user_guess - 1
            if user_guess < to_guess:
                print("    + + + + + + + + + + + + + +\n" + str(guesses), "guesses remaining.")
                winsound.PlaySound('sounds/Up.wav', winsound.SND_ASYNC)
                if low_limit <= user_guess and difficulty[2] != 'very hard':
                    low_limit = user_guess + 1
            guesses -= 1



winsound.PlaySound('sounds/Start.wav', winsound.SND_ASYNC)
game_play()

