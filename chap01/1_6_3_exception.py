# Magic number initialization
magicNumber = 3

# Main game loop
while True:
    # Player input
    word = input("What is the magic number? ")

    # Quit if the player types "quit"
    if word == "quit":
        break
    
    # Int casting with exception handling
    try:
        playerNumber = int(word)
    except ValueError:
        print("Please type a number without decimals!")
        continue
        
    # Cases that stops the game
    if playerNumber == magicNumber:
        print("This is correct! You win!")
        break
    
    # Wrong number, continue 
    print("This is not the magic number. Try again!")

# End of the program
