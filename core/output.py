from colorama import Fore, Style, init

init(autoreset=True)

QUIET = False
VERBOSE = False

def configure(quiet=False, verbose=False):
    global QUIET, VERBOSE
    QUIET = quiet
    VERBOSE = verbose

def info(msg):
    if not QUIET:
        print(f"{Fore.CYAN}[i]{Style.RESET_ALL} {msg}")

def success(msg):
    if not QUIET:
        print(f"{Fore.GREEN}[+]{Style.RESET_ALL} {msg}")

def warning(msg):
    if VERBOSE and not QUIET:
        print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} {msg}")

def error(msg):
    print(f"{Fore.RED}[-]{Style.RESET_ALL} {msg}")

def debug(msg):
    if VERBOSE and not QUIET:
        print(f"{Fore.BLUE}[debug]{Style.RESET_ALL} {msg}")

def header(msg):
    if not QUIET:
        print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{msg}{Style.RESET_ALL}")

