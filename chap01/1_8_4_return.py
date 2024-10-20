# Import the random package
import random

def askPlayer():
    while True:
        # Player input
        word = input("What is the magic number? ")
        # Quit if the player types "quit"
        if word == "quit":
            return None

        # Int casting with exception handling
        try:
            playerNumber = int(word)
            break
        except ValueError:
            print("Please type a number without decimals!")
            continue
        
    return playerNumber


def runGame():
    # Generate a random Magic number
    magicNumber = random.randint(1,10)
    # An integer to count the guesses
    guessCount = 0
    while True:
        playerNumber = askPlayer()
        if playerNumber is None:
            break        
        # Increase the number of guesses
        guessCount += 1
                    
        # Cases
        if playerNumber == magicNumber:
            print("This is correct! You win!")
            print("You guessed the magic number in {} steps.".format(guessCount))
            break
        elif magicNumber < playerNumber:
            print("The magic number is lower")
        elif magicNumber > playerNumber:
            print("The magic number is higher")
        
        # Wrong number, continue 
        print("This is not the magic number. Try again!")
    

runGame()
