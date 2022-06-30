from rich.console import Console
from requests import exceptions
import requests
import sys
import os
import json


from difflib import SequenceMatcher
from github import Github
from rich import pretty
pretty.install()
cdir = os.popen('curr.bat').read()

p = Console()

ld = len(sys.argv)
grawerf = f"{cdir}grawer.ypm".replace("\n","")
grawer = []

g = Github()

if os.path.exists(grawerf) == False:
    open(grawerf, "a+") 

for gacc in open(grawerf).readlines():
    s = gacc.replace("\n", "")
    if s.strip() == "":
        continue
    grawer.append(s)

def checkGUser(user: str):
    url = f"https://api.github.com/users/{user}"
    try:
        r = requests.get(url.format(user)).json()
    except exceptions.ConnectionError:
        p.print(" [bold blue]i[/] -> No connection.")
        sys.exit(1)
    try:
        if "API rate limit" in r['message']:
            p.print(" [blue bold]i[/] -> It seems that you have been rate limited. Try again tomorrow or use proxy.") 
            return False, True
    except:
        pass
    try:
        s = r['login']
        for i in grawer:
            if SequenceMatcher(None, i, s).ratio() > 0.8:
                return True, True
        return True, False
    except KeyError:
        return False, False

def help():
    print(''' Usage: ypm [OPTIONS] [ARGUMENTS]

 Options:                                        
    - help      | Display help or this. Argument: NONE
    - add       | Add account into the drawer. Argument: (Account Name)
    - delete    | Delete account from the drawer. Argument: (Account Name)
    - graws     | Returns list of added accounts. Argument: NONE
    ''')
    sys.exit(0)


if __name__ == "__main__":
    print("")
    if len(sys.argv) == 1:
        help()

    if sys.argv[1] == "delete":
        if (len(sys.argv) == 3) == True:
            if sys.argv[2] not in grawer:
                Dx = 0
                for i in grawer:
                    if SequenceMatcher(None, sys.argv[2], i).ratio() > 0.488888888:
                        d = p.input(f" [bold magenta]?[/] -> You mean {i}? y/n > ")
                        if d.strip() == "N" or d.strip() == "n":
                            p.print(" [bold blue]i[/] -> Try again, with the exact name.")
                            sys.exit(0)
                        sys.argv[2] = i
                        break
                if sys.argv[2] not in grawer:
                    p.print(" [bold red]ERR[/] -> Account not found, please try again with the exact name.")
                    sys.exit()

            with open(grawerf, "r") as file:
                filedata = file.read()
            
            filedata = filedata.replace(sys.argv[2], "")

            p.print(" [bold green][i]Ok[/][/] -> Account removed.")
            with open(grawerf, "w") as file:
                file.write(filedata)

    if sys.argv[1] == "graws":
        if len(grawer) == 0:
            p.print(f" [bold blue]i[/] -> There is no account in the drawer, maybe you could add some?")
            sys.exit(0)
        for ix in grawer:
            dix = 0
            ds = checkGUser(ix)
            if ds[0] != True:
                if ds[1] == True:
                    sys.exit(1)
                p.print(f" [bold red]ERR[/] -> Invalid user : {ix}, please remove with delete option")
                sys.exit(1)
            repcount = f"https://api.github.com/users/{ix}/repos?per_page=100"
            try:
                rep = requests.get(repcount)
                rep = json.loads(rep.text)
                rep = len(rep)
                if rep == 100:
                    now = 2
                    while True:
                        dix += rep
                        rep2 = requests.get(f"https://api.github.com/users/{ix}/repos?per_page=100&page={now}")
                        rep2 = json.loads(rep2.text)
                        rep2 = len(rep2)
                        dix += rep2
                        if rep2 == rep*now:
                            now += 1
                        else:
                            break
                    p.print(f" [bold yellow]Acc[/] -> [blue]{ix}[/] :: has {dix} repos [bold green]++[/] ")
                    continue
            except exceptions.ConnectionError:
                p.print(" [blue]i[/] -> There is no internet connection available. Please retry")
                sys.exit(1)
            if int(rep) > 50:
                p.print(f" [bold yellow]Acc[/] -> [blue]{ix}[/] :: has {rep} repos [bold green]+[/]")
                continue
            p.print(f" [bold yellow]Acc[/] -> [blue]{ix}[/] :: has {rep} repos ")

    if sys.argv[1] == "add":
        if (len(sys.argv) == 3) == True:
            p.print(" [bold blue]i[/] -> Checking availability of [underline]github[underline] account.") 
            Dib = checkGUser(sys.argv[2].strip())
            if Dib[0] == True:
                if Dib[1] == True:
                    p.print(" [bold blue]i[/] -> Account exist, already added in the drawer.")
                    sys.exit(0)
                p.print(" [bold green][i]Ok[/][/] -> Account found, adding it into the drawer.")
                with open(grawerf, 'a+') as grw:
                    grw.write("\n"+sys.argv[2].strip())
                sys.exit(0)
            if Dib[0] == False:
                if sys.argv[2].strip in grawer:
                    p.print(" [bold blue]i[/] -> Github account not found but listed in the drawer, removing..")
                    with open(grawerf, "r") as f:
                        fs = f.read()
                    fs = fs.replace(sys.argv[2], "")
                    p.print(" [green bold][i]Ok[/][/] -> Unknown account removed.")
                    sys.exit(0)
                p.print(" [bold red]ERR[/] -> [red underline]Github account not found[/]")

        else:
            help("add")
    if sys.argv[1] == "help":
        help()