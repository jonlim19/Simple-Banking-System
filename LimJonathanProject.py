def read_nonempty_string(prompt):  # Checking for an empty string and prompting user to enter one if so
    something_is_wrong = True
    while something_is_wrong:
        s = input(prompt)
        if len(s) > 0:
            something_is_wrong = False
        else:
            print("Please type something...")
    return s


def read_nonnegative_integer(prompt):  # Checking for a blank integer value and looping until user enters 1
    something_is_wrong = True
    while something_is_wrong:
        try:
            number = int(input(prompt))
            if number >= 0:
                something_is_wrong = False
            else:
                print("Non-negative numbers please...")
        except:
            print("Must be numeric...")
    return number


def process_choice(acc_list, names, balance):  # menu function
    menu = "What would you like to do?:,\n" \
           "1. Open an account \n" \
           "2. Close an account \n" \
           "3. Withdraw money \n" \
           "4. Deposit money \n" \
           "5. Generate report for management \n" \
           "6. Quit \n" \
           "==>"
    active = True
    while active:  # Loops through the menu until user presses 6 to quit and write to file
        try:
            print(menu)
            choice = int(input("Please select a number: "))
            if choice > 6 or choice < 1:
                print("Please choose a value between 1 to 6!")
            elif choice == 1:
                acc_list, names, balance = open_account(acc_list, names, balance)
            elif choice == 2:
                acc_list, names, balance = delete_account(acc_list, names, balance)
            elif choice == 3:
                acc_list, balance = withdraw(acc_list, balance)
            elif choice == 4:
                acc_list, balance = deposit(acc_list, balance)
            elif choice == 5:
                balance = generate_report(names, balance)
            elif choice == 6:
                quit_and_write(acc_list, names, balance)
                active = False
        except:
            print("Please enter numeric values!")  # Warning users to only write numbers


def open_account(acc_list, names, balance):  # function to create an account
    import random
    acc_num = random.randint(100000, 999999)  # Generate a random 6 digit account number
    acc_fname = read_nonempty_string("Please enter your first name: ").capitalize()
    acc_lname = read_nonempty_string("Please enter your last name: ").capitalize()
    fullname = acc_fname + " " + acc_lname
    acc_list.append(acc_num)
    names.append(fullname)  # Appends the fullname of the customer
    balance.append(0)
    print(acc_list, names, balance)
    return acc_list, names, balance


def delete_account(acc_list, names, balance):
    del_acc = read_nonempty_string("Please enter account number you would like to delete: ")
    # User inputs account number he/she wants to delete
    if del_acc in acc_list:  # checks if the account entered is in the list.
        for del_bal in balance:
            if acc_list.index(del_acc) in balance.index(del_bal):  # checks if for other info associated with account
                balance.remove(del_bal)  # removes the balance associated with the account number
        for del_name in names:
            if acc_list.index(del_acc) in names.index(del_name):  # checks if for other info associated with account
                names.remove(del_name)  # removes the name associated with the account number
        acc_list.remove(del_acc)  # Removes the account from list
        print("Account has been deleted")
    else:
        print("Account does not exist!")
    return acc_list, names, balance


def deposit(acc_list, balance):
    login = read_nonempty_string("Please enter account number: ")  # user selects account number to deposit money into
    if login in acc_list:  # Condition to only proceed when the account entered is contained in the list
        lodge = read_nonnegative_integer("Enter amount you want to deposit?: ")  # User inputs amount of cash to lodge
        for selected_acc_bal in balance:
            if balance.index(selected_acc_bal) is acc_list.index(login):
                balance[balance.index(selected_acc_bal)] = selected_acc_bal + lodge  # Adds the money to the balance
                print("Successful transaction!")
    else:
        print("Account doesn't exist!")  # Warning for user if the account isn't found
    return acc_list, balance


def withdraw(acc_list, balance):
    login = read_nonempty_string("Please enter account number: ")  # user selects account number to deposit money into
    if login in acc_list:
        amount = read_nonnegative_integer("Enter amount you want to withdraw?: ")
        for selected_acc_bal in balance:
            if balance.index(selected_acc_bal) is acc_list.index(login):
                if selected_acc_bal >= amount:  # Checks if there is enough money in the account
                    balance[balance.index(selected_acc_bal)] = selected_acc_bal - amount  # Deducts the money withdrawn
                    print("Successful transaction!")
                else:
                    print("Insufficient funds!")  # Message to the customer if there isn't enough money in account
    else:
        print("Account doesn't exist!")
    return acc_list, balance


def generate_report(names, balance):
    bank_file = open("data.txt")  # Opens file
    bank_data = bank_file.read()  # reads data from file
    print(bank_data)  # prints the data from file
    total_balance = sum(balance)  # Determines the total balance of deposit in the bank
    largest_bank_amount = max(balance)  # determines the largest deposit
    for large in names:
        if names.index(large) == balance.index(largest_bank_amount):
            # Maching the name of the acccount holder to the largest amount deposited
            print("The Largest bank deposit is ", largest_bank_amount, "owned by: ", large)
    print("Total amount on deposit in the bank is", total_balance)
    bank_file.close()
    return balance


def quit_and_write(acc_list, names, balance):  # Opening a file and writing to it every time user quits.
    i = 0
    acc_file = open("data.txt", "w+")  # Opening the file
    while i < len(acc_list):
        text = (str(acc_list[i]) + " " + str(names[i]) + " " + str(balance[i]) + "\n")  # Writing to the file
        acc_file.write(text)
        i += 1
    acc_file.close()


def load():
    # Below is the lists used
    acc_list = []
    names = []
    balance = []
    bank_file = open("data.txt")  # Opening the file to read from it
    reading_file = True
    while reading_file:
        bank_file_line = bank_file.readline()
        if bank_file_line == "":
            break
        bank_file_line_split = bank_file_line.split()  # Splitting data into 4 different columns
        acc_list.append(bank_file_line_split[0])
        fullname = bank_file_line_split[1] + " " + bank_file_line_split[2]
        balance.append(float(bank_file_line_split[3]))
        names.append(fullname)
    bank_file.close()
    return acc_list, names, balance


def main():
    acc_list, names, balance = load()
    process_choice(acc_list, names, balance)


main()
