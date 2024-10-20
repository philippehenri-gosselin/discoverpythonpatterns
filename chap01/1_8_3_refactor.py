import random

def runGame():
    magicNumber = random.randint(1,10)
    guessCount = 0
    while True:
        word = input("What is the magic number? ")
        if word == "quit":
            break
        
        try:
            playerNumber = int(word)
        except ValueError:
            print("Please type a number without decimals!")
            continue
            
        guessCount += 1
        if playerNumber == magicNumber:
            print("This is correct! You win!")
            print("You guessed the magic number in {} steps.".format(guessCount))
            break
        elif magicNumber < playerNumber:
            print("The magic number is lower")
        elif magicNumber > playerNumber:
            print("The magic number is higher")
        
        print("This is not the magic number. Try again!")  

while True:
    print("Game menu")
    print("1) Start a new game")
    print("2) Quit")

    choice = input("Enter your choice:")
    if choice == "1":
        runGame()
    elif choice == "2":
        break
