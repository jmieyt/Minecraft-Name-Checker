import requests, time, fade, os, string, random
from colorama import Fore
from threading import Thread
# Pre Start
os.system('color')

proxys = []
proxyCount = 0
def scrapProxies():
    global proxys
    global proxyCount
    r = requests.get(
        "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=https&timeout=10000&country=all&ssl=all&anonymity=all",
        headers={
            'User-Agent':
            'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'
        })
    try:
        for i in range(10000):
            proxys.append(
                r.text.split('\r')[i].replace('\r',
                                            '').replace(' ',
                                                        '').replace('\n', ''))
    except IndexError:
        pass

    for item in proxys:
        proxyCount += 1
    print("DEBUG Scrapped Proxys: " + str(proxyCount))

scrapProxies()

def generatingName(letter):
    code = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=int(letter)))
    return code

def checkName(name):
    try:
        choosedProxy = proxys[random.randint(1, proxyCount -1)]
        r = requests.get("https://api.mojang.com/users/profiles/minecraft/" + name, proxies={'https':choosedProxy}, headers={
                'User-Agent':
                'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'
        })
        if '200' in str(r.status_code):
            print(Fore.RED + "          TAKEN " + name + " " +Fore.BLUE + choosedProxy)
        elif '204' in str(r.status_code):
            print(Fore.GREEN + "        AVAILABLE " + name + " " + Fore.BLUE + choosedProxy)
        else:
            print(Fore.YELLOW + "       Ratelimited " + choosedProxy)
    except Exception as e:
        if 'proxy' in str(e):
            pass 

def checkFull(letter):
    while True:
        checkName(generatingName(letter))

def clear():
    os.system('cls')

def mainMenu():
    clear()
    print(fade.water("""
   __  ________  __  __                                  _______           __          
  /  |/  / ___/ / / / /__ ___ _______  ___ ___ _  ___   / ___/ /  ___ ____/ /_____ ____
 / /|_/ / /__  / /_/ (_-</ -_) __/ _ \/ _ `/  ' \/ -_) / /__/ _ \/ -_) __/  '_/ -_) __/
/_/  /_/\___/  \____/___/\__/_/ /_//_/\_,_/_/_/_/\__/  \___/_//_/\__/\__/_/\_\\__/_/   
                                                                                       
"""))
    print(Fore.BLUE + "     Press Enter to start")
    print(Fore.RED + " Coded by 𝙟𝙢𝙞𝙚𝙮𝙩𝟭𝟯𝟯𝟳#9743")
    input()

    print(Fore.BLUE + "     How many Letters? ")
    letters = input()
    print(Fore.BLUE + "     Threads?")
    threads1 = int(input())
    print(Fore.BLUE + "     Alright, generating and checking Names with " + Fore.CYAN + str(letters) + Fore.BLUE + " Letters and " + Fore.CYAN + str(threads1) + Fore.BLUE + " Threads!")
    threads = []
    threadNumber = threads1
    for i in range(threadNumber):
        t = Thread(target=checkFull, args=(letters))
        t.daemon = True
        threads.append(t)
    for i in range(threadNumber):
        threads[i].start()
    for i in range(threadNumber):
        threads[i].join()

mainMenu()