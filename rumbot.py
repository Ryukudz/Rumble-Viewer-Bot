from apscheduler.schedulers.background import BackgroundScheduler
from concurrent.futures import ThreadPoolExecutor
from colorama import Fore, init, Style
from datetime import datetime
import argparse as a
import random
import string
import requests as r


print(Fore.RED + '''
\t┬─┐┬ ┬┌┬┐┌┐ ┌─┐┌┬┐┌─┐
\t├┬┘│ ││││├┴┐│ │ │ └─┐
\t┴└─└─┘┴ ┴└─┘└─┘ ┴ └─┘''')
print(Fore.YELLOW + '\tcoded by github.com/Ryukudz 🥷\n')
print(Style.RESET_ALL)

#headers are not required :)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    'Referer': 'https://rumble.com/',
    'Origin': 'https://rumble.com'
}

inv = BackgroundScheduler()
init(autoreset=True)


def ValidStream(video_id):
    url = f"https://wn0.rumble.com/service.php?video={video_id}&name=video.watching_now"
    req = r.get(url)
    data = req.json()
    if "viewer_count" in data.get("data", {}):
        return True
    else:
        raise ValueError("Invalid video id.")

def GenBots(count):
    char = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ["".join(random.choices(char, k=8)) for _ in range(count)]


def ViewBot(video_id, viewer_id):
    target = "https://wn0.rumble.com/service.php?name=video.watching_now"
    data = {"video": video_id, "viewer_id": viewer_id}
    r.post(target, data=data, headers=headers, timeout=15)


def ViewCount(video_id, bot_count):
    def GetCount():
        url = f"https://wn0.rumble.com/service.php?video={video_id}&name=video.watching_now"
        response = r.get(url)
        data = response.json()
        count = data["data"]["viewer_count"]
        now = datetime.now().strftime("[%H:%M:%S]")
        print(Fore.GREEN + f"{now}" + Fore.WHITE + " Viewer Count:" + f"{count}")

    def launch(viewer_id):
        ViewBot(video_id, viewer_id)

    try:
        if not ValidStream(video_id):
            raise ValueError("Invalid video id.")
    except ValueError as e:
        print(Fore.RED + "[x] " + Fore.WHITE + str(e))
        exit()

    viewer_ids = GenBots(bot_count)
    now = datetime.now().strftime("[%H:%M:%S]")
    print(Fore.GREEN + f"{now}" + Fore.BLUE + " 🚀 🚀 🚀 ...Launching Rocket Ships... 🚀 🚀 🚀")
    print(Fore.GREEN + "[INFO]" + Fore.WHITE + " The viewers are expected to arrive within the next five minutes ⏳")
    print(Fore.GREEN + "[INFO] " + Fore.WHITE + "Once you are done, Press ENTER to exit 👾\n")

    with ThreadPoolExecutor(max_workers=100) as executor:
        for viewer_id in viewer_ids:
            executor.submit(launch, viewer_id)

    inv.add_job(lambda: list(map(launch, viewer_ids)), 'interval', minutes=4)
    inv.add_job(GetCount, 'interval', minutes=4)
    inv.start()

    while True:
        user_input = input()
        if user_input == "":
            inv.shutdown()
            break

if __name__ == "__main__":
    parser = a.ArgumentParser(description='Rumble ViewerBOT.')
    parser.add_argument('-v', '--video_id', type=str, help='the video you want to viewbot. How to get video id? => https://raw.githubusercontent.com/Ryukudz/Rumble-Viewer-Bot/main/tab.png')
    parser.add_argument('-b', '--bot_count', type=int, help='the number of bots to send, recommended range is between 100 and 500.')

    args = parser.parse_args()

    if args.video_id and args.bot_count:
        video_id = args.video_id
        bot_count = args.bot_count
        ViewCount(video_id, bot_count)

    else:
        video_id = str(input(Fore.GREEN + "[~] " + Fore.WHITE + "Enter video id 📺: "))
        bot_count = int(input(Fore.GREEN + "[~] " + Fore.WHITE + "How many viewers do you want to send 🤖: "))
        ViewCount(video_id, bot_count)

# ==========================================
# Copyright 2023 Ryukudz
# You expressly understand and agree that Subfinder (creators and contributors) shall not be liable for any damages or losses
# resulting from your use of this tool or third-party products that use it.
# Creators aren't in charge of any and have/has no responsibility for any kind of:
# Unlawful or illegal use of the tool.
# Legal or Law infringement (acted in any country, state, municipality, place) by third parties and users.
# Act against ethical and / or human moral, ethic, and peoples and cultures of the world.
# Malicious act, capable of causing damage to third parties, promoted or distributed by third parties or the user through this tool.
# ==========================================