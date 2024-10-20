# Import the random package
import random

# Generate a random Magic number
magicNumber = random.randint(1,10)
# An integer to count the guesses
guessCount = 0
while True:
    # Player input
    word = input("What is the magic number? ")
    # Quit if the player types "quit"
    if word == "quit":
        break
    # Increase the number of guesses
    guessCount += 1
    
    # Int casting with exception handling
    try:
        playerNumber = int(word)
    except ValueError:
        print("Please type a number without decimals!")
        continue
        
    # Cases
    if playerNumber == magicNumber:
        print("This is correct! You win!")
        break
    elif magicNumber < playerNumber:
        print("The magic number is lower")
    elif magicNumber > playerNumber:
        print("The magic number is higher")
    
    # Wrong number, continue 
    print("This is not the magic number. Try again!")

print("You guessed the magic number in {} guesses.".format(guessCount))
