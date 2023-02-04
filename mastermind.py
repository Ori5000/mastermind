from random import sample
from rich.table import Table
from rich.live import Live
from rich import box, print as printr
from ctypes import windll
from msvcrt import getch, putwch
from string import digits

def getDigits(number):
    return [int(digit) for digit in str(number)]

def noDuplicates(number):
    number = getDigits(number)
    if len(number) == len(set(number)):
        return True
    else:
        return False

def genCode():
    code = ''.join(map(str,sample((0,1,2,3,4,5), 4)))
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

windll.kernel32.SetConsoleTitleW(f'MASTERMIND')
code = genCode()

REPLACEMENTS = [
('0', '[bright_cyan]●[/bright_cyan]'),
('1', '[cyan]●[/cyan]'),
('2', '[bright_green]●[/bright_green]'),
('3', '[bright_red]●[/bright_red]'),
('4', '[bright_yellow]●[/bright_yellow]'),
('5', '[bright_magenta]●[/bright_magenta]')
]
COLORS = [
('0', '\033[1;36m'),
('1', '\033[0;36m'),
('2', '\033[1;32m'),
('3', '\033[1;31m'),
('4', '\033[1;33m'),
('5', '\033[1;35m')
]
error = ''

try:
    tries = int(input('ENTER NUMBER OF TRIES (DEFAULT = 10): '))
except:
    tries = 10
windll.kernel32.SetConsoleTitleW(f'MASTERMIND  |  {tries} TRIES LEFT')
print('\033c')
table = Table(title='MASTERMIND', title_style='bright_white', box=box.SIMPLE)
with Live(table):
    table.add_column("GUESS", style='bright_white')
    table.add_column("BULLS", style='dodger_blue1')
    table.add_column("COWS", style='deep_sky_blue1')
    table.add_column("TRIES LEFT")

while tries > 0:
    if error != True:
        for num, color in REPLACEMENTS:
            printr(f'[white]{num} = [/white]{color}')
    error = ''
    putwch('\n')
    for letter in "WHAT'S YOUR GUESS: ":
        putwch(letter)
    guess = ''
    while True:
        key = getch()
        match key:
            case b'\x1b' | b'\x03' | b'q' | b'\x17':
                print('\033c', end='')
                printr('[bright_red]QUITTED![/bright_red]')
                exit()
            case b'\x08':
                if guess != '':
                    putwch('\b')
                    putwch(' ')
                    putwch('\b')
                    guess = guess[:-1]
            case _ if len(guess) == 4:
                putwch('\n')
                break
            case key if key in digits[:-4].encode():
                print(f'{COLORS[int(key.decode())][1]}●\033[0;37m', end='', flush=True)
                guess += key.decode()
    if not noDuplicates(guess):
        print('YOUR GUESS CANNOT CONTAIN DUPLICATES!')
        error = True
        continue
    # if not all(list(map(lambda x : True if x in ['0', '1', '2', '3', '4', '5'] else False, *[str(guess)]))):
    #     printr('YOUR GUESS NEED TO CONTAIN ONLY 0, 1, 2, 3, 4 & 5!')
    #     continue
    bulls_cows = numOfBullsCows(code, guess)
    for old, new in REPLACEMENTS:
        guess = guess.replace(old, new)
    with Live(table):
        print('\033c')
        tries -= 1
        table.add_row(guess, str(bulls_cows[0]), str(bulls_cows[1]), str(tries))
    if bulls_cows[0] == 4:
        printr('[bright_green]YOUR GUESS IS RIGHT, YOU WON![/bright_green]')
        break
    windll.kernel32.SetConsoleTitleW(f'MASTERMIND  |  {tries} TRIES LEFT')
else:
    for old, new in REPLACEMENTS:
        code = code.replace(old, new)
    printr(f'[bright_red]YOU RAN OUT OF TRIES, THE CODE WAS[/bright_red] {code}[bright_red]![/bright_red]')