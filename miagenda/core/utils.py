from colorama import Fore, Back, Style


def debug(*args):
    print(Back.BLUE + 'DEBUG:', Style.RESET_ALL, end=' ')

    for arg in args:
        print(Fore.BLUE, arg, end=' ')

    print(Style.RESET_ALL)
