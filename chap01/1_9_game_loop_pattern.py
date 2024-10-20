# Import the random package
import random


def init():
    """
    Initialize game
    
    Outputs:
      * gameStatus
      * magicNumber
    """
    # Generate a random Magic number
    return "init", random.randint(1, 10)


def processInput():
    """
    Handle player's input
    
    Output:
      * playerNumber: the number entered by the player, or None if the player wants to stop the game
    """

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


def update(gameStatus, magicNumber, playerNumber):
    """
    Update game state
    
    Inputs:
      * gameStatus: the status of the game
      * magicNumber: the magic number to find
      * playerNumber: the number entered by the player
    Output:
      * gameStatus: the status of the game
      * magicNumber: the magic number to find
    """
    if playerNumber is None:
        gameStatus = "end"
    elif playerNumber == magicNumber:
        gameStatus = "win"
    elif magicNumber < playerNumber:
        gameStatus = "lower"
    elif magicNumber > playerNumber:
        gameStatus = "higher"

    return gameStatus, magicNumber


def render(gameStatus, magicNumber):
    """
    Render game state
    
    Input:
      * gameStatus: the status of the game, "win", "end", "lower" or "higher"
    """
    # Cases
    if gameStatus == "win":
        print("This is correct! You win!")
    elif gameStatus == "end":
        print("Bye!")
    elif gameStatus == "lower":
        print("The magic number is lower")
    elif gameStatus == "higher":
        print("The magic number is higher")
    else:
        raise RuntimeError("Unexpected game status {}".format(gameStatus))


def runGame():
    gameStatus, magicNumber = init()
    while gameStatus != "win" and gameStatus != "end":
        playerNumber = processInput()
        gameStatus, magicNumber = update(gameStatus, magicNumber, playerNumber)
        render(gameStatus, magicNumber)


# Launch the game
runGame()
