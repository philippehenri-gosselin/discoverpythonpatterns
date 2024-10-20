while True:
    word = input("Enter the magic word: ")
    if word != "please":
        print("This is not correct, try again!")
        continue
    print("This is correct, you win!")
    break
print("Thank you for playing this game!")
