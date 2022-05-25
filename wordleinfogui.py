import tkinter as tk
from tkinter import simpledialog
from tkinter import *
from tkinter import messagebox

def get_wordmaster_answers():
    words = set()
    with open("words.txt", "r") as f:
        for line in f:
            words.add(line.strip())
    return words

possible = get_wordmaster_answers()

alpha = "abcdefghijklmnopqrstuvwxyz"
valid = "012"

window = Tk()
window.geometry('600x300')
window.title("Wordle Info")

header = Label(window, text="~~~Info based upon Wordle progress~~~", font=("Arial Bold", 20))
header.grid(column=0, row=0)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ GUESS STUFF ~~~~~~~~~~~~~~~~~~~~~~~~~~~
wordPrompt = Label(window, text = "Input your word: ")
wordPrompt.grid(column = 0, row = 1)

word = Entry(window,width=10)
word.grid(column=1, row=1)

guessInfo = Label(window, text = "")
guessInfo.grid(column = 0, row = 2)

def clickedOK():
    status = 0
    guess = word.get().lower()
    # make sure it's letters only
    for let in guess:
        if let not in alpha:
            status = 1
    # and that it's 5 letters
    if len(guess) == 5 and status == 0:
        res = "Your guess was " + guess.upper()
        guessInfo.configure(text = res)
    else:
        guessInfo.configure(text = "Your guess must be 5 letters. Try again.")

def clickedCONFIRM():
    guess = word.get().lower()
    status = 0
    for let in guess: 
        if let not in alpha:
            status = 1
    if len(guess) == 5 and status ==0:
        global currentGuess 
        currentGuess = guess
    else:
        guessInfo.configure(text = "Your guess must be 5 letters. Try again.")

btOK = Button(window, text = "OK", command = clickedOK)
btOK.grid(column = 2, row = 1)

btCONFIRM = Button(window, text = "CONFIRM", command = clickedCONFIRM)
btCONFIRM.grid(column = 1, row = 2)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ FEEDBACK STUFF ~~~~~~~~~~~~~~~~~~~~~~~~
feedbackPrompt = Label(window, text = "Input the feedback you recieved: \n (0 = gray, 1 = yellow, 2 = green)")
feedbackPrompt.grid(column = 0, row = 3)

feedback = Entry(window,width=10)
feedback.grid(column=1, row=3)

feedbackInfo = Label(window, text = "")
feedbackInfo.grid(column = 0, row = 4)

def clickedOK2():
    status = 0
    info = feedback.get()
    # make sure it's 0,1,2 only
    for num in info:
        if num not in valid:
            status = 1
    # and that it's 5 letters
    if len(info) == 5 and status == 0:
        colored = [0 for i in range(5)]
        for i in range(5):
            if info[i] == "0":
                colored[i] = "GRAY"
            if info[i] == "1":
                colored[i] = "YELLOW"
            if info[i] == "2":
                colored[i] = "GREEN"
        colorstr = ", ".join(colored)
        res = "Your feedback was: [" + (colorstr) +"]"
        feedbackInfo.configure(text = res)
    else:
        feedbackInfo.configure(text = "Your guess must be 5 digits - 0, 1, or 2. Try again.")

btOK2 = Button(window, text = "OK", command = clickedOK2)
btOK2.grid(column = 2, row = 3)

def clickedCONFIRM2():
    info = feedback.get()
    if len(info) == 5:
        colored = [0,0,0,0,0]
        for i in range(5):
            if info[i] == "0":
                colored[i] = "GRAY"
            if info[i] == "1":
                colored[i] = "YELLOW"
            if info[i] == "2":
                colored[i] = "GREEN"
        global currentInfo
        currentInfo = colored
    else: 
        feedbackInfo.configure(text = "Your guess must be 5 digits - 0, 1, or 2. Try again.")

btCONFIRM2 = Button(window, text = "CONFIRM", command = clickedCONFIRM2)
btCONFIRM2.grid(column = 1, row = 4)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~ POSSIBILITIES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
number = str(len(possible))
possibleInfo = Label(window, text = "There are currently " + number + " possible words.")
possibleInfo.grid(column = 0, row = 6)

possiblePrompt = Label(window, text = "Would you like to see the new number of possibilities?")
possiblePrompt.grid(column = 0, row = 7)

possibleFeedback = Label(window, text = "")
possibleFeedback.grid(column = 0, row = 8)

def updatePossible(currentGuess, currentInfo):
    global possible
    temppos = possible.copy()
    for i in range(5):
        letter = currentGuess[i]
        # is there a green(s)? remove every word without that letter in that spot
        if currentInfo[i] == "GREEN":
            for word in possible:
                if word[i] != letter:
                    temppos.remove(word)
            possible = temppos.copy()

        # is there a yellow? remove every word without that letter at all
        elif currentInfo[i] == "YELLOW":
            for word in possible:
                if letter not in word:
                    temppos.remove(word)
                elif word[i] == letter:
                    temppos.remove(word)
            possible = temppos.copy()

        # a gray? remove every word with that letter
        elif currentInfo[i] == "GRAY":
            # duplicate letter - ignore tihs one, look at the next since gray
            if letter in currentGuess[i+1:]:
                break

            for word in possible:
                if letter in word:
                    temppos.remove(word)
            possible = temppos.copy()

    newNumber = str(len(possible))
    possibleInfo.configure(text = "There are now " + newNumber + " possible words.")


def clickedYES():
    status = 0
    if 'currentGuess' not in globals():
        status += 1
    if 'currentInfo' not in globals():
        status += 2
    if status == 1:
        possibleFeedback.configure(text ="Ruh-roh. You never confirmed your word.")
    if status == 2:
        possibleFeedback.configure(text = "Ruh-roh. You never confirmed your feedback.")
    if status == 3:
        possibleFeedback.configure(text ="Ruh-roh. You never confirmed your word or feedback.")
    if status == 0:
        possibleFeedback.configure(text="")
        updatePossible(currentGuess, currentInfo)


btYES = Button(window, text = "YES", command = clickedYES)
btYES.grid(column = 1, row = 7)
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

word.focus()
window.mainloop()

# TODO: fix the same things that are wrong in wordleinfo.py

