# Write your code here
import sqlite3
import random

conn = sqlite3.connect('card.s3db')

cur = conn.cursor()
cur.execute(
    "CREATE TABLE IF NOT EXISTS card (id INTEGER PRIMARY KEY, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")


class Card:
    MII = 400000
    checksum = 100000001  # будет 15 цифр
    cards = {}
    cards_num = list()

    def __init__(self):
        self.checksum = Card.checksum + 1
        Card.checksum = self.checksum
        new_pin = round(random.random() * 10000)
        if new_pin < 1000:
            new_pin += 1000
        self.pin = int(new_pin)
        self.card_number = str(Card.MII) + str(self.checksum)
        self.luna()
        Card.cards_num.append(self.card_number)
        Card.cards[self.card_number] = {'number': self.card_number, 'pin': self.pin, 'balance': 0}

    def luna(self):
        number = self.card_number
        luna1 = list(number)
        luna2 = []
        num_sum = 0
        count = 0
        i = 1
        for num in luna1:
            if i == 1:
                i += 1
                num = int(num) * 2
                if int(num) > 9:
                    num2 = int(num) - 9
                    luna2.append(num2)
                    num_sum += num2
                else:
                    num_sum += num
                    luna2.append(num)
            else:
                i -= 1
                luna2.append(int(num))
                num_sum += (int(num))
        while num_sum % 10 != 0:
            num_sum += 1
            count += 1
        number += str(count)
        self.card_number = number


def create_account():
    new_card = Card()
    print("Your card has been created")
    print("Your card number:")
    print(new_card.card_number)
    print("Your card PIN:")
    print(new_card.pin)
    print("")
    cur.execute("INSERT INTO card(number, pin) VALUES(?, ?);", (new_card.card_number, new_card.pin))
    conn.commit()
    main()


def luna_check(card_transfer):
    luna1 = list(str(card_transfer))
    last_number = int(luna1.pop(15))
    luna2 = []
    num_sum = 0
    i = 1
    for num in luna1:
        if i == 1:
            i += 1
            num = int(num) * 2
            if int(num) > 9:
                num2 = int(num) - 9
                luna2.append(num2)
                num_sum += num2
            else:
                num_sum += num
                luna2.append(num)
        else:
            i -= 1
            luna2.append(int(num))
            num_sum += (int(num))
    if (num_sum + last_number) % 10 != 0:
        print(luna1, luna2, num_sum, "правда")
        return True
    else:
        print(luna1, luna2, num_sum, "ложь")
        return False


def do_transfer(card_number):
    print("Transfer")
    print("Enter card number:")
    card_transfer = int(input())
    print(card_number, card_transfer, card_transfer == int(card_number))
    if int(card_number) == card_transfer:
        print("You can't transfer money to the same account!")
    elif luna_check(card_transfer):
        print("Probably you made a mistake in the card number. Please try again!")
    elif str(card_transfer) not in Card.cards_num:
        print("Such a card does not exist.")
    else:
        print("Enter how much money you want to transfer:")
        transfer_money = int(input())
        if transfer_money > Card.cards[card_number]['balance']:
            print("Not enough money!")
        else:
            Card.cards[card_number]['balance'] -= transfer_money
            Card.cards[str(card_transfer)]['balance'] += transfer_money
            print(Card.cards[card_number]['balance'], Card.cards[str(card_transfer)]['balance'])
            cur.execute("UPDATE card SET balance = ? WHERE number = ?;", (Card.cards[str(card_number)]['balance'], int(card_number)))
            conn.commit()
            cur.execute("UPDATE card SET balance = ? WHERE number = ?;", (Card.cards[str(card_transfer)]['balance'], card_transfer))
            conn.commit()
            print("Success!")


def log_int():
    print("Enter your card number:")
    card_number = input()
    print("Enter your PIN:")
    pin = int(input())
    print("")

    def menu_2():
        print("")
        print("1. Balance")
        print("2. Add income")
        print("3. Do transfer")
        print("4. Close account")
        print("5. Log out")
        print("0. Exit")
        option2 = int(input())
        if option2 == 1:
            print("")
            print("Balance: {}".format(Card.cards[card_number]['balance']))
            menu_2()
        elif option2 == 2:  # функция увеличить деньги на банлсе
            print("")
            print("Enter income:", Card.cards[card_number]['balance'])
            income = int(input())
            Card.cards[card_number]['balance'] += income
            cur.execute("UPDATE card SET balance = balance + ? WHERE number = ?;", (income, card_number))
            conn.commit()
            print("Income was added!", Card.cards[card_number]['balance'])
            menu_2()
        elif option2 == 3:  # TO DO функция перевода денег
            print("")
            do_transfer(card_number)
            menu_2()
        elif option2 == 4:  # удалить аккаунт
            print("")
            cur.execute("DELETE FROM card WHERE number = ?;", (card_number,))
            conn.commit()
            print("The account has been closed!")
            print("")
            main()
        elif option2 == 5:
            print("You have successfully logged out!")
            print("")
            main()
        elif option2 == 0:  # выйти
            print("")
            print("Bye")

    if card_number not in Card.cards_num:
        print("Wrong card number or PIN!")
        print("")
        main()
    elif Card.cards[card_number]['pin'] != pin:
        print("Wrong card number or PIN!")
        print("")
        main()
    else:
        print("")
        print("You have successfully logged in!")
        menu_2()


def main():
    print('''1. Create an account
2. Log into account
0. Exit''')
    option = int(input())
    if option == 1:  # создать аккаунт
        create_account()
    elif option == 2:  # войти аккаунт
        log_int()
    else:  # выйти
        conn.close()
        print("Bye!")


main()
