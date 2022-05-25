
## has access to the wordle master list and returns a set of all possible words
def get_wordmaster_answers():
    words = set()
    with open("words.txt", "r") as f:
        for line in f:
            words.add(line.strip())
    return words

## command-line input a guess, ensure it is valid
    ## TODO: add words outside of wordle scope - option to continue or re-input
    ## ^ as of current, all 5-letter series are allowed
def take_guess():
    ## make sure the guess is a valid guess!
    status = 0
    while status == 0:
        guess = input("Enter your guess: ")

        # ensure correct length
        if len(guess) != 5:
            print("Invalid guess - must be 5 letters. Try again.")
        
        else:
            #ensure letters only
            status = 1 
            alpha = "abcdefghijklmnopqrstuvwxyz"
            for let in guess:
                if let not in alpha:
                    print("Invalid guess - must be only letters. Try again.")
                    status = 0
                if status == 0:
                    break

    #print("Your guess was: ", guess)
    return guess

## takes guess, returns list of words that have any such letter
def update_possibilities(possible, guess, feedback):
    # print("Number of possiblities: ", len(possible))

    #if guess not in possible:
    #    print("That was never a valid guess")

    temppos = possible.copy()
    
    for i in range(5):
        letter = guess[i]
        # is there a green(s)? remove every word without that letter in that spot
        if feedback[i] == "green":
            for word in possible:
                if word[i] != letter:
                    temppos.remove(word)
            possible = temppos.copy()

        # is there a yellow? remove every word without that letter at all
        elif feedback[i] == "yellow":
            for word in possible:
                if letter not in word:
                    temppos.remove(word)
                elif word[i] == letter:
                    temppos.remove(word)
            possible = temppos.copy()

        # a gray? remove every word with that letter
        elif feedback[i] == "gray":
            # duplicate letter - ignore tihs one, look at the next since gray
            if letter in guess[i+1:]:
                break

            for word in possible:
                if letter in word:
                    temppos.remove(word)
            possible = temppos.copy()

    print("Number of new possibilities: ", len(possible))
    view = input("Would you like to see the possibities? (y/n): ")
    if view == "y":
        if len(possible) == 0:
            print("Must've messed up. No possibilities left.")
        else:
            print(possible)
    return possible

## takes feedback recieved, returns array with colors
def take_feedback():
    ## make sure the feedback is a valid
    status = 0
    while status == 0:
        feedback = input("Enter your feedback (0 = gray, 1 = yellow, 2 = green): ")

        if feedback == "22222":
            return 1

        # ensure correct length
        if len(feedback) != 5:
            print("Invalid feedback - must be 5 numbers. Try again.")
        
        else:
            #ensure 0,1,2 only
            status = 1 
            valid = "012"
            for let in feedback:
                if let not in valid:
                    print("Invalid form of feedback - must be only 0, 1, or 2. Try again.")
                    status = 0
                if status == 0:
                    break
    
    # turn into array with colors
    arr = [0 for i in range(5)]
    i = 0
    for let in feedback:
        if let == "0":
            arr[i] = "gray"
            i += 1
        if let == "1":
            arr[i] = "yellow"
            i += 1
        if let == "2":
            arr[i] = "green"
            i += 1
    return arr

if __name__ == "__main__":
    possible = get_wordmaster_answers()
    print("Number of possibilities: ", len(possible))
    
    for i in range(6):
        current = take_guess()
        colors = take_feedback()
        if colors == 1:
            print("Good work. You did it.")
            break
        possible = update_possibilities(possible, current, colors)
    
    
# TODO: NEED TO FIX WHEN LETTER IS SEEN TWICE, SECOND TIME GRAY

