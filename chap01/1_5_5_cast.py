magicNumber = 3
while True:
    word = input("What is the magic number? ")
    playerNumber = int(word)
    if playerNumber == magicNumber:
        print("This is correct! You win!")
        break
    print("This is not the magic number. Try again!")
