repeat = True
while repeat:
    word = input("Enter the magic word: ")
    if word == "please":
        print("This is correct, you win!")
        repeat = False
    else:
        print("This is not correct, try again!")
print("Thank you for playing this game!")
