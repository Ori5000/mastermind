from random import randint
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich import box, print
from ctypes import windll

def getDigits(number):
    return [int(digit) for digit in str(number)]

def noDuplicates(number):
    number = getDigits(number)
    if len(number) == len(set(number)):
        return True
    else:
        return False

def genCode():
    while True:
        code = randint(1000, 9999)
        if noDuplicates(code):
            return code

def numOfBullsCows(number, guess):
    number_list = getDigits(number)
    guess_list = getDigits(guess)
    BullsCows = [0,0] 
    for N, G in zip(number_list, guess_list):
        if G in number_list:
            if G == N:
                BullsCows[0] += 1
            else:
                BullsCows[1] += 1
    return BullsCows

windll.kernel32.SetConsoleTitleW(f'BULLS & COWS')
code = genCode()
try:
    tries = int(input('ENTER number OF TRIES (DEFAULT = 10): '))
except:
    tries = 10
windll.kernel32.SetConsoleTitleW(f'BULLS & COWS  |  {tries} TRIES LEFT')
table = Table(title='BULLS & COWS', title_style='bright_white', box=box.SIMPLE)
with Live(table):
    table.add_column("GUESS", style='bright_white')
    table.add_column("BULLS", style='dodger_blue1')
    table.add_column("COWS", style='deep_sky_blue1')
    table.add_column("TRIES LEFT")

while tries > 0:
    try:
        guess = int(input(f"WHAT'S YOUR GUESS: "))
    except KeyboardInterrupt:
        exit()
    except:
        print('YOUR GUESS NEEDS TO BE A NUMBER BETWEEN 1000 AND 9999!')
        continue
    if not noDuplicates(guess):
        print('YOUR GUESS CANNOT CONTAIN DUPLICATES!')
        continue
    if 1000 > guess or guess > 9999:
        print('YOUR GUESS NEEDS TO BE BETWEEN 1000 AND 9999!')
        continue
    bulls_cows = numOfBullsCows(code, guess)
    with Live(table):
        Console().clear()
        tries -= 1
        table.add_row(str(guess), str(bulls_cows[0]), str(bulls_cows[1]), str(tries))
 
    if bulls_cows[0] == 4:
        print('[bright_green]YOUR GUESS IS RIGHT, YOU WON![/bright_green]')
        break
    windll.kernel32.SetConsoleTitleW(f'BULLS & COWS  |  {tries} TRIES LEFT')
else: 
    print(f'[bright_red]YOU RAN OUT OF TRIES, THE NUMBER WAS {code}![/bright_red]')