import random

magicNumber = random.randint(1,10)
while True:
    word = input("What is the magic number? ")
    if word == "quit":
        break
    
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
    
    print("This is not the magic number. Try again!")
