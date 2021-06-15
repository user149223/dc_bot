import discord, datetime, random, string, time, json, difflib, os, smtplib, threading, asyncio, socket, requests
import platform
from lxml import html
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import pw as pwer

class MyClient(discord.Client):
    #start

    def __init__(self):
        super().__init__() 
        try: self.data_load()
        except:
            with open("DISCORD_USERS.json","w") as file:
                file.write("[]")
                file.close()            
            with open("USERS.json","w") as file:
                file.write("[]")
                file.close()            
            with open("ADS.json","w") as file:
                file.write("[]")
                file.close()            
            with open("BOT-INFO.json","w") as file:
                file.write("[]")
                file.close()            
            with open("FILE_NOT_FOUND.json","w") as file:
                file.write('["file not found",":/"]')
                file.close()
            with open("WAITING.json","w") as file:
                file.write('[]')
                file.close()            
            with open("POSTS.json","w") as file:
                file.write('[]')
                file.close()
            with open("countrys.txt","w") as file:
                file.write('''
                Fiji
                Finland
                France
                Gabon
                The Gambia
                Georgia
                Germany
                Ghana
                Greece
                Grenada
                Guatemala
                Guinea
                Guinea-Bissau
                Guyana
                Haiti
                Honduras
                Hungary
                Iceland
                India
                Indonesia
                Iran
                Iraq
                Ireland
                Israel
                Italy
                Jamaica
                Japan
                Jordan
                Kazakhstan
                Kenya
                Kiribati
                North Korea
                South Korea
                Kosovo
                Kuwait
                Kyrgyzstan
                Laos
                Latvia
                Lebanon
                Lesotho
                Liberia
                Libya
                Liechtenstein
                Lithuania
                Luxembourg
                Macedonia
                Madagascar
                Malawi
                Malaysia
                Maldives
                Mali
                Malta
                Marshall Islands
                Mauritania
                Mauritius
                Mexico
                Micronesia
                Moldova
                Monaco
                Mongolia
                Montenegro
                Morocco
                Mozambique
                Myanmar
                Namibia
                Nauru
                Nepal
                Netherlands
                New Zealand
                Nicaragua
                Niger
                Nigeria
                Norway
                Oman
                Pakistan
                Palau
                Panama
                Papua New Guinea
                Paraguay
                Peru
                Philippines
                Poland
                Portugal
                Qatar
                Romania
                Russia
                Rwanda
                Saint Kitts and Nevis
                Saint Lucia
                Saint Vincent and the Grenadines
                Samoa
                San Marino
                Sao Tome and Principe
                Saudi Arabia
                Senegal
                Serbia
                Seychelles
                Sierra Leone
                Singapore
                Slovakia
                Slovenia
                Solomon Islands
                Somalia
                South Africa
                South Sudan
                Spain
                Sri Lanka
                Sudan
                Suriname
                Swaziland
                Sweden
                Switzerland
                Syria
                Taiwan
                Tajikistan
                Tanzania
                Thailand
                Togo
                Tonga
                Trinidad and Tobago
                Tunisia
                Turkey
                Turkmenistan
                Tuvalu
                Uganda
                Ukraine
                United Arab Emirates
                United Kingdom
                USA
                Uruguay
                Uzbekistan
                Vanuatu
                Vatican City
                Venezuela
                Vietnam
                Yemen
                Zambia
                Zimbabwe
                ''')
                file.close()
            self.data_load()
        self.website_name = "http://127.0.0.1:5000"
        self.role_sequence = [  
            'banned','user', 'premium', 'verified', 'tester', 
            'T-team', 'Supporter', 'X-team', 'manager', 'moderator', 'owner'
        ]
        self.bot_closed = False

    def permission_checker(self, nachricht):
        try:
            if "owner" in self.benutzer["role"]:
                return True
        except: 
            pass
        if self.discord_user["authorization"][nachricht] == True:
            return True
        return False

    def data_load(self):
        with open("USERS.json","r") as file:
            self._users = json.loads(file.read())
            file.close()

        with open("WAITING.json","r") as file:
            self.waiting_list = json.loads(file.read())
            file.close()

        with open("POSTS.json","r") as file:
            self.posts = json.loads(file.read())
            file.close()

        with open("BOT-INFO.json","r") as file:
            self.test = json.loads(file.read())
            file.close()

            self.post_id = self.test[0]
            self.user_id = self.test[1]
            self.comment_id = self.test[2]

        with open("DISCORD_USERS.json","r") as file:
            self._discord_users = json.loads(file.read())
            file.close()   

        with open("ADS.json","r") as file:
            self.ads = json.loads(file.read())
            file.close()

    async def send_to_mod(self, nachricht, kanal_id, extra):
        if nachricht["reason"] == "new_post":
            em = discord.Embed(
                title=nachricht["content"], 
                description = str(
                    "**Name:\n**" + str(nachricht["extra"][1]) + "\n**id:\n**" + str(nachricht["extra"][3]) + "\n**Content:**\n"
                    + str(nachricht["extra"][2]) + "\n**User:**\n" + str(nachricht["extra"][0]["id"])
                )
            )
            mes = await client.get_channel(int(kanal_id)).send(embed = em)

        elif nachricht["reason"] == "report_comment":
            em = discord.Embed(
                title=nachricht["content"], 
                description = str(
                    "**Likes:\n**" + str(nachricht["extra"][1]) + "\n**id:\n**" + str(nachricht["extra"][3]) + "\n**Content:**\n"
                    + str(nachricht["extra"][2]) + "\n**User:**\n" + str(nachricht["extra"][0]["id"])
                )
            )
        mes = await client.get_channel(int(kanal_id)).send(embed = em)

    def ago(self, num):
        keep_going = True
        test = 0
        if num < 60:
            if num == 1:
                result_log = ("4 minutes and " + str(60 - int(num)) + " second")
            else:
                result_log = ("4 minutes and " + str(60 - int(num)) + " seconds")
        else:
            while keep_going:
                test += 1
                if num / test < 60:
                    secs = (num - ((test - 1) * 60))
                    test -= 1
                    if test < 1:
                        if secs == 1:
                            (str(5 - int(test)) + " minute and " + str(60 - int(secs)) + " second")
                        else:
                            (str(5 - int(test)) + " minutes and " + str(60 - int(secs)) + " seconds")
                    else:
                        if secs == 1:
                            result_log = (str(5 - int(test)) + " minutes and " + str(60 - int(secs)) + " second")
                        else:
                            result_log = (str(5 - int(test)) + " minutes and " + str(60 - int(secs)) + " seconds")
                    keep_going = False
        return result_log

    async def get_user_by_id(self,userid):
        for value in self._users:
            for value2 in value["account-users"]:
                if str(value2) == str(userid):
                    return value

    async def get_discord_user(self, discord_user_id):  
        user_gefunden = False
        for value in self._discord_users:
            if str(value["id"]) == str(discord_user_id):
                user_gefunden = True
                return value
        if user_gefunden == False:
            new_discord_user = {
                "id":str(discord_user_id),
                "authorization":{
                    "upload":True,
                    "eval":False,
                    "register":True,
                    "feedback":True,
                    "edit_field":False,
                    "login":True,
                    "logout":True,
                    "send_data_files":False,
                    "search":True,
                    "report":True,
                    "notif":True,
                    "start":True,
                    "ban":False, 
                    "weather":False,
                    "add_ad":False,
                    "change_info":True,
                    "update-data":False,
                    "safe-data":False,
                    "change-domain":False,
                    "dict-append":False,
                    "unban":False,
                    "perm-manager":False
                },
                "trusted-guild":[],
                "log-acc":[]
            }
            self._discord_users.append(new_discord_user)
            return new_discord_user

    # errors

    async def forbidden_error(self, message):
        await message.channel.send(embed = discord.Embed(
            title = "403 ForbiddenError",
            description = "Sorry, but this site is fobidden for you. ",
            color = 15158332
        ))

    async def notfound_error(self, message):
        await message.channel.send(embed = discord.Embed(
            title = "404 NotFoundError",
            description = "This site wasn't found.",
            color = 15158332
        ))

    async def notactivatet_error(self, message):
        await message.channel.send(embed = discord.Embed(
            title = "20 NotActivatetError",
            description = "Your profile is not activatet, \n" +
            "you can activate your profil with **" + self.prefix + 
            "verify [verify code]** or on the website " + self.website_name +
            "/verify-code.",
            color = 15158332
        ))

    async def noaccount_error(self, message):
        await message.channel.send(embed = discord.Embed(
            title = "3200 NoAccountError",
            description = "You don't have an account, please login or register first.",
            color = 15158332
        ))        

    #message-functions

    async def my_stats(self, message):
        try: post_id = message.content.split(" ")[2]
        except: post_id = ""
        copied_acc = self.benutzer
        views_count = 0
        likes_count = 0
        reputation_count = 0
        found = False
        for value in self.posts:
            if value["user id"] == copied_acc["id"]:
                if post_id != "":
                    if post_id == str(value["post id"]):
                        views_count = int(value["views"])
                        likes_count = int(len(value["likes"]))
                        reputation_count = int(value["reputation"])
                        found = True
                else:
                    views_count += int(value["views"])
                    likes_count += int(len(value["likes"]))
        if post_id != "" and found == False:
            await message.channel.send("**:x:Post with the ID " + str(post_id) + " wasn't found.**")
        else:
            if post_id != "": 
                if reputation_count < 0: reputation_string = "**Reputation:** :black_square: very low"
                elif reputation_count < 1000 and reputation_count > 0: reputation_string = "**Reputation:** :red_square: low"
                elif reputation_count > 999 and reputation_count < 2500: reputation_string = "**Reputation:** :orange_square: normal"
                elif reputation_count > 2499 and reputation_count < 4000: reputation_string = "**Reputation:** :yellow_square: high"
                elif reputation_count > 3999 and reputation_count < 7000: reputation_string = "**Reputation:** :green_square: very high"
                elif reputation_count > 6999 and reputation_count < 10000: reputation_string = "**Reputation:** :blue_square: super high"
                elif reputation_count > 9999: reputation_string = "**Reputation:** :purple_square: very very high"
            else: reputation_string = ""
            await message.channel.send(embed = discord.Embed(
                title = ":bar_chart: YOUR STATS", #-⠀​⠀​⠀​⠀​⠀​⠀​-
                description = (
                    "**total likes:** " + str(likes_count) + 
                    "⠀​⠀​⠀​⠀​⠀​⠀​⠀​⠀​⠀​⠀​⠀​⠀​**total views:** " + 
                    str(views_count) + "\n" + reputation_string
                ),
                color = 0
            ))

    async def net_stats(self, message):
        max_created = 99999.9 * 99999.9
        for value in self.posts:
            if time.time() - float(value["datetime"]) < float(max_created):
                max_created = time.time() - float(value["datetime"])
        if float(max_created) > 86400.0: max_created = str(max_created / 60 / 60 / 24).split(".")[0] + " days"
        elif float(max_created) > 3600.0: max_created = str(max_created / 60 / 60).split(".")[0] + " hours"
        elif float(max_created) > 60.0: max_created = str(max_created / 60).split(".")[0] + " minutes"
        else: max_created = str(max_created).split(".")[0] + " seconds"
        await message.channel.send(embed = discord.Embed(
            title = ":bar_chart: BOT STATS",
            description = (
                "**:levitate: Registered accounts: " + str(len(self._users)) +
                "\n:speech_balloon: Uploaded posts: " + str(len(self.posts)) +
                "\n:computer: Commands count: 55" +
                "\n:timer: Last post uploaded: " + str(max_created) + " ago"
                "**"
            ),
            color = 0
        ))

    async def delete_account(self, message):
        copied_user = self.benutzer
        if str(self.benutzer["discord id"]) == str(message.author.id):
            if message.content.split(" ")[1] == pwer.encode(copied_user["password"]):
                mes = await message.channel.send("**Deleting your account...**")
                copied_user["role"] += "*deleted"
                copied_user["account-users"].remove(str(message.author.id))
                for value in self.posts:
                    if value["user id"] == str(copied_user["id"]):
                        value["reputation"] = -999999999
                try: self.discord_user["log-acc"].remove(str(copied_user["id"]))
                except: pass
                await mes.edit(content="**Succesfull deleted your account:white_check_mark:**")
            else: await message.channel.send(":x:**Wrong password, use your command " + self.prefix + "delete-account [password]**")
        else: await message.channel.send(":x:**You can only delete your account if you are logged in with the"+
        " discord account where you created your account.**")

    async def set_command(self, message):
        copied_user = self.benutzer
        try:
            post_id = message.content.split(" ")[1]
            if [i for i in self.posts if i["post id"]==post_id]:
                if [i for i in self.posts if i["post id"]==post_id][0]["user id"]==copied_user["id"]:
                    field = message.content.split(" ")[2]
                    if field == "status":
                        if message.content.split(" ")[3] != "deleted" or \
                            message.content.split(" ")[3] != "privat" or \
                            message.content.split(" ")[3] != "normal":
                            if field == "deleted":
                                self.posts.remove([i for i in self.posts if i["post id"]==post_id][0])
                            else: [i for i in self.posts if i["post id"]==post_id][0]["status"] = message.content.split(" ")[3]
                            await message.channel.send("**" + field + " was set to " + message.content.split(" ")[3] + "**:white_check_mark:")
                        else: await message.channel.send(":x:**[new field content] can contain just deleted or privat.**")
                    else: await message.channel.send(":x:**Field wasn't found.**")
                else: await message.channel.send(":x:**Not your post.**")
            else: await message.channel.send(":x:**Post wasn't found.**")
        except:
            await message.channel.send(embed = discord.Embed(
                title = ":x: Error",
                description = "**Command usage:**\n" + self.prefix + "set [post id] [field] [new field content]",
                color = 15158332
            ))

    async def my_posts(self, message):
        copied_user = self.benutzer
        your_posts = ""
        for value in self.posts:
            if value["user id"] == copied_user["id"]:
                if len(your_posts) < 1980:
                    your_posts += "**• ID " + value["post id"] + " | " + value["name"] + "**\n"
        await message.channel.send(embed = discord.Embed(
            title = copied_user["name"] + "'s posts",
            description = your_posts,
            color = 0
        ).set_footer(text="Delete or edit your posts with the " + self.prefix + "set command, check the usage with " + self.prefix + "help set"))

    async def messages_from_mod(self, message):
        wem = message.content.replace(self.prefix + "send-message","").split(" ")[1]
        nachricht = message.content.replace(self.prefix + "send-message " + wem,"")
        if wem == "everyone":
            for value in self._users:
                value["notif"].append({
                    "message":"New message from GlobalTube, please check your DM's.",
                    "readen":False,
                    "about":[str(datetime.datetime.now())]
                })
                for value1 in value["account-users"]:
                    try:
                        await (await client.fetch_user(int(value1))).send(embed=discord.Embed(
                            title = ":warning:NEW MESSAGE FROM GLOBALTUBE TEAM",
                            description = "**to: everyone**\n" + nachricht,
                            color = 0
                        ))
                    except: pass

            await message.channel.send(":white_check_mark:**Succefully sent message to everyone.**")
        elif wem.startswith("<role:"):
            gefunden = False
            welche_rolle = wem.split("<role:")[1].split(">")[0]
            for value in self._users:
                if welche_rolle in value["role"]:
                    value["notif"].append({
                        "message":"New message from GlobalTube for your role, please check your DM's.",
                        "readen":False,
                        "about":[str(datetime.datetime.now())]
                    })
                    gefunden = True
                    for value1 in value["account-users"]:
                        try:
                            await (await client.fetch_user(int(value1))).send(embed=discord.Embed(
                                title = ":warning:NEW MESSAGE FROM GLOBALTUBE TEAM",
                                description = "**to: <role:" + welche_rolle + ">**\n" + nachricht,
                                color = 0
                            ))
                        except: pass
            if gefunden == True:
                await message.channel.send(":white_check_mark:**Succefully sent message to everyone with the role " + welche_rolle +  ".**")
            else: await message.channel.send(":x:**Role wasn't found.**")
        elif wem.startswith("<user:"):
            wer = wem.split("<user:")[1].split(">")[0]
            gefunden = False
            for value in self._users:
                if wer == value["name"]:
                    value["notif"].append({
                        "message":"New message from GlobalTube for you, please check your DM's.",
                        "readen":False,
                        "about":[str(datetime.datetime.now())]
                    })
                    gefunden = True
                    for value1 in value["account-users"]:
                        try:
                            await (await client.fetch_user(int(value1))).send(embed=discord.Embed(
                                title = ":warning:NEW MESSAGE FROM GLOBALTUBE TEAM",
                                description = "**to: <user:" + wer + ">**\n" + nachricht,
                                color = 0
                            ))
                        except: pass
            if gefunden == True:
                await message.channel.send(":white_check_mark:**Succefully sent message to " + wer +  ".**")
            else: await message.channel.send(":x:**User wasn't found.**")
        else:
            await message.channel.send(":x:**You can just write messages to <user:[username]>, <role:[role-name]> or everyone.**")

    async def help_messager(self, message):
        help_messages = [
            {"command":"register","example":"(*prefix*)register 'max_mustermann139' 'coolmail@gmail.com'"
            " 'x§dadso13' 'x§dadso13' '12/1995' 'germany'","description":
            "You can create your account with that command.","cmd_usage":
            "(*prefix*)register 'username' 'email' 'password' 'password again' 'birthday (MM/YYYY)' 'country'"},
            {"command":"upload","example":"(*prefix*)upload name='Hello, that's my post' post='Please subscribe to me'",
            "description":"You can upload posts with that command","cmd_usage":
            "(*prefix*)upload name='post name' post='post content'"},
            {"command":"set","example":"(*prefix*)set 51 status privat","cmd_usage":"(*prefix*)set [post id] [field] [new field content]",
            "description":"You can manage your posts.\n[field] -> status\n[new field content] -> deleted/privat/normal"}
        ]
        if message.content.replace(self.prefix + "help","").replace(" ","") != "":
            help_mes = [i for i in help_messages if i["command"]==message.content.replace(self.prefix + "help","").replace(" ","")]
            if help_mes:
                help_mes = help_mes[0]
                await message.channel.send(embed = discord.Embed(
                    title = ":information_source: Help",
                    description = (
                        "Command:\n```" + self.prefix + help_mes["command"] + "```" + "\nDescription:\n" +
                        "```" + help_mes["description"] + "```\nCommand usage:\n```" + help_mes["cmd_usage"].replace("(*prefix*)",self.prefix) + 
                        "```\nCommand example:\n```" + help_mes["example"].replace("(*prefix*)",self.prefix) + "```"   
                    ),
                    color = 0
                ))
            else: await message.channel.send("**Command not found.**")
        else:
            await message.channel.send(embed = discord.Embed(
                title = ":information_source: Central Help",
                description = "Hey, \n if you are new you can register to GlobalTube" 
                + " with the command \n ```" + self.prefix + "register```\nif you don't " +
                "know the usage, you can check it with **" + self.prefix + "help register.**" +
                "\nIf you want to upload posts, you can do it with the command \n```" + self.prefix +
                "upload```\n you can check the usage with **" + self.prefix + "help upload**.\n" +
                "If you want to see a user account, you can make it with the command \n```" + self.prefix +
                "user [username]``` \nOr if you want to see a post, you can use the command ```" + self.prefix +
                "post [post id]```.\nOr you can see your profile/posts/stats - ```" + self.prefix + "my profile/posts/stats```." +
                "\nYou can edit your settings with the command ```" + self.prefix + "settings```.",
                color = 0
            ))

    async def pay(self, message):
        copied_user = self.benutzer
        try:
            user = [i for i in self._users if message.content.split(" ")[1]==i["name"]][0]
            money = int(message.content.split(" ")[2])
            if money < int(copied_user["money"]):
                if money > 100:
                    copied_user["money"] = int(copied_user["money"]) - money
                    user["money"] = int(user["money"]) + money
                    user["f_notif"].append({
                        "message":copied_user["name"] + " paid " + str(money) + "⍫ to you",
                        "readen":False,
                        "about":[str(datetime.datetime.now())]
                    })
                    await message.channel.send("**Paid " + str(money) + "⍫ to " + user["name"] + ":moneybag:**")
                else: await message.channel.send(":x:**Please pay at least 100.00⍫**")
            else: await message.channel.send(":x:**You don't have that money.**")
        except: await message.channel.send(":x:**Command usage: " + self.prefix + "pay user money**")

    async def shop(self, message):
        await message.channel.send(embed = discord.Embed(
            title = "SHOP ITEMS:shopping_cart:",
            description = "**Buy items with " + self.prefix + "buy-item [item number]\n" +
            "**\nItem name: ```red-user-color``` price: ```25000.00⍫``` Item Number: ```1```\nmore soon..."
        ))

    async def buy_shop_item(self, message):
        copied_user = self.benutzer
        items = [{"name":"red-user-color","price":25000,"number":"1"}]
        item = [i for i in items if message.content.split(" ")[1]==i["number"]]
        if item:
            item = item[0]
            if item["price"]<int(copied_user["money"]):
                copied_user["money"] = int(copied_user["money"]) - item["price"]
                if item["number"] == "1":
                    copied_user["premium-color"] = 15158332
                    await message.channel.send("**Succesfully bought item:white_check_mark:**")
            else: await message.channel.send(":x:**Not enough money, you need" + str(item["price"] - int(copied_user["money"]))+ "⍫more.**")
        else: await message.channel.send(":x:**The item wasn't found.**")

    async def tree(self, message):
        all_dict = {
            "users":self._users,
            "posts":self.posts,
            "waiting_list":self.waiting_list,
            "discord_users":self._discord_users,
            "ads":self.ads
        }
        em = ""
        message.content = message.content.replace(self.prefix + "tree ","")
        path = "DT:%"
        if len(message.content.replace("DT:%","").split("%")) + 1 > 1:
            count = 0
            notes = ""
            for value1 in message.content.replace("DT:%","").split("%"):
                try:
                    path += value1.replace("%","") + "%"
                    if "#add#" in value1:
                        if str(value1).split("#add#")[1].startswith("<") and "::" in \
                            str(value1).split("#add#")[1] and ">" in str(value1).split("#add#")[1]:
                            if str(value1).split("#add#")[1].startswith("<list::"):
                                if str(value1).split("#add#")[1].split(">")[0].split("::")[1].startswith("["):
                                    elem_now[str(value1).split("#add#")[0]].append(eval(str(value1).split("#add#")[1].split(">")[0].split("::")[1]))
                                elif str(value1).split("#add#")[1].split(">")[0].split("::")[1].startswith("{"):
                                    elem_now[str(value1).split("#add#")[0]].append(eval(str(value1).split("#add#")[1].split(">")[0].split("::")[1]))
                                else:
                                    try:
                                        elem_now[str(value1).split("#add#")[0]].append(str(int(value1).split("#add#")[1].split(">")[0].split("::")[1]))
                                    except:
                                        elem_now[str(value1).split("#add#")[0]].append(str(value1).split("#add#")[1].split(">")[0].split("::")[1])
                            elif str(value1).split("#add#")[1].startswith("<str::"):
                                elem_now[str(value1).split("#add#")[0]] += str(value1).split("#add#")[1].split(">")[0].split("::")[1]
                            elif str(value1).split("#add#")[1].startswith("<int::"):
                                elem_now[str(value1).split("#add#")[0]] = int(elem_now[str(value1).split("#add#")[0]]) \
                                + int(str(value1).split("#add#")[1].split(">")[0].split("::")[1])
                        value1 = value1.split("#add#")[0]
                    if "#replace-to#" in value1:
                        elem_now[str(value1).split("#replace-to#")[0]] = str(value1).split("#replace-to#")[1]
                        value1 = value1.split("#replace-to#")[0]
                        notes = elem_now[str(value1).split("#add#")[0]] + " replaced into " + str(value1).split("#add#")[1]
                    if "#filter-by#" in value1:
                        elem_now = [i for i in elem_now if i[str(value1).split("#filter-by#")[0]]==str(value1).split("#filter-by#")[1]][0]
                    if "#remove#" in value1:
                        del elem_now[str(value1).split("#remove#")[0]][eval(str(value1).split("#remove#")[1])]
                    else:
                        notes = ""
                        if count == 0:
                            elem_now = all_dict[value1.replace(" ","")]
                        else: 
                            try: elem_now = (elem_now[int(value1)])
                            except ValueError: 
                                elem_now = (elem_now[str(value1)])
                except: pass
                count += 1
            if str(type(elem_now)).split("'")[1] == "dict":
                for key, value in elem_now.items():
                    key_value = str(value)
                    if len(str(value)) > 1900 / len(all_dict.keys()):
                        key_value = "[Too large " + str(type(value)).split("'")[1] + "]"
                    em += "**" + str(key) + "** -> " + str(key_value).replace("', '","',\n'").replace("[{","[{\n").replace("}]","\n}]") + "\n"
            elif str(type(elem_now)).split("'")[1] == "list":
                em += "\nList Items:\n"
                for value in elem_now:
                    key_value = value
                    elem_index = str(elem_now.index(key_value))
                    if len(str(value)) > 1900 / len(elem_now):
                        key_value = "[Too large " + str(type(value)).split("'")[1] + "]"
                    em += "**Index " + elem_index + " -> " + str(key_value) + "**\n"
            else:
                value = str(elem_now)
                if len(str(value)) > 1900:
                    value = "[Too large " + str(type(value)).split("'")[1] + "]"
                em += str(value)
        else:
            for key, value in all_dict.items():
                key_value = value.replace("', '","',\n'")
                if len(str(value)) > 1900 / len(all_dict.keys()):
                    key_value = "[Too large " + str(type(value)).split("'")[1] + "]"
                em += "**" + str(key) + "** -> " + str(key_value) + "\n"
        await message.channel.send(embed=discord.Embed(
            title="DATA TREE",
            description="```" + path + "```\n\n" + notes + "\n" + em,
            color = 10181046
        ))

    async def send_data_files(self, message):
        message.content = message.content.replace(" ","").replace(self.prefix + "send-data-files","")
        if message.content.lower().startswith("p"): dateiname = "POSTS"
        elif message.content.lower().startswith("d"): dateiname = "DISCORD_USERS"
        elif message.content.lower().startswith("u"): dateiname = "USERS"
        elif message.content.lower().startswith("w"): dateiname = "WAITING"
        elif message.content.lower().startswith("a"): dateiname = "ADS"
        else: dateiname = "FILE_NOT_FOUND"
        await message.channel.send("**Sending the file into your dm's... Please check your dm's.**")
        await message.author.send(file=discord.File(str(dateiname) + '.json'))

    async def comment_anzeiger(self, reaction, user):
        copied_acc = self.benutzer
        for value in self.waiting_list:
            if str(value["reason"]) == "post_add":
                if str(reaction.message.id) == str(value["extra"][1]):
                    if str(user.id) == str(value["extra"][0]):
                        gewollter_post = [i for i in self.posts if value["extra"][2] == i["post id"]]
                        value2 = gewollter_post[0]["comments"][random.randint(0,len(gewollter_post[0]["comments"]) - 1)]
                        haken = ""
                        if "verified" in [i for i in self._users if value2["author"]==i["name"]][0]["role"]:
                            haken = "✓"
                        res_mes = ":arrow_forward: **" + value2["author"] + haken + " | " + str(len(value2["likes"])) + ":star: | " + str(self.ago2(value2["datetime"])) + " | ID " + str(value2["id"]) + "**\n" + value2["comment"] + "\n"
                        fake_post = gewollter_post
                        gewollter_post[0]["reputation"] += 4
                        ids_von_comments = [value2["id"]]
                        for value in fake_post[0]["comments"]:
                            value["likes_count"] = len(value["likes"])
                        fake_post[0]["comments"].sort(key=lambda d: int(d["likes_count"]), reverse=True)
                        for value1 in fake_post[0]["comments"]:
                            if value1 != value2:
                                if len(res_mes) < 1900:
                                    ids_von_comments.append(value1["id"])
                                    haken = ""
                                    if "verified" in [i for i in self._users if value1["author"]==i["name"]][0]["role"]:
                                        haken = "✓"
                                    res_mes += "**" + value1["author"] + haken + " | " + str((value1["likes_count"])) + ":star: | " + str(self.ago2(value1["datetime"])) + " | ID " + str(value1["id"]) + "**\n" + value1["comment"] + "\n"
                        mes=await reaction.message.channel.send(embed = discord.Embed(
                            title = "COMMENTS",
                            description = res_mes
                        ))
                        self.waiting_list.append({
                            "reason":"comments",
                            "completed":"false", 
                            "extra":[mes.id, user.id, copied_acc["name"], fake_post[0]["post id"], value2, 0, ids_von_comments]
                        })
                        await mes.add_reaction("⬆️")
                        await mes.add_reaction("⬇️")
                        await mes.add_reaction("🅰️")
                        await mes.add_reaction("⭐")
                        await mes.add_reaction("❗")
                        if gewollter_post[0]["user id"] == copied_acc["id"]:
                            await mes.add_reaction("🗑️")

    async def comment_eventer(self, reaction, user):
        try:
            copied_user = self.benutzer
            for value in self.waiting_list:
                if value["reason"] == "comments":
                    if value["extra"][0] == reaction.message.id:
                        if value["extra"][1] == user.id:
                            if reaction.emoji == "⬆️" or reaction.emoji == "⬇️":
                                fake_post = [i for i in self.posts if i["post id"] == value["extra"][3]]
                                for value5 in fake_post[0]["comments"]:
                                    value5["likes_count"] = len(value5["likes"])
                                if reaction.emoji == "⬇️": 
                                    if value["extra"][5] < len(fake_post[0]["comments"]):
                                        value["extra"][5] += 1
                                if reaction.emoji == "⬆️":
                                    if value["extra"][5] > -1:
                                        value["extra"][5] -= 1
                                await reaction.message.remove_reaction(reaction.emoji, user)
                                test = ""
                                res_mes = ""
                                if value["extra"][5] == 0: test = ":arrow_forward:"
                                new_comments = []
                                for counter in range(len(value["extra"][6])):
                                    try: new_comments.append([i for i in fake_post[0]["comments"] if value["extra"][6][counter]==i["id"]][0])
                                    except: pass
                                counter = 0
                                for value1 in new_comments:
                                    counter += 1
                                    test = ""
                                    if counter == value["extra"][5]:
                                        test = ":arrow_forward: "
                                    if len(res_mes) < 1900:
                                        haken = ""
                                        if "verified" in [i for i in self._users if value1["author"]==i["name"]][0]["role"]:
                                            haken = "✓"
                                        res_mes += test + "**" + value1["author"] + haken + " | " + str((value1["likes_count"])) + ":star: | " + str(self.ago2(value1["datetime"])) + " | ID " + str(value1["id"]) + "**\n" + value1["comment"] + "\n"
                                await reaction.message.edit(embed=discord.Embed(
                                        title="COMMENTS",
                                        description=res_mes
                                    ))

                            elif reaction.emoji == "🅰️":
                                fake_post = [i for i in self.posts if i["post id"] == value["extra"][3]]
                                for value5 in fake_post[0]["comments"]:
                                    value5["likes_count"] = len(value5["likes"])
                                await reaction.message.remove_reaction(reaction.emoji, user)
                                new_comments = []
                                for counter in range(len(value["extra"][6])):
                                    try: new_comments.append([i for i in fake_post[0]["comments"] if value["extra"][6][counter]==i["id"]][0])
                                    except: pass
                                counter = 1
                                res_mes = ""
                                for value1 in new_comments:
                                    test = ""
                                    test2 = ""
                                    if counter == value["extra"][5]:
                                        if value1["answers"] != []: test = "↳⠀​"
                                        test2 = ":arrow_forward:"
                                        for value13 in value1["answers"]:
                                            haken = ""
                                            if "verified" in [i for i in self._users if value13["author"]==i["name"]][0]["role"]:
                                                haken = "✓"
                                            test += "⠀​⠀​**" + value13["author"] + haken + " | " + str(self.ago2(value13["datetime"])) + " | ID " + str(value13["id"]) + "**\n⠀​⠀​⠀​⠀​" + value13["comment"] + "\n"
                                    counter += 1
                                    if len(res_mes) < 1900:
                                        haken = ""
                                        if "verified" in [i for i in self._users if value1["author"]==i["name"]][0]["role"]:
                                            haken = "✓"
                                        res_mes += test2 + "**" + value1["author"] + haken + " | " + str((value1["likes_count"])) + ":star: | " + str(self.ago2(value1["datetime"])) + " | ID " + str(value1["id"]) + "**\n" + value1["comment"] + "\n" + test
                                
                                await reaction.message.edit(embed=discord.Embed(
                                    title="COMMENTS",
                                    description=res_mes
                                ))

                            elif reaction.emoji == "⭐":
                                await reaction.message.remove_reaction(reaction.emoji, user)
                                fake_post = [i for i in self.posts if i["post id"] == value["extra"][3]][0]
                                kommentar = [i for i in fake_post["comments"] if i["id"]==value["extra"][6][value["extra"][5]]][0]
                                if [i for i in kommentar["likes"] if i==copied_user["name"]]: 
                                    kommentar["likes"].remove(copied_user["name"])
                                    test = " removed his like from "
                                else: 
                                    kommentar["likes"].append(copied_user["name"])
                                    test = " liked "
                                mes=await reaction.message.channel.send("**" + str(user) + test + " the comment with the ID " + str(kommentar["id"]) + "**")
                                await asyncio.sleep(3)
                                await mes.delete()
                            
                            elif reaction.emoji == "❗":
                                if self.permission_checker("report"):
                                    fake_post = [i for i in self.posts if i["post id"] == value["extra"][3]][0]
                                    kommentar = [i for i in fake_post["comments"] if i["id"]==value["extra"][6][value["extra"][5]]][0]
                                    await self.send_to_mod(
                                        {
                                            "reason":"report_comment",
                                            "content":"A comment was reported! :warning:",
                                            "extra":[copied_user,len(kommentar["likes"]),kommentar["comment"],kommentar["id"]]
                                        },
                                        int(817906575128789003),
                                        []
                                    )
                                    await reaction.message.channel.send("**Reported comment :white_check_mark:**")
                                else: await self.forbidden_error(reaction.message)

                            elif reaction.emoji == "🗑️":
                                fake_post = [i for i in self.posts if i["post id"] == value["extra"][3]][0]
                                kommentar = [i for i in fake_post["comments"] if i["id"]==value["extra"][6][value["extra"][5]]][0]
                                if kommentar["author"] == copied_user["name"] or copied_user["name"] ==\
                                    [i for i in self._users if fake_post["user id"]==i["id"]][0]["name"]:
                                    fake_post["comments"].remove(kommentar)
                                    mes=await reaction.message.channel.send("**Deleting comment...**")
                                    await asyncio.sleep(random.randint(0,2))
                                    await mes.edit(content="**succesfully deleted comment :white_check_mark:**")
                                    await asyncio.sleep(2)
                                    await mes.delete()
        except: await reaction.message.channel.send("**Something went wrong :/**")

    async def add_comment(self, message):
        try:
            post_id = message.content.split("'")[1]
            try: kommentar = message.content.split("'")[3]
            except: kommentar = message.content.split("'")[2]
            kom_post = [i for i in self.posts if i["post id"]==post_id]
            if len(kommentar) < 200:
                kommentar = kommentar.replace("*","").replace("```","").replace("_","*_*").replace("~~","").replace("\n","")
                if kommentar.startswith("answer:"):
                    answered_comment = [i for i in kom_post[0]["comments"] if str(i["id"])==kommentar.split(":")[1]]
                    if answered_comment:
                        answered_comment[0]["answers"].append({
                            "comment":kommentar.split(":")[2],
                            "datetime":str(datetime.datetime.now()),
                            "author":self.benutzer["name"],
                            "id":self.comment_id
                            })
                        self.comment_id += 1
                        gewollter_user = [i for i in self._users if str(i["id"])==str(kom_post[0]["user id"])]
                        gewollter_user[0]["f_notif"].append({
                            "message":self.benutzer["name"] + " answered to your comment: " + kommentar.split(":")[2] + " on the post " + kom_post[0]["name"] + " (*#-prefix-#*link/post/" + kom_post[0]["post id"] + ")",
                            "readen":False,
                            "about":[str(datetime.datetime.now())]
                        })
                    else: await message.channel.send(":x:**Comment with that id weren't found.**")
                else:
                    kom_post[0]["comments"].append({
                        "comment":kommentar,
                        "datetime":str(datetime.datetime.now()),
                        "likes":[],
                        "author":self.benutzer["name"],
                        "answers":[],
                        "id":self.comment_id
                    })  
                    gewollter_user = [i for i in self._users if str(i["id"])==str(kom_post[0]["user id"])]
                    gewollter_user[0]["f_notif"].append({
                        "message":self.benutzer["name"] + " commented your post " + kom_post[0]["name"] + "(" + kommentar + ") (*#-prefix-#*link/post/" + kom_post[0]["post id"] + ")",
                        "readen":False,
                        "about":[str(datetime.datetime.now())]
                    })                
                    self.comment_id += 1
                if "@" in kommentar:
                    g_u_i = kommentar.split("@")[1].split(" ")[0]
                    gewollter_user = [i for i in self._users if str(i["name"])==str(g_u_i)]
                    kom_post = kom_post[0]
                    gewollter_user[0]["f_notif"].append({
                        "message":self.benutzer["name"] + " mentioned you on the post " + kom_post[0]["name"] + " (*#-prefix-#*link/post/" + kom_post[0]["post id"] + ")",
                        "readen":False,
                        "about":[str(datetime.datetime.now())]
                    })
                await message.channel.send(":white_check_mark:**Added comment!**")
            else: await message.channel.send(":x:**Your comment is too large. (max. 200 characters)**")
        except: 
            await message.channel.send(
            ":x:**Use the command so: " + self.prefix + "comment post_id [comment]**"
        )

    async def set_account_color(self, message):
        if self.benutzer != None:
            if "premium" in self.benutzer["role"]:
                self.benutzer["premium-color"] = message.content.split(" ")[1]
                await message.channel.send("**Set your user color to " + message.content.split(" ")[1] + ".:white_check_mark:**")
                await message.channel.send("**Here are all the colors (Int values)\n" + 
                "https://gist.github.com/thomasbnt/b6f455e2c7d743b796917fa3c205f812**")
            else: await self.forbidden_error(message)
        else: await self.noaccount_error(message)

    async def history_manager(self, message):
        history_mes = ""
        copied_acc = self.benutzer
        copied_acc["history"].reverse()
        for value in list(copied_acc["history"]):
            for value1 in self.posts:
                if str(value1["post id"]) == str(value):
                    if len(str(history_mes)) < 150:
                        history_mes +=  "• ID " + str(value) + " | **" + value1["name"] + "**\n"
        history_mes = str(history_mes)
        await message.channel.send(embed = discord.Embed(
            title = ":scroll:YOUR HISTORY:scroll:",
            description = str(history_mes)
        ))

    async def edit_field(self, message):
        try:
            if message.content.split("'")[1].lower().startswith("u"):
                for value in range(len(self._users)):
                    if self._users[value]["id"] == message.content.split("'")[3]:
                        self._users[value][message.content.split("'")[5]] = message.content.split("'")[7]
            else:
                for value in range(len(self.posts)):
                    if self._users[value]["post id"] == message.content.split("'")[3]:
                        self.posts[value][message.content.split("'")[3]] = message.content.split("'")[5]
            await message.channel.send("**Succesfully edited field.**")
        except:
            await message.channel.send(embed = discord.Embed(
                title = ":x: ERROR",
                descripton = "Use the command so:\n**" + self.prefix 
                + "edit-field 'users/posts' 'user/post id' 'field-name' 'new_content'**"
            ))

    async def mod_help(self, message):
        await message.channel.send(embed = discord.Embed(
            title = ":information_source:MOD HELP",
            description = self.prefix + "tree DT:%..."
        ))

    class starter(discord.Client):
        #
        async def start(self, message, in_need_values, user, starter_mode):
            self.starter_mode = starter_mode    
            self.waiting_list = in_need_values[0]
            self._users = in_need_values[1]
            self.posts = in_need_values[2]
            self.user_id = in_need_values[3] 
            self.post_id = in_need_values[4]
            self.benutzer = in_need_values[5]
            self.prefix = in_need_values[6]
            self.website_name = in_need_values[7]
            self.discord_user = in_need_values[8]
            try:
                await self.analyze(message, user)
            except:
                await message.channel.send(
                    ":x:**We can't recommend you something because" + 
                    " we don't have any more posts to show**"
                )
            return self.waiting_list, self._users
        #
        async def analyze(self, message, user):
            copied_acc = self.benutzer
            self.test_posts = self.posts
            for value in self.test_posts:
                for value2 in self._users:
                    if value2["id"] == value["user id"]:
                        if value2["country"] != self.benutzer["country"] and self.benutzer["country"].lower() \
                            != "usa" and self.benutzer["country"].lower() != "britain":
                            for value3 in range(len(self.test_posts)):
                                if value3>0:
                                    value3 -= 1
                                if self.test_posts[value3] == value:
                                    del self.test_posts[value3]
            self.test_posts.sort(key=lambda d: int(d["reputation"]),reverse=True)
            result_id = 0
            for value in range(len(self.benutzer["history"])):
                if self.benutzer["history"][value] == self.test_posts[result_id]["post id"]:
                    result_id += 1
            for value in range(len(self.test_posts)):
                if self.test_posts[value]["status"] == "banned" or \
                self.test_posts[value]["status"] == "deleted" or \
                self.test_posts[value]["reputation"] == -999999999:
                    del self.test_posts[value]
                elif "banned" in [i for i in self._users if self.test_posts[value]["user id"] == i["id"]][0]["role"]:
                    del self.test_posts[value]
            result = self.test_posts[result_id]
            await self.sender(message, result, copied_acc, user)
        #
        async def sender(self, message, value4, copied_acc, user):
            clock = str(value4["created"]).split(" ")[0]
            for value7 in self._users:
                if value7["id"] == value4["user id"]:
                    user_name = value7
            em_content = str("**----------------\n**") + str(value4["content"]) + str("**\n----------------\n" + str(len(value4["likes"])) + "👍" + str(len(value4["dislikes"])) + "👎\n----------------\n**") + str(value4["views"]) + " views\n" + str(clock) + "**\n----------------\n" + user_name["name"] + "**\n" + str(len(user_name["subscribers"])) + " Subscribers\n**----------------**\n"
            em = discord.Embed(
                title=":bulb:RECOMMENDATION / :speech_balloon: post " + value4["post id"],
                description=value4["name"] + "\n" + str(em_content),
                color = 0
            )
            if self.starter_mode == "mes":
                mes=await message.channel.send(embed=em)
                await mes.add_reaction("⬇")
                await mes.add_reaction("👍")
                await mes.add_reaction("👎")
                await mes.add_reaction("🕴️")
                await mes.add_reaction("❗")
                await mes.add_reaction("💬")
                self.waiting_list.append({
                    "reason":"post_add",
                    "completed":"false",
                    "extra":[str(user.id),str(mes.id),str(value4["post id"]), "start"]
                })
            else: await message.edit(embed=em)
            value4["views"] = int(value4["views"]) + 1
            self.benutzer["history"].append(value4["post id"])
            value4["reputation"] = int(value4["reputation"]) - 2

    async def safe_data(self, message):
        eine_list = [self.post_id,self.user_id, self.comment_id]
        with open("USERS.json","w") as file:
            json.dump(self._users, file)
            file.close()   
            with open("WAITING.json","w") as file:
                json.dump(self.waiting_list, file)
                file.close()
                with open("POSTS.json","w") as file: 
                    json.dump(self.posts, file)
                    file.close()
                    with open("BOT-INFO.json","w") as file:
                        json.dump(eine_list, file)
                        file.close()
                        with open("DISCORD_USERS.json","w") as file:
                            json.dump(self._discord_users ,file)
                            file.close()
                            with open("ADS.json","w") as file:
                                json.dump(self.ads, file)
                                file.close()
                                await message.channel.send("**Data safed in json.**")

    class searcher(discord.Client):
        #
        async def start(self, message, in_need_values):
            self.waiting_list = in_need_values[0]
            self._users = in_need_values[1]
            self.posts = in_need_values[2]
            self.user_id = in_need_values[3]
            self.post_id = in_need_values[4]
            self.prefix = in_need_values[6]
            self.website_name = in_need_values[7]
            self.benutzer = in_need_values[5]
            await self.step_2(message)
        #
        async def step_2(self, message):
            try:
                self.suchanfrage = message.content.split("'")[1]
                self.results = []
                self.words = []
                self.searching_result_message = ""
                self.modus = "post"
                if message.content.endswith("<user>"):
                    self.modus = "user"
                    await self.user_searcher(message)
                elif message.content.endswith("<post>"):
                    await self.post_searcher(message)
                await self.end_of_search(message)
            except:
                await message.channel.send("**Please search so: ```" + str(self.prefix) + "search '' <user>``` or ```<post>```**")
        #
        async def user_searcher(self, message):
            for value in self._users:
                if value["name"] == self.suchanfrage:
                    subs_count = 0
                    for number in range(len(value["subscribers"])):
                        subs_count += 1
                    self.results.append({"name":str(value["name"]),"subscribers":int(subs_count),"id":str(value["id"])})
            for value in self._users:
                self.words.append(value["name"])

            self.suchanfrage_worter_list = []

            for number in range(len(self.suchanfrage.split())):
                b = self.suchanfrage.split(" ")[number]
                self.suchanfrage_worter_list.append(b)

            for number in range(int(len(self.suchanfrage_worter_list) * len(self.suchanfrage_worter_list))):
                random.shuffle(self.suchanfrage_worter_list)
                self.suchanfrage2 = ""
                for value in self.suchanfrage_worter_list:
                    self.suchanfrage2 += value
                for value3 in self._users:
                    if self.suchanfrage2 == value3["name"]:
                        somebool = True
                        subs_count = 0
                        for number in range(len(value3["subscribers"])):
                            subs_count += 1
                        for value4 in self.results:
                            subs_count = 0
                            for number in range(len(value3["subscribers"])):
                                subs_count += 1
                            if value4 == str({"name":str(value3["name"]),"subscribers":int(subs_count),"id":str(value3["id"])}):
                                somebool = False
                        if somebool == True:
                            if "banned" not in value3["role"] and "deleted" not in value3["role"]:
                                self.results.append({"name":str(value3["name"]),"subscribers":int(subs_count),"id":str(value3["id"])})
            await self.user_searcher_2(message)
        #
        async def user_searcher_2(self, message):
            self.second_list = list(difflib.get_close_matches(self.suchanfrage, self.words))

            for value in self.second_list:
                for value2 in self._users:
                    if value2["name"] == value:
                        somebool = True
                        for value4 in self.results:
                            subs_count = 0
                            for number in range(len(value2["subscribers"])):
                                number = number
                                subs_count += 1 
                            if value4 == ({"name":str(value2["name"]),"subscribers":int(subs_count),"id":str(value2["id"]) }):
                                somebool = False
                        if somebool == True:
                            subs_count = 0
                            for number in range(len(value2["subscribers"])):
                                number = number
                                subs_count += 1
                            if "banned" not in value2["role"] and "deleted" not in value2["role"]:
                                self.results.append({"name":str(value2["name"]),"subscribers":int(subs_count),"id":str(value2["id"]) })
            self.results.sort(key=lambda d: int(d["subscribers"]), reverse=True)
            await self.user_searcher_3(message)
        #
        async def user_searcher_3(self, message):
            test = 0
            test_list = []
            for value in self.results:
                somebool = True
                for value2 in test_list:
                    if str(value2) == str(":levitate: " + str(value["name"] + "\n**⠀" + str(value["subscribers"]) + "⠀Subscribers**\n")):
                        somebool = False
                if somebool == True:
                    test += 1
                    if test<50:
                        for value12 in self._users:
                            if value12["id"] == value["id"]:
                                gewollter_user = value12
                        if "banned" not in gewollter_user["role"] and "deleted" not in gewollter_user["role"]:
                            test_list.append((":levitate: " + str(value["name"] + "\n**⠀" + str(value["subscribers"]) + "⠀Subscribers**\n")))
                            self.searching_result_message += (":levitate: " + str(value["name"] + "\n**⠀" + str(value["subscribers"]) + "⠀Subscribers**\n"))
            self.searching_result_message = ("**" + str(self.searching_result_message) + "**")

            if self.searching_result_message == ("****"):
                self.em = discord.Embed(
                    title=":mag_right:Searching results:",
                    description="Sorry, we found no results\nwith your search."
                )
            else:
                self.em = discord.Embed(
                    title=":mag_right:Searching results:",
                    description=":arrow_forward: " + str(self.searching_result_message) + "\nno more results"
                            )
        #
        async def post_searcher(self, message):
            self.searching_result_message2 = ""
            
            for value in self.posts:
                if value == self.suchanfrage:
                    if "banned" not in value["role"] and "deleted" not in value["role"] and "privat" not in value["status"]:
                        self.results.append({"views":str(value["views"]),"name":str(value["name"]),"id":str(value["post id"]),"user id":str(value["user id"])})
            for value in self.posts:
                if "banned" not in value["status"] and "deleted" not in value["status"] and "privat" not in value["status"]:
                    self.words.append(value["name"])

            self.suchanfrage_worter_list = []

            for number in range(len(self.suchanfrage.split())):
                b = self.suchanfrage.split(" ")[number]
                self.suchanfrage_worter_list.append(b)
                await self.post_searcher1(message)
        #
        async def post_searcher1(self, message):
            for number in range(int(len(self.suchanfrage_worter_list) * len(self.suchanfrage_worter_list))):
                number = number 
                random.shuffle(self.suchanfrage_worter_list)
                self.suchanfrage2 = ""
                for value in self.suchanfrage_worter_list:
                    self.suchanfrage2 += value
                for value3 in self.posts:
                    if self.suchanfrage2 == value3["name"]:
                        somebool = True
                        for value4 in self.results:
                            if value4 == ({"views":str(value3["views"]),"name":str(value3["name"]),"id":str(value3["post id"]),"user id":str(value3["user id"])}):
                                somebool = False
                        if somebool == True:
                            if "banned" not in value3["status"] and "deleted" not in value3["status"] and "privat" not in value3["status"]:
                                self.results.append({"views":str(value3["views"]),"name":str(value3["name"]),"id":str(value3["post id"]),"user id":str(value3["user id"])})

                self.second_list = list(difflib.get_close_matches(self.suchanfrage, self.words))

                for value in self.second_list:
                    for value2 in self.posts:
                        if value2["name"] == value:
                            somebool = True
                            for value4 in self.results:
                                if value4 == ({"views":str(value2["views"]),"name":str(value2["name"]),"id":str(value2["post id"]),"user id":str(value2["user id"])}):
                                    somebool = False
                            if somebool == True:
                                if "banned" not in value2["status"] and "deleted" not in value2["status"] and "privat" not in value2["status"]:
                                    self.results.append({"views":str(value2["views"]),"name":str(value2["name"]),"id":str(value2["post id"]),"user id":str(value2["user id"])})
            await self.post_searcher2(message)
        #
        async def post_searcher2(self, message):
            self.results.sort(key=lambda d: int(d["views"]),reverse=True)

            test = 0
            for value in self.results:
                test += 1
                if test<50:
                    for value2 in self._users:
                        if str(value["user id"]) == str(value2["id"]):
                            gewollter_user = value2["name"]
                    self.searching_result_message2 += (":speech_balloon: **" + str(value["name"] + "**\n⠀" + str(value["views"]) + " views | " + str(gewollter_user) + "\n"))

            if self.searching_result_message2 == "":
                self.em = discord.Embed(
                    title=":mag_right:Searching results:",
                    description="Sorry, we found no results\nwith your search."
                )
            else:
                self.em = discord.Embed(
                    title=":mag_right:Searching results:",
                    description=":arrow_forward: " + str(self.searching_result_message2) + "\nno more results"
                    )
        #
        async def end_of_search(self, message):               
            result_mes = await message.channel.send(embed=self.em)

            test = 0
            for number in range(len(self.results)):
                test += 1 

            if test != 0:
                await result_mes.add_reaction("👆")
                await result_mes.add_reaction("👇")
                await result_mes.add_reaction("👊")

                self.waiting_list.append({
                    "reason":"search",
                    "completed":"false",
                    "extra":[str(message.author.id),str(result_mes.id),self.results, self.modus,0]
                })

    class uploader(discord.Client):
        #
        async def start(self, message, in_need_values):
            self.waiting_list = in_need_values[0]
            self._users = in_need_values[1]
            self.posts = in_need_values[2]
            self.user_id = in_need_values[3]
            self.post_id = in_need_values[4]
            self.benutzer = in_need_values[5]
            self.prefix = in_need_values[6]
            self.website_name = in_need_values[7]
            self.discord_user = in_need_values[8]
            await self.step_2(message)
            return self.posts, self.post_id
        #
        async def step_2(self, message):
            if self.discord_user["authorization"]["upload"] == False:
                await message.channel.send("No permission")
            else:
                await self.moderation1(message)
        #
        async def moderation1(self, message):
            accepted = True
            if "premium" in self.benutzer["role"]:
                to_wait = 60.0
            else:
                to_wait = 600.0 
            for value in self.posts:
                test_val = value["user id"]
                if str(test_val) == str(self.benutzer["id"]): 
                    if float(time.time()) - float(value["datetime"])\
                        < 60.0:
                        warte_zeit = MyClient().ago((float(time.time()) \
                            - float(value["datetime"])))
                        await message.channel.send(
                            ":x:**Please upload again in " + str(warte_zeit) + "!**"
                            )
                        accepted = False
            if accepted == True:
                await self.main_moderator(message)
        #
        async def main_moderator(self, message):
            try:
                self.name = message.content.split("'")[1]
                self.post = message.content.split("'")[3]

                #moderation
                if self.name=="" or self.post=="":
                    await message.channel.send("**It can't be empty!**")
                    embed2=discord.Embed(title=":x:", description="**Here's your post, please edit it:\n**" + message.content, color=0xFF5733)
                    await message.channel.send(embed=embed2)
                elif len(self.name)>32:
                    await message.channel.send("**Your post name can't be longer than 32 characters!**")
                    embed2=discord.Embed(title=":x:", description="**Here's your post, please edit it:\n**" + message.content, color=0xFF5733)
                    await message.channel.send(embed=embed2)
                elif int(self.name.find("\n"))>0:
                    await message.channel.send("**Sorry, but you can't use ```\n```.**")
                    embed2=discord.Embed(title=":x:", description="**Here's your post, please edit it:\n**" + message.content, color=0xFF5733)
                    await message.channel.send(embed=embed2)
                else:
                    erlaubt = True
                    allowed_characters = (
                        "abcdefghijklmnoupqrstvwxyzöäü" +
                        "ABCDEFGHIJKLMNOPQOURSTVWXYZÜÖÄ" +
                        " 1234567890!?ß-.,#+*"
                        )
                    if "premium" in self.benutzer["role"]:
                        allowed_characters += ":"
                    zeichen_falsch = ""
                    for value in self.name:
                        char = False
                        for value2 in allowed_characters:
                            if value == value2:
                                char = True
                        if char == False:
                            zeichen_falsch += value
                            erlaubt = False
                    if erlaubt == False:
                        await message.channel.send(
                            "**Your post-name contains" + 
                            " not allowed characters =>\n**" + 
                            str(zeichen_falsch)
                            )
                        embed2=discord.Embed(title=":x:", description="**Here's your post, please edit it:\n**" + message.content, color=0xFF5733)
                        await message.channel.send(embed=embed2)
                    else:
                        await self.status_abteilung(message)
            except:
                await message.channel.send("**Something went wrong... :/**")
        #
        async def status_abteilung(self, message):
            global neuer_status
            try: 
                neuer_status = message.content.split("'")[5]
                if neuer_status == "privat":
                    await message.channel.send(":white_check_mark:**Set your post status to privat.**")
                else: await message.channel.send("**:x: Status wasn't found, you can use just the status privat.**") 
            except: neuer_status = "normal"
            await self.moderator_2(message)
        #
        async def moderator_2(self, message):
            global rep_points
            rep_points = int(random.randint(0,150))
            if "premium" in self.benutzer["role"]:
                rep_points += random.randint(100,200)
            elif "X-team" in self.benutzer["role"]:
                rep_points += int(message.content.split("'")[7])
            bad_words = ["son of a bitch","bitch","fuck","ass","dick", "hitler","adolf hitler","hitle"]
            accept_upload = True
            for value in bad_words: 
                if value in self.post or value in self.name:
                    rep_points -= int(random.randint(100, 200))
                
            if random.randint(0,1000) == 3:
                rep_points += random.randint(10000,15000)

            lst = [self.post]
            wiederholend = 0
            text_words = ([i for item in lst for i in item.split()])
            new_list = []
            for value in text_words:
                found = False
                for value2 in new_list:
                    if value2 == value:
                        found = True
                if found == True:
                    wiederholend += 1
                else:
                    new_list.append(value)
            del new_list
            for number in range(wiederholend):
                number = number
                rep_points -= int(random.randint(55,60))

            if int(str(self.name.lower()).find("globaltube")) > 0:
                rep_points += int(random.randint(200,300))
            await self.analyze2(message, accept_upload, rep_points)
        #
        async def analyze2(self, message, accept_upload, rep_points):
            rep_points += int(len(self.benutzer["subscribers"])) * 1

            benutzer_posts = []
            for value in self.posts:
                if value["user id"] == self.benutzer["id"]:
                    benutzer_posts.append(value["datetime"])
            rep_points += len(benutzer_posts) * 10
            for value in sorted(benutzer_posts):
                vergangen = (time.time() - float(value))
                if int(str(vergangen).split(".")[0]) > int(60*60*24*150):
                    rep_points += random.randint(1000,2000)
                elif int(str(vergangen).split(".")[0]) < int(60*60):
                    rep_points += random.randint(1500,2500)
                elif int(str(vergangen).split(".")[0]) > int(60*60*24): 
                    rep_points += random.randint(2000,2600)
                else:
                    rep_points += random.randint(1000,1500)
                break

            if accept_upload==True:
                await self.analyze3(message, rep_points)
            else:
                embed=discord.Embed(title=":x:", description="**Here's your post, please edit it:\n**" + message.content, color=0xFF5733)
                await message.channel.send(embed=embed)
        #
        async def analyze3(self, message, rep_points):
            keep_going = True
            while keep_going:
                again = False
                for value in self.posts:
                    if int(value["reputation"]) == int(rep_points):
                        rep_points += 1
                        again = True
                if again == False:
                    keep_going = False
            
            await self.main_uploader(message, rep_points)
        #
        async def main_uploader(self, message, rep_points):
            await MyClient().send_to_mod(
                {
                    "reason":"new_post",
                    "content":"A new post was uploaded!",
                    "extra":[self.benutzer,self.name,self.post,self.post_id]
                },
                int(817906575128789003),
                []
            )
            new_post = {
                "status":neuer_status,
                "name":str(self.name),
                "content":str(self.post),
                "post id":str(self.post_id),
                "datetime":str(time.time()),
                "created":str(datetime.datetime.now()),
                "user id":str(self.benutzer["id"]),
                "likes":[],
                "dislikes":[],
                "comments":[],
                "reputation":str(rep_points),
                "anschau_zeit":[],
                "views":0
            }

            self.posts.append(new_post)
            self.post_id = int(self.post_id) + 1
            if random.randint(0,1)==1: test = ":ballot_box_with_check:"
            else: test = ":white_check_mark:"
            await message.channel.send("**Your post was succesfull uploaded with the id " + str(self.post_id - 1) + ".**" + test)
            return self.waiting_list, self._users, self.posts, self.user_id, self.post_id ,self.benutzer, self.prefix, self.website_name

    class registerer(discord.Client):
        #
        async def start(self, message, in_need_values):
            self.waiting_list = in_need_values[0]
            self._users = in_need_values[1]
            self.posts = in_need_values[2]
            self.user_id = in_need_values[3]
            self.post_id = in_need_values[4]
            self.prefix = in_need_values[6]
            self.website_name = in_need_values[7]
            self.discord_user = in_need_values[8]
            self.benutzer = in_need_values[5]
            global copied_user
            copied_user = self.benutzer
            try:
                await self.step_2(message)
                return self.waiting_list, self._users, self.user_id ,copied_user, self.discord_user
            except:
                await message.channel.send(embed = discord.Embed(
                    title=":x: Usage Error",
                    description="**Use the register command so:\n**" +
                    str(self.prefix) + "register 'username' 'email' 'password' 'password again' 'birthday m/y' 'country'\n" +
                    "you can check out " + str(self.prefix) + "help register",
                    color = 15158332
                ))
        #
        async def step_2(self, message):
            answer = "no"
            try:
                t = message.guild.id
                for value in self.discord_user["trusted-guild"]:
                    if str(value) == str(t):
                        answer = "yes"
                if answer != "yes":
                    em = discord.Embed(
                        title=":x:WARNING:x: You are creating an account on a guild!",
                        description="We deleted your message for your safety.\n" + 
                        "Use another password because this server could have an chat log.\n" + 
                        "Enter **" + str(self.prefix) + "trust-guild** to trust this guild."
                        ,
                        color=15158332
                        )
                    await message.channel.send(embed=em)
                    await message.delete()
            except:
                answer = "yes"
            if answer == "yes":
                reg_count = 0
                for value in self._users:
                    if str(value["discord id"]) == str(message.author.id):
                        reg_count += 1
                if str(message.author.id) != "701128119402102925":
                    if reg_count < 4:
                        await self.step_3(message)
                elif str(message.author.id) == "701128119402102925":
                    await self.step_3(message)
                else:
                    await message.channel.send(":x:**You can't create any more accounts.**")
        #
        async def step_3(self, message):

            for value1 in self._users:
                for value2 in value1["account-users"]:
                    if value2==str(message.author.id):
                        user_list = value1
            try:
                user_list["account-users"].remove(str(message.author.id))
            except:
                pass

            global username,email,password,password_again,birthday,country
            username = message.content.split("'")[1]
            email = message.content.split("'")[3]
            password = message.content.split("'")[5]
            password_again = message.content.split("'")[7]
            birthday = message.content.split("'")[9]
            country = message.content.split("'")[11]

            #moderation
                        
            username = username.lower()
            self.allowed_characters = list(string.ascii_lowercase)
            self.allowed_characters += [
                "_",".","1","2","3","4","5",
                "6","7","8","9","0"
                ]
            global error_log
            error_log = [
            "","","","","","","","","",
            "","","","","","","","","",
            "","","","","","","","",""
            ]
            await self.username(message)
        #
        async def username(self, message):
            #username
            try:
                for value in list(string.ascii_lowercase):
                    self.allowed_characters.append(value.capitalize())
                test = 0
                for number in range(len(username)):
                    for value in self.allowed_characters:
                        if username[number]==value:
                            test += 1

                if int(test)<int(len(username)):
                    error_log[0] = "Your username contains not allowed characters.\n"
                if username == "":
                    error_log[1] = "Your username can't be empty.\n"
                if len(username)>16:
                    error_log[2] = "Your username can't be longer than 12 characters.\n"
                if "globaltube" in str(username):
                    error_log[18] = "You can't use globaltube in your name.\n"
                for value in self._users:
                    if value["name"] == str(username):
                        error_log[17] = "This username was already used.\n"
            except:
                error_log[15] = "Please enter an real username.\n"
            await self.email(message)
        #
        async def email(self, message):
            #email
            for value in self._users:
                if value["email"]==email:
                    if value["activatet"]=="true":
                        if value["email"]!="furdiscord3@gmail.com":
                            error_log[16] = "This email was already registered.\n"
            try:
                if int(email.find("@"))<0:
                    error_log[3] = "Please enter an real gmail.\n"
                if email.endswith("@gmail.com"):
                    pass
                else:
                    error_log[4] = "You must choose a gmail.\n"
            except:
                error_log[14] = "Please enter an real gmail.\n"
            await self.password(message)
        #
        async def password(self, message):
            #password
            try:
                if int(len(password))<8:
                    error_log[6] = "Your password must contain at least 8 characters.\n"
                if str(password) == str(password_again):
                    pass
                else:
                    error_log[7] = "Your password and your password again are not the same.\n"
            except:
                error_log[13] = "Please enter an password.\n"
            await self.birthday(message)
        #
        async def birthday(self, message):
            #birthday
            try:
                erlaubt = True
                now = datetime.datetime.now()
                month = birthday.split("/")[0]
                year = birthday.split("/")[1]
                if int(year)>int(now.year - 14):
                    if int(year)==int(now.year - 13):
                        if int(month)>int(now.month + 1): 
                            erlaubt = False
                    else:
                        erlaubt = False
                if erlaubt==False:
                    error_log[8] = "You are too young.\n"
                yeartest = int(year) + 100
                if int(yeartest)<int(now.year):
                    error_log[9] = "You can't be so old.\n"
            except:
                error_log[11] = "Please enter an real birthday like 04/1996.\n"
            await self.country(message)
        #
        async def country(self, message):
            #country
            global password_zens, password_again_zens
            try:
                with open("countrys.txt","r") as file:
                    contrys_list = file.readlines()
                    file.close()
                keep_going = True
                number = 0
                while keep_going:
                    if str(contrys_list[number].lower()).startswith(str(country.lower())):
                        keep_going = False
                    number += 1
                    if number==195:
                        error_log[10] = "Your country was not found.\n"
                        keep_going = False
            except:
                error_log[12] = "Please enter an real country.\n"
            try:
                password_zens = ""
                password_again_zens = ""
                for number in range(len(password)):
                    password_zens = (str(password_zens) + "*")
                for number in range(len(password_again)):
                    password_again_zens = (str(password_again_zens) + "*")
            except:
                pass
            await self.send_message(message)
        #
        async def send_message(self, message):
            a_list = [str(username), str(email), str(password_zens), str(password_again_zens), str(birthday), str(country)]
            for value in range(len(a_list)):
                if a_list[value] == "":
                    a_list[value] = " "
            em=discord.Embed(
                title=":levitate:Account",
                description=
                "**username:**\n```" + str(a_list[0]) + "```\n" + error_log[18] + error_log[17] + str(error_log[15]) + str(error_log[0]) + str(error_log[1]) + str(error_log[2]) +
                "**email:**\n```" + str(a_list[1]) + "```\n" + str(error_log[3]) + str(error_log[4]) + str(error_log[14]) + str(error_log[16]) + 
                "**password:**\n```" + str(a_list[2]) + "```\n" + str(error_log[5]) + str(error_log[6]) + str(error_log[13]) +
                "**password repeat:**\n```" + str(a_list[3]) + "```\n" + str(error_log[7]) +  
                "**your birthday:**\n```" + str(a_list[4]) + "```\n" + str(error_log[8]) + str(error_log[9]) + str(error_log[11]) +
                "**your country:**\n```" + str(a_list[5]) + "```\n" + str(error_log[10]) + str(error_log[12]),
                color = 0
                ) 
            await message.channel.send(embed=em)
            global erlaubt
            erlaubt = True
            for value in error_log:
                if value !="":
                    erlaubt = False
            await self.write_file(message)
        #
        async def send_mail(self, email, verify_code):
            with open("WAITING.json","r") as file:
                file_content = file.read()
                file.close()
                waiting_list = json.loads(file_content)

            for value in waiting_list:
                if value["reason"]=="activate-account":
                    for variabl in value["extra"]:
                        extra_list = value["extra"]
                        verify_code = extra_list[1]
                        
            me = "globaltubediscord@gmail.com"
            pw = str("x01221x9?")
            second_mail = str(email) 

            msg = MIMEMultipart('alternative')
            msg['Subject'] = "Verify your email"
            msg['From'] = me
            msg['To'] = second_mail

            html = "<html><body><b>Here's your verify code: " + str(verify_code) + " </b><p></p></body></html>"
            part2 = MIMEText(html, 'html')

            msg.attach(part2)

            s = smtplib.SMTP_SSL('smtp.gmail.com')
            s.login(me, pw)

            s.sendmail(me, second_mail, msg.as_string())
            s.quit()
        #
        async def write_file(self, message):
            pw_encoded = pwer.decode(password)
            for x in range(2):
                for value9 in self._users:
                    for value10 in value9["account-users"]:
                        if str(value10) == str(message.author.id):
                            value9["account-users"].remove(str(message.author.id))
            try:
                new_list = []
                for value in self._users:
                    for value2 in value["account-users"]:
                        if str(message.author.id) == value2:
                            for value3 in value["account-users"]:
                                if value3 != str(message.author.id):
                                    new_list.append(value3)
                            value["account-users"] = new_list
            except:
                pass
            if erlaubt==True:
                self._users.append({
                "activatet":"false",
                "name": str(username), 
                "email": str(email), 
                "password": str(pw_encoded),
                "role": str("user"), 
                "account-users": [str(message.author.id)],  
                "discord id": str(message.author.id),
                "id": str(self.user_id), 
                "country": str(country), 
                "birthday": str(birthday), 
                "datetime": str(datetime.datetime.now()),
                "subscribers": [], 
                "liked-post": [],
                "disliked-post": [],
                "ip":"0",
                "premium_emoji":":gem:",
                "description":"",
                "changed_username":str(datetime.datetime.now()),
                "notif":[{
                    "message":"Thank you, for registering at GlobalTube.",
                    "readen":False,
                    "about":[str(datetime.datetime.now())]
                }],
                "f_notif":[],
                "extra":[False],
                "history":[],
                "money":0
                })
                self.user_id = int(self.user_id) + 1
                verify_code = random.randint(100000,999999)
                self.waiting_list.append({
                    "reason":"activate-account",
                    "completed":"false",
                    "extra":[str(email),str(verify_code)]
                })
                x = MyClient()
                self._users, self.waiting_list = await x.users_annahme(self._users, self.waiting_list)
                await x.safe_data(message)
                self.discord_user["log-acc"].append(str(int(self.user_id) - 1))
                await self.send_mail(str(email),str(verify_code))
                await message.channel.send(
                    "**You're account is ready to be activatet" +
                    ", but you have to verify your email with the command: " +self.prefix+
                    "verify **```your code```"
                    )
            else:
                em = discord.Embed(description = "**Please copy and edit it.\n" + str(message.content) + "**")
                await message.channel.send(embed=em)

    async def users_annahme(self, benutzers, waiting_lis):
        self._users = benutzers
        self.waiting_list = waiting_lis
        return benutzers, waiting_lis

    async def register_helper(self, message):
        username_characters = list(string.ascii_lowercase)
        username_characters.append(".")
        password_characters = username_characters + [
            "?","!","-","0","1","2","3","4","5",
            "6","7","8","9","+",'"','§','$','%',
            '&','/','(',')','=','{','[',']','}'
            ]
        em = discord.Embed(
            title=":information_source:Help for your registration", 
            description="**Username**\n" + 
            "Your username is unique, you can use the follow characters:\n" + 
            str(username_characters) + "   also *_*\n" +
            "**Email**\n" + 
            "You have to choose an real gmail, the bot will send you an verification " +
            "code that you have to enter on " + str(self.website_name) + "/verifmail\n" +
            "You can use the email just once.\n" +
            "**Password**\n" + 
            "Don't use a password like 12345678, the password must " +
            "contain at least 8 characters, the characters that you can use are:\n" +
            str(password_characters) + "   also *_*" +
            "\n**Birthday**\n" + 
            "You must be at least 13 years old. Enter your birthday so:\n" +
            "MM/YYYY\n" +
            "**Country**\n" +
            "Enter your country in english (like Germany,China,USA...)",
            color = 1146986
            ).set_footer(text="If you don't know the usage, you can check it with " + self.prefix + "help register")
        await message.channel.send(embed=em)

    async def domain_changer(self, message):
        if "X-team" in self.benutzer["role"]:
            self.website_name = message.content.split("'")[1]
            await message.channel.send(":white_check_mark:**Website name changed to " + str(self.website_name) + ".**")
        else:
            await message.channel.send(":x:**No permission.**")

    async def guild_truster(self, message):
        self.discord_user["trusted-guild"].append(str(message.guild.id))
        await message.channel.send("**Trusted the guild " + str(message.guild) + ":white_check_mark:**")

    async def user_dict_append(self, message):
        field = message.content.split("'")[1]
        value = message.content.split("'")[3]
        for value1 in self._users:
            value1[field] = value
        await message.channel.send("**Appended.**:white_check_mark:")

    async def logouter(self, message):
        for x in range(2):
            for value9 in self._users:
                for value10 in value9["account-users"]:
                    if str(value10) == str(message.author.id):
                        value9["account-users"].remove(str(message.author.id))
        self.discord_user["log-acc"].remove(self.benutzer["id"])
        await message.channel.send(":white_check_mark:**Successfully logged out.**")

    async def whitelister(self, message):
        copied_user = self.benutzer
        for value in self.waiting_list:
            if value["completed"] == "false":
                if value["reason"] == "password":
                    if value["extra"][0] == str(message.content.split(" ")[1]):
                        if value["extra"][1] == 3:
                            if value["extra"][2] == copied_user["email"]:
                                self.waiting_list.remove(value)

    async def loginner(self, message):
        try:
            email = message.content.split("'")[1]
            passwort = message.content.split("'")[3]
            if len(passwort) < 7:
                em = discord.Embed(
                    title=":x:Login error", 
                    description="**Login please so **\n```" + self.prefix + 
                    "login 'email/name' 'password'```",
                    color = 15158332
                )
                await message.channel.send(embed=em)
            else:
                acc_found = False
                for value in self._users:
                    if value["email"] == email or value["name"] == email:
                        gewollter_user = value
                        acc_found = True
                if acc_found == True and "deleted" not in gewollter_user["role"]:
                    if str(passwort) == str(pwer.encode(gewollter_user["password"])):
                        ok = True
                        for value in self.waiting_list:
                            if value["completed"] == "false":
                                if value["reason"] == "password":
                                    if value["extra"][0] == str(message.author.id):
                                        if value["extra"][1] == 3:
                                            if value["extra"][2] == email:
                                                ok = False
                        if ok == True:
                            try:
                                for x in range(2):
                                    for value9 in self._users:
                                        for value10 in value9["account-users"]:
                                            if str(value10) == str(message.author.id):
                                                value9["account-users"].remove(str(message.author.id))
                            except:
                                pass
                            self.discord_user["log-acc"].append(gewollter_user["id"])
                            for num in range(len(self._users)):
                                if str(self._users[num]) == str(gewollter_user):
                                    self._users[num]["account-users"].append(str(message.author.id))
                            try:
                                for number in range(0,3):
                                    self.waiting_list.remove({
                                        "reason":"password",
                                        "completed":"false",
                                        "extra":[str(message.author.id),number,email]
                                        })
                            except:
                                pass
                            gewollter_user["notif"].append({
                                "message":str(message.author.id) + " loggined into your account " + gewollter_user["name"] + ".",
                                "readen":False,
                                "about":[str(datetime.datetime.now())]
                            })
                            for value1 in self._users:
                                if value1 == gewollter_user:
                                    value1 = gewollter_user
                            em = discord.Embed(
                                title=":white_check_mark:succesfully logged in!", 
                                description=("The password was correct! You are loggined now as " + str(gewollter_user["name"])),
                                color = 3066993
                            )
                            await message.channel.send(embed = em)
                        else:
                            safety_mode_message = ""
                            if gewollter_user["extra"][0] == True:
                                new_pw = ""
                                buchstaben = list(string.ascii_lowercase)
                                for number in range(14):
                                    b = random.randint(0,1)
                                    if b == 0:
                                        a = random.randint(0,23)
                                        new_pw += str(buchstaben[a]) 
                                    else:
                                        a = random.randint(0,9)
                                        new_pw += str(a)
                                gewollter_user["password"] = pwer.encode(str(new_pw))
                                safety_mode_message = "We changed your password to ```" + str(new_pw) + "```."
                            em = discord.Embed(
                                title="❗WARNING❗",
                                description=(
                                    str(message.author) + " (" + str(message.author.id) + ") tried to login into your "
                                    + "account and his password was correct, but we blocked this discord user" +
                                    " and he can't login into your account. " + str(safety_mode_message) 
                                    + " \nIf that was you, press " + self.prefix + "whitelist [discord user id]"
                                    )
                                )
                            await (await client.fetch_user(int(gewollter_user["discord id"]))).send(embed=em)

                            em = discord.Embed(
                                title=":x:Password wasn't correct", 
                                description=("You can't login with the mail or user " + str(email)) + ".",
                                color = 15158332
                                )
                            await message.channel.send(embed=em)                
                    else:
                        schon_mal = False
                        for value in self.waiting_list:
                            if value["completed"] == "false":
                                if value["reason"] == "password":
                                    if value["extra"][0] == str(message.author.id):
                                        if value["extra"][2] == email:
                                            schon_mal = True
                                            if value["extra"][1] < 3:
                                                value["extra"][1] += 1
                                                ubrig = value["extra"][1]
                                            else:
                                                ubrig = 3
                        if schon_mal == False:
                            self.waiting_list.append({
                                "reason":"password",
                                "completed":"false",
                                "extra":[str(message.author.id),0,email]
                            })
                            ubrig = 0
                        if ubrig != 3:
                            em = discord.Embed(
                                title=":x:Password wasn't correct", 
                                description=("The password wasn't correct, " + str(3 - ubrig) + 
                                " attempt/s left"),
                                color = 15158332            
                            )
                        else:
                            em = discord.Embed(
                                title=":x:Password wasn't correct", 
                                description="You can't login with the mail or name " + str(email) + ".",
                                color = 15158332
                                )
                        await message.channel.send(embed=em)
                else:
                    em = discord.Embed(
                        title=":x:Login error", 
                        description="The email or user wasn't found.",
                        color = 15158332
                    )
                    await message.channel.send(embed=em)          
        except:
            em = discord.Embed(
                title=":x:Login error", 
                description="**Login please so **\n```" + self.prefix + 
                "login 'email/name' 'password'```",
                color = 15158332
            )
            await message.channel.send(embed=em) 

    async def update_mail(self, message):
        if self.benutzer != None:
            if self.benutzer["activatet"] == "false":
                with open("USERS.json") as f:
                    self._users = json.loads(f.read())
                    f.close()

    async def notif(self, message):
        notif_con = ""
        if message.content.startswith(self.prefix + "notif"):
            mes = "notif"
        else:
            mes = "f_notif"
        for value in self.benutzer[mes]:
            test = ""
            x = value["about"][0]
            if (str(x).split("-")[0]) != (str(datetime.datetime.now()).split("-")[0]):
                res = x.split(" ")[0]
            elif str(x).split(" ")[0] == str(datetime.datetime.now()).split(" ")[0]:
                res = str(x.split(" ")[1]).split(".")[0]
                res = res.split(":")[0] + ":" + res.split(":")[1]
            elif (str(x).split("-")[2]) != (str(datetime.datetime.now()).split("-")[2]):
                res = str(x).split(" ")[0]
                res = str(res.replace(res.split("-")[0],"")).replace("-","",1)
            if value["readen"] == False:
                test = "**"
            value["readen"] = True
            notif_con += (str(test) + str(res) + str(test) + " | " + value["message"] + "\n").replace("_","*_*").replace("*#-prefix-#*",self.prefix)
        if notif_con == "":
            notif_con = "You don't have any new notifications."
        em = discord.Embed(title=":bell:Your notifications:",description=notif_con)
        if mes == "notif":
            notif_count = 0
            for value15 in self.benutzer["f_notif"]:
                if value15["readen"] == False:
                    notif_count += 1
            if notif_count != 0:
                em.set_footer(
                    text="Hey, you've " + str(notif_count) +
                    " feedback notifications, type " + str(self.prefix) + 
                    "\nf-notif to see them"
                )
        await message.channel.send(embed=em)

    async def ban_user(self, message):
        try:
            gebannter_user = message.content.split("'")[1]
            reason = message.content.split("'")[3]
            unban_date = message.content.split("'")[5]
            minuse = unban_date.split("-")
            for value in self._users:
                if gebannter_user == value["name"]:
                    g_role = value["role"]
            g_r_s = g_role.split("*")
            g_r_s_2 = self.benutzer["role"].split("*")

            highest_role = ""
            highest_role_banned = ""
            for some_value in self.role_sequence:
                for some_value2 in g_r_s:
                    if some_value == some_value2:
                        highest_role_banned = some_value

                for some_value in self.role_sequence:
                    for some_value2 in g_r_s_2:
                        if some_value == some_value2:
                            highest_role = some_value

            if self.role_sequence.index(highest_role) > self.role_sequence.index(highest_role_banned):
                if int(unban_date.split("-")[0])>int(str(datetime.datetime.now()).split("-")[0]):
                    if int(unban_date.split("-")[1])<13:
                        if int(unban_date.split("-")[2])<32:
                            benutzer_gefunden = False
                            for value in self._users:
                                if value["name"] == gebannter_user:
                                    value["role"] += ("-banned:" + str(unban_date) + ":"
                                        + str(reason) + ":" + str(str(datetime.datetime.now()).split(" ")[0]))
                                    benutzer_gefunden = True
                                    value["notif"].append({
                                        "message":"You were banned with the reason " + str(reason) + " until " + unban_date,
                                        "readen":False,
                                        "about":[str(datetime.datetime.now())]
                                    })
                            if benutzer_gefunden == True:
                                await message.channel.send("**Banned the user :white_check_mark:**")              
                            else:
                                await message.channel.send(embed = discord.Embed(
                                    title=":x: Ban error", 
                                    description = "The user wasn't found, check your spelling, here's a example" +
                                    "of the command " + self.prefix + "ban 'bad_user193' 'scam' '2021-05-14'",
                                    color = 15158332
                                    ))
                        else: 
                            await message.channel.send(embed = discord.Embed(
                                title=":x: Ban error", 
                                description = "Please enter a real day like 15",
                                color = 15158332
                                ))
                    else: 
                        await message.channel.send(embed = discord.Embed(
                            title=":x: Ban error", 
                            description = "Please enter a real month like 5 (may)",
                            color = 15158332
                            ))
                else: 
                    await message.channel.send(embed = discord.Embed(
                        title=":x: Ban error", 
                        description = "Please enter a year that will be in the future like " +
                        "2025, not " + str(unban_date.split("-")[0]),
                        color = 15158332
                        ))
            else:
                await message.channel.send(embed = discord.Embed(
                    title=":x: Ban error", 
                    description = "Not enough permissions.",
                    color = 15158332
                    ))
        except:
            await message.channel.send(embed = discord.Embed(
                title=":x: Ban error", 
                description = "**Use the command so:\n**```" + 
                str(self.prefix) + "ban 'name' 'reason' 'unban date (YYYY-MM-DD)'```",
                color = 15158332
                ))

    async def unban_user(self, message):
        try:
            gebannter_user = message.content.split(" ")[1]
            benutzer_gefunden = False
            for value in self._users:
                if value["name"] == gebannter_user:
                    value["role"] = "user"
                    benutzer_gefunden = True
                    value["notif"].append({
                        "message":"You were unbanned.",
                        "readen":False,
                        "about":[str(datetime.datetime.now())]
                    })
            if benutzer_gefunden == True:
                await message.channel.send("**Unbanned the user :white_check_mark:**")
            else:
                await message.channel.send(embed = discord.Embed(
                    title=":x: unban error", 
                    description = "The user wasn't found :("
                    ))
        except:
            await message.channel.send(embed = discord.Embed(
                title=":x: unban error", 
                description = "**Use the command so:\n**```" + 
                str(self.prefix) + "unban name```"
                ))        

    def ago2(self, x):
        if (str(x).split("-")[0]) != (str(datetime.datetime.now()).split("-")[0]):
            res = x.split(" ")[0]
        elif str(x).split(" ")[0] == str(datetime.datetime.now()).split(" ")[0]:
            res = str(x.split(" ")[1]).split(".")[0]
            res = res.split(":")[0] + ":" + res.split(":")[1]  + " :new:"
        elif (str(x).split("-")[2]) != (str(datetime.datetime.now()).split("-")[2]):
            res = str(x).split(" ")[0]
            res = str(res.replace(res.split("-")[0],"")).replace("-","",1)
        return res

    def flag_umwandler(self, country, gewollter_user):
        countrys = [
            "Kanada", "USA", "Germany", "Latvia",
            "Czechia", "austria", "russia", "Ukraine",
            "United Kingdom","india","China","Switzerland"
            ]
        flaggen = [
            "ca","us","de","lv","cz",
            "au","ru","ua","gb","in",
            "cn","ch"
        ]
        for value in range(len(countrys)):
            if countrys[value].lower() == gewollter_user["country"].lower():
                return str(":flag_") + flaggen[value].lower() + str(": ")
        if len(country) > 10:
            for value in range(len(country)):
                if country[value].lower() > 10:
                    country[value] = ""
            return str("_") + country + str("..._:")
        return str("_") + country + str("_:")

    async def user_anzeiger(self, message, gewollter_user_id, react_or_not, user):
        copied_acc_2 = self.benutzer
        gewollter_user = {}
        try:
            for value56 in self._users:
                if int(value56["id"]) == int(gewollter_user_id):
                    if "banned" not in value56["role"] and "deleted" not in value56["role"]:
                        gewollter_user = value56
        except: pass
        if gewollter_user == {}:
            for value42 in self._users:
                if str(value42["name"]) == str(gewollter_user_id):
                    if "banned" not in value42["role"] and "deleted" not in value42["role"]:
                        gewollter_user = value42
        if gewollter_user != {}:
            flag = self.flag_umwandler(gewollter_user["country"], gewollter_user)
            
            user_posts = []
            for value in self.posts:
                if value["user id"] == gewollter_user["id"]:
                    if value["status"] == "normal" or copied_acc_2 == gewollter_user: 
                        user_posts.append({
                            "created":value["created"],
                            "id":value["post id"],
                            "name":value["name"],
                            "views":value["views"],
                            "datetime":float(value["datetime"])
                        })
            
            user_posts.sort(key=lambda d: int(str(d["datetime"]).split(".")[0]), reverse=True)

            orig_user_posts = ""

            for value in range(0, len(user_posts)):
                mt = ""
                if value == 0 and copied_acc_2 != None:
                    mt = ":arrow_forward: "
                orig_user_posts += str(
                    "-----------------\n**" + str(mt) + str(user_posts[value]["name"]) +      
                    "**\n" + str(user_posts[value]["views"]) + " views | " +
                    str(self.ago2(str(user_posts[value]["created"]))) + "\n"
                )
            sub_status = " :white_circle: **[subscribe]**"
            try:
                if str(copied_acc_2["id"]) in str(gewollter_user["subscribers"]):
                    sub_status = " :blue_circle: **[unsubscribe]**"
            except: sub_status = "**X**"

            stat = ""

            if "premium" in gewollter_user["role"]:
                stat += gewollter_user["premium_emoji"]
            if "tester" in gewollter_user["role"]:
                stat += ":microscope:"
            if "hodenkobold" in gewollter_user["role"]:
                stat += ":alien:"
            if "Supporter" in gewollter_user["role"]:
                stat += ":man_technologist:"
            if "T-team" in gewollter_user["role"]:
                stat += ":student:"
            if "verified" in gewollter_user["role"]:
                stat += ":heavy_check_mark:"
            if "X-team" in gewollter_user["role"]:
                stat += ":crown:"
            if "manager" in gewollter_user["role"]:
                stat  += ":chart_with_upwards_trend:"
            if "moderator" in gewollter_user["role"]:
                stat += "::shield:"
            if "owner" in gewollter_user["role"]:
                stat += ":fleur_de_lis:"
            if "user" in gewollter_user["role"]:
                stat += ":levitate:"
            copied_acc = gewollter_user
            if orig_user_posts == "":
                orig_user_posts = "no posts yet\n"
            em = discord.Embed(
                title = str(flag) + "**" + gewollter_user["name"] + "**",
                description =
                ":levitate:" + str(len(gewollter_user["subscribers"])) + " subscribers" +
                "\n\n" + sub_status + gewollter_user["description"] + 
                "\n\n**Money:** " + str(gewollter_user["money"]) + "⍫\n\n**Posts:**\n" + 
                orig_user_posts + "\n" +
                "badge/s: " + str(stat) + "\ncheck out " + self.prefix + "dev-profil " + gewollter_user["name"] + " for some dev info",
            ).set_footer(text = "Account created on " + str(gewollter_user["datetime"].split(" ")[0]))
            if gewollter_user["premium-color"] != "":
                em.color = int(gewollter_user["premium-color"])
            user_mes = await message.channel.send(embed = em)
            if sub_status != "**X**":
                if sub_status == " :blue_circle: **[unsubscribe]**":
                    await user_mes.add_reaction("🔵")
                else:
                    await user_mes.add_reaction("⚪")
            if orig_user_posts != "no posts yet\n" and sub_status != "**X**":
                await user_mes.add_reaction("🔺")
                await user_mes.add_reaction("🔻")
            if copied_acc_2 != None:
                if react_or_not == "message":
                    self.waiting_list.append({
                        "reason":"user",
                        "completed":"false",
                        "extra":[copied_acc_2["id"], user_mes.id , message.author.id ,user_posts, 0, True, gewollter_user["id"]]
                    })
                elif react_or_not == "react":
                    self.waiting_list.append({
                        "reason":"user",
                        "completed":"false",
                        "extra":[copied_acc_2["id"], user_mes.id , user.id ,user_posts, 0, True, gewollter_user["id"]]
                    })
                    gewollter_user = copied_acc
                self.waiting_list.append({
                    "reason":"subscribe",
                    "completed":"false",
                    "extra":[copied_acc["id"], user_mes.id]
                })
        else: await message.channel.send(embed = discord.Embed(
            title = ":x: User cann't be showed",
            description = "This user was doesn't exist or was banned or the user deleted it account.",
            color = 15158332
        ))

    async def daily_update(self, message):
        p_c_m = await message.channel.send("**Starting check premium... 0%**")
        x = 0
        try: heute_datum = message.content.split(" ")[1]
        except: heute_datum = str(datetime.datetime.now()).split(" ")[0]
        premium_removed = ""
        for value in self._users:
            x += 1
            if x == len(self._users) / 2:
                await p_c_m.edit(content = "**Checking premium... 50%**")
            if "premium" in value["role"]:
                roles = value["role"].split("*")
                for value1 in roles:
                    if value1.startswith("premium"):
                        ablauf_datum = value1.split(":")[1]
                        if ablauf_datum != "permanent":
                            if str(ablauf_datum) == heute_datum:
                                premium_removed += value["id"] + ", "
                                value["role"] = value["role"].replace("*premium:" + str(ablauf_datum), "")
                                value["description"] = ""
                                value["premium-color"] = ""
                                for value2 in range(len(self._users)):
                                    if self._users[value2]["id"] == value["id"]:
                                        self._users[value2] = value
        await p_c_m.edit(content = "**Checking premium finished - 100%**")
        await message.channel.send(embed = discord.Embed(
            title = "Removed premium",
            description = "Ids:\n" + 
            premium_removed
        ))
        p_c_m = await message.channel.send("**Starting check bans... 0%**")
        x = 0
        bans_removed = ""
        for value in self._users:
            x += 1
            if x == len(self._users) / 2:
                await p_c_m.edit(content = "**Checking bans... 50%**")
            if "banned" in value["role"]:
                roles = value["role"].split("*")
                for value1 in roles:
                    if value1.startswith("banned"):
                        ablauf_datum = value1.split(":")[1]
                        if ablauf_datum != "permanent":
                            if str(ablauf_datum) == heute_datum:
                                bans_removed += value["id"] + ", "
                                value["role"] = value["role"].replace("*banned:" + str(ablauf_datum), "")
                                for value2 in range(len(self._users)):
                                    if self._users[value2]["id"] == value["id"]:
                                        self._users[value2] = value
                                        self._users[value2]["notif"].append({
                                            "message":"Today is your unban date, you are unbanned now.",
                                            "readen":False,
                                            "about":[str(datetime.datetime.now())]
                                        })
        await p_c_m.edit(content = "**Checking bans finished - 100%**")
        await message.channel.send(embed = discord.Embed(
            title = "Removed bans",
            description = "Ids:\n" + 
            bans_removed
        ))
        mes=await message.channel.send("**Sending notification messages... 0%**")
        for value in self._users:
            counter = 0
            for value3 in value["notif"]:
                if value3["readen"] == False:
                    counter += 1
            if counter > 0:
                for value2 in value["account-users"]:
                    try:
                        begrusung = ["Hey","Hello","Hi"][random.randint(0,2)]
                        await (await client.fetch_user(int(value2))).send("**" + str(begrusung) + ", you've " + str(counter) + " unreaden notifications.:smile:**")
                    except: pass
            if self._users.index(value) == len(self._users) / 2:
                await mes.edit(content="**Sending notification messages... 50%**")
        await mes.edit(content="**Finished sending notification messages! 100%**")
        for x in range(10):
            for value in self.waiting_list:
                if value["reason"] != "activate-account" and value["reason"] != "password":
                    self.waiting_list.remove(value)
        await message.channel.send("**Cleared waiting list.**")

    async def add_perm(self, message):
        try:
            user_gefunden = False
            for value in range(len(self._discord_users)):
                if str(self._discord_users[value["name"]]) == str(message.content.split(" ")[1]):
                    try: 
                        self._discord_users[value]["authorization"][message.content.split(" ")[3]] = bool(
                            message.content.split[5]
                            )
                        await message.channel.send(":white_check_mark: **Succefull runned your command.**")
                        user_gefunden = True
                    except: 
                        await message.channel.send(
                            ":x: **Use the command so: " + 
                            self.prefix + "add-perm username" +
                            " permission_name True/False.**"
                        )
            if user_gefunden == False:
                await message.channel.send(":x:**User wasn't found.**")
        except:
            await message.channel.send(
                ":x: **Use the command so: " + 
                self.prefix + "add-perm username" +
                " permission_name True/False.**"
            )

    async def subscribe(self, reaction, gewollter_user, val_status):
        copied_user = self.benutzer
        if copied_user["id"] != gewollter_user["id"]:
            if val_status == "white":
                if int(copied_user["id"]) in gewollter_user["subscribers"]:
                    gewollter_user["subscribers"].remove(int(copied_user["id"]))
                    copied_user["money"] = int(copied_user["money"]) - 9
                    mes = await reaction.message.channel.send("**Someone unsubscribed of " + gewollter_user["name"] + ".**")
                    
                    for value1 in self.posts:
                        if value1["user id"] == copied_user["id"]:
                            value1["reputation"] += 10
                else:
                    gewollter_user["subscribers"].append(int(copied_user["id"]))
                    mes = await reaction.message.channel.send("**Someone subscribed to " + gewollter_user["name"] + ".**")
                    ok = True
                    for value in gewollter_user["f_notif"]:
                        if value["message"] == copied_user["name"] + " subscribed to you. | +10⍫":
                            ok = False
                    if ok == True:
                        gewollter_user["f_notif"].append({
                            "message":copied_user["name"] + " subscribed to you. | +10⍫",
                            "readen":False,
                            "about":[str(datetime.datetime.now())]
                        })
                    gewollter_user["money"] = int(gewollter_user["money"]) + 10
            elif val_status == "blue":
                if int(copied_user["id"]) in gewollter_user["subscribers"]:
                    gewollter_user["subscribers"].remove(int(copied_user["id"]))
                    mes = await reaction.message.channel.send("**Someone unsubscribed of " + gewollter_user["name"] + ".**")
                    gewollter_user["money"] = int(gewollter_user["money"]) - 10
                else:
                    gewollter_user["money"] = int(gewollter_user["money"]) + 10
                    gewollter_user["subscribers"].append(int(copied_user["id"]))
                    mes = await reaction.message.channel.send("**Someone subscribed to " + gewollter_user["name"] + ".**")
            
            for value in range(len(self._users)):
                if self._users[value]["id"] == copied_user["id"]:
                    self._users[value] = copied_user
            await asyncio.sleep(3)
            await mes.delete()
        else:
            mes = await reaction.message.channel.send("**You can't subscribe to yourself.**")
            await asyncio.sleep(3)
            await mes.delete()

    async def dev_user(self, der_user, message):
        mod_extra = ""
        if self.benutzer != None:
            if "X-team" in self.benutzer["role"]:
                mod_extra = (
                    "\n**password:** " + str(pwer.encode(der_user["password"])) + "\n**email: **" +
                    str(der_user["email"]) + "**\naccount-user:**\n"+ str(der_user["account-users"]) +
                    "\n**creator: ** " + der_user["discord id"] + "\n**birthday: **" + der_user["birthday"]
                )

        await message.channel.send(embed=discord.Embed(
            title = "DEV-INFO",
            description = ("**User ID: **" + der_user["id"] + "\n**Liked posts: **" + 
            str(len(der_user["liked-post"])) + "\n**disliked posts: **" + 
            str(len(der_user["disliked-post"])) + "\n**IP**: " + der_user["ip"] + 
            "\n**feedback notification count**: " + str(len(der_user["f_notif"])) + 
            str(mod_extra))
        ))

    async def weather_lpz(self, message):
        day = message.content.replace(self.prefix + "weather ","")
        try:
            if day.lower().startswith("tod"):
                day = 0
            elif day.lower().startswith("tom"):
                day = 1
        except:
            pass
        link = "https://www.wetter.com/wetter_aktuell/wettervorhersage/16_tagesvorhersage/deutschland/leipzig/DE0006194.html"
        response = requests.get(link, verify=False)
        val_bytes = response.text.encode("utf-8")
        xml = html.fromstring(val_bytes)
        res = ""
        xm = xml.xpath(".//div[@class='text--white date']")[day]
        xm2 = xml.xpath(".//span[@class='temp-max']")[day]
        xm3 = xml.xpath(".//span[@class='temp-min']")[day]
        xm4 = xml.xpath(".//div[@class='weather-state']")[day]
        xm5 = xml.xpath(".//dl/dd")[2]
        res += "-" * 20 + " WEATHER " + "-" * 20 
        res += "\nMax: " + html.tostring(xm2).decode("utf-8").split(">")[1].split("<")[0].replace("&#176;","°C").replace("\n","")
        res += "\nMin: " + html.tostring(xm3).decode("utf-8").split(">")[1].split("<")[0].replace("&#176;","°C").replace(" / ","").replace("\n","")
        res += "\nWetter: " + html.tostring(xm4).decode("utf-8").split(">")[1].split("<")[0].replace("\n","").replace("            ","").replace("&#173;",", ").replace("&#246;","ö")
        res += "\n" + html.tostring(xm5).decode("utf-8").split(">")[1].split("<")[0].replace("\n","").replace("                ","").replace("&#176;","°C").replace("&#252;","ü") + "\n"
        res += "-" * 20 + " WEATHER " + "-" * 20 + "\n"
        await message.channel.send(embed = discord.Embed(
            title = "WEATHER " + html.tostring(xm).decode("utf-8").split(">")[1].split("<")[0].capitalize(),
            description = "**" + res + "**"
        ))

    async def werbung(self, message):
        if random.randint(1,10) == 3:
            if self.ads:
                the_ad = self.ads[0]["ad"]
                self.ads[0]["views"] += 1
                if int(self.ads[0]["max_views"]) < int(self.ads[0]["views"]): del self.ads[0]
                else:
                    colorr = self.ads[0]["color"]
                    v_c = self.ads[0]["views"]
            else:
                the_ad = "**Buy premium now.\nmore infos -> " + self.prefix + "premium**"
                v_c = "-"
                colorr = 10181046
            await message.channel.send(embed = discord.Embed(
                title = "AD",
                description = the_ad,
                color = colorr
            ).set_footer(text = str(v_c) + " views"))

    async def add_ad(self, message):
        try:
            new_ad = message.content.replace(self.prefix + "add-ad " + message.content.split(" ")[1] + " ","")
            aufrufe = message.content.split(" ")[1]
            try: color = message.content.split("#")[1]
            except: color = 0
            self.ads.append({
                "max_views":int(aufrufe),
                "views":0,
                "ad":str(new_ad),
                "color":int(color)
            })
            await message.channel.send(embed = discord.Embed(
                title = "READY",
                description = "Your ad will be deleted, when it reaches " + str(aufrufe) + 
                " views.\n" + "You are the " + str(len(self.ads)) + ". in the ad-queue.",
                color = 3066993
            ))
        except:
            await message.channel.send(embed = discord.Embed(
                title = ":x: AD ERROR",
                description = "**Use the command so:\n**" + self.prefix + "add-ad max-views ad (optional: #color#)",
                color = 15158332
            ))

    async def verify_coder(self, message):
        if self.benutzer != None:
            if self.benutzer["activatet"] == "false":
                code = message.content.split(" ")[1]
                for value in self.waiting_list:
                    if value["reason"]=="activate-account":   
                        extra_list = value["extra"] 
                        try: 
                            nothing = value["versuche"]
                        except: 
                            value["versuche"] = 0 
                        if value["versuche"] < 3:
                            if extra_list[0] == self.benutzer["email"]:
                                if extra_list[1]==code:
                                    value["completed"] = True
                                    self.benutzer["activatet"] = "true"
                                    await message.channel.send(":white_check_mark:**Your email is verified now! :)**")
                                    self.benutzer["notif"].append({
                                        "message":"You verified your email. | +100⍫",
                                        "readen":False,
                                        "about":[str(datetime.datetime.now())]
                                    })
                                    self.benutzer["money"] = int(self.benutzer["money"]) + 100
                                else:
                                    value["versuche"] += 1 
                                    await message.channel.send(":x:The code isn't correct.")
                        else: await message.channel.send(":x:You can't verify your email anymore.")
            else: await message.channel.send(":x:Your email is already verified.")
        else: await self.noaccount_error(message)

    async def dev_info(self, message):
        try:
            post_id = message.content.split("'")[1]
            for value in self.posts:
                if str(value["post id"]) == str(post_id):
                    gewollter_post = value
            extra_info = ""
            if "X-team" in self.benutzer["role"]:
                extra_info += "\nStatus:** " + gewollter_post["status"] + "**"
                extra_info += "\nReputation: **" + gewollter_post["reputation"] + "**"
            if "premium" in self.benutzer["role"]:
                extra_info += "\nReputation: **" + gewollter_post["reputation"] + "**"
            await message.channel.send(embed = discord.Embed(
                title = "DEV-POST-INFO",
                description = "ID: **" + gewollter_post["post id"] + "**\nDatetime: **"
                + gewollter_post["datetime"] + "**"
                + extra_info
            ))
        except:
            await self.notfound_error(message)    

    async def settings(self, message):
        copied_acc = self.benutzer
        des_info = "You can add a description to your channel, if you buy premium. (" + self.prefix + "premium)\n"
        if "premium" in copied_acc["role"]:
            if copied_acc["description"] == "":
                des_info = "You can add a description to your channel with **" + self.prefix + "change-desc**" 
            else:
                des_info = "Your description: " + copied_acc["description"] + "\n"
        await message.channel.send(embed = discord.Embed(
            title = ":nut_and_bolt:Your account settings",
            description = "Account activatet - **" + copied_acc["activatet"] +
            "\n\n**Change your username with **" + self.prefix + "change-username**\n" + 
            "-> Your currently username is " + copied_acc["name"] + "\n-> You can change your username" +
            " just once in 3 days\n\n" +
            "Change your password with **" + self.prefix + "change-password**\n\n" +
            "Your birthday: **" + copied_acc["birthday"] + "**\n\n" + des_info +
            "\n\nSafety-mode: **" + str(copied_acc["extra"][0]) + "** \n-> (You can turn on safety-mode with " +
            self.prefix + "safety-mode True/False)\n\nyou can delete your account - **" + self.prefix + "delete-account [password]**" +
            "\n(Just when you created your account with that discord account)",
            color = 0
        ))

    async def change_something(self, message):
        try:
            was = message.content.replace(self.prefix + "change-","")
            if "premium" in self.benutzer["role"]:
                if was.startswith("desc"):
                    if message.content.split("'")[1] == pwer.encode(self.benutzer["password"]):
                        self.benutzer["description"] =  "\n\n" + message.content.split("'")[3]
                        await message.channel.send("**:white_check_mark: Succesfully changed description.**")
                    else:
                        await message.channel.send(embed = discord.Embed(
                            title = ":x: wrong password",
                            description = "You have to use this command so: " + self.prefix +
                            "change-desc 'password' 'new description'",
                            color = 15158332
                        ))
            else:
                if was.startswith("desc"):
                    await message.channel.send(":x: **You need premium to use this command.**")    

            if was.startswith("username"):
                if message.content.split("'")[1] == pwer.encode(self.benutzer["password"]):
                    heute = str(self.benutzer["changed_username"]).split(" ")[0]
                    morgen = str(datetime.datetime.strptime(self.benutzer["changed_username"],self.benutzer["changed_username"]) + datetime.timedelta(days = 1)).split(" ")[0]
                    u_morgen = str( datetime.datetime.strptime(self.benutzer["changed_username"],self.benutzer["changed_username"]) + datetime.timedelta(days = 2)).split(" ")[0]
                    jetzt = str(datetime.datetime.now()).split(" ")[0]
                    username = message.content.split("'")[3]
                    fehler = ""
                    allowed_characters = list(string.ascii_lowercase)
                    try:
                        for value in list(string.ascii_lowercase):
                            allowed_characters.append(value.capitalize())
                        for value in range(len(username)):
                            if username[value] not in allowed_characters:
                                fehler += "Your username contains not allowed characters. -> " + username[value] + "\n"
                        if username == "":
                            fehler += "Your username can't be empty.\n"
                        if len(username)>16:
                            fehler += "Your username can't be longer than 12 characters.\n"
                        if "globaltube" in str(username):
                            fehler += "You can't use globaltube in your name.\n"
                        for value in self._users:
                            if value["name"] == str(username):
                                fehler = "This username was already used.\n"
                    except:
                        fehler = "Please enter an real username.\n"
                    not_ok = True
                    if heute == jetzt:
                        not_ok = False
                    if morgen == jetzt:
                        not_ok = False
                    if u_morgen == jetzt:
                        not_ok = False
                    if not_ok == True:
                        if fehler == "":
                            self.benutzer["name"] = message.content.split("'")[3]
                            self.benutzer["changed_username"] = str(datetime.datetime.now()).split(" ")[0]
                            await message.channel.send("**:white_check_mark: Succesfully changed username.**")
                        else:
                            await message.channel.send(embed = discord.Embed(
                                title = ":x: Cann't change username",
                                description = "Reason/s:\n" + fehler,
                                color = 15158332  
                            ))      
                    else:
                        await message.channel.send("**:x: You can change your name just once in 3 days.**")
                else:
                    await message.channel.send(embed = discord.Embed(
                        title = ":x: wrong password",
                        description = "You have to use this command so: " + self.prefix +
                        "change-desc 'password' 'new username'",  
                        color = 15158332
                    ))      

            elif was.startswith("password"):
                if message.content.split("'")[1] == pwer.encode(self.benutzer["password"]):
                    self.benutzer["password"] == pwer.decode(message.content.split("'")[3])
                    await message.delete()
                    await message.channel.send("**:white_check_mark: Succesfully changed password.**")
                else:
                    await message.channel.send(embed = discord.Embed(
                        title = ":x: wrong password",
                        description = "You have to use this command so: " + self.prefix +
                        "change-desc 'password' 'new password'",
                        color = 15158332
                    ))
        except:
            await message.channel.send(embed = discord.Embed(
                title = ":x: Error",
                description = "You have to use this command so: " + self.prefix +
                "change-[] 'password' '[]'",
                color = 15158332
            ))

    async def raw_user(self, message):
        for value in self._users:
            try:
                if message.content.split("'")[1] == value["name"] or \
                    message.content.split("'")[1] == value["id"]:
                    await message.channel.send(str(value))
            except:
                if message.content.split(" ")[1] == value["name"] or \
                    message.content.split(" ")[1] == value["id"]:
                    await message.channel.send(str(value))
    
    async def change_rep(self, message):
        try:
            for i in self.posts:
                if i["post id"] == message.content.split(" ")[1]:
                    i["reputation"] = message.content.split(" ")[2]
            await message.channel.send(":white_check_mark: **Changed reputation from the post " + message.content.split(" ")[1] + " to " + message.content.split(" ")[2] + ".**")
        except: await message.channel.send(":x: **Post wasn't found.**")

    #reaction-functions 

    async def subscribe_react(self, reaction, user):
        for value in self.waiting_list:
            if str(value["reason"]) == "subscribe":
                if str(reaction.message.id) == str(value["extra"][1]):
                    for value1 in self._users:
                        if value["extra"][0] == value1["id"]:
                            if reaction.emoji == "🔵":
                                await self.subscribe(reaction, value1, "blue")
                                await reaction.message.remove_reaction("🔵", user)
                            elif reaction.emoji == "⚪":
                                await self.subscribe(reaction, value1, "white")
                                await reaction.message.remove_reaction("⚪", user)

    async def report_post(self, reaction, user):
        if self.benutzer != None:
            for value in self.waiting_list:
                if str(value["reason"]) == "post_add":
                    if str(reaction.message.id) == str(value["extra"][1]):
                        for value1 in self.posts:
                            if value["extra"][2] == value1["post id"]:
                                await reaction.message.remove_reaction("❗", user)
                                if self.discord_user["authorization"]["report"] == True:
                                    await client.get_channel(817906575128789003).send(
                                        embed = discord.Embed(
                                            title = "Reported post :warning:",
                                            description = "**Post Id:\n**" + str(value1["post id"]) +
                                            "\n**Post:**\n_" + str(value1["name"]) + "_\n" + str(value1["content"]) +
                                            "**\nReporter id:\n**" + str(user.id) + "**\nUser Id**:\n" + str(value1["user id"])
                                        ))
                                    await reaction.message.channel.send("**Reported post.**")
                                    self.discord_user["authorization"]["report"] = False
                                    await asyncio.sleep(60*10)    
                                    self.discord_user["authorization"]["report"] = True            
                                else:
                                    await reaction.message.channel.send(
                                        ":x: **You can only report once in 10 minutes.**"
                                        )

    async def user_anzeige_edit(self, reaction, user):
        copied_acc = self.benutzer
        counter = 0
        for value in self.waiting_list:
            if value["reason"] == "user":
                if value["extra"][0] == copied_acc["id"]:
                    if str(reaction.message.id) == str(value["extra"][1]):        
                        if str(value["extra"][2]) == str(user.id):
                            if counter == 0:
                                for value57 in self._users:
                                    if value57["id"] == value["extra"][6]:
                                        gewollter_user = value57
                                        break
                                flag = self.flag_umwandler(gewollter_user["country"], gewollter_user) 

                                user_posts = []
                                for value3 in self.posts:
                                    if value3["user id"] == gewollter_user["id"]:   
                                        if value3["status"] == "normal" or copied_acc == gewollter_user:  
                                            user_posts.append({
                                                "created":value3["created"],
                                                "id":value3["post id"],
                                                "name":value3["name"],
                                                "views":value3["views"],
                                                "datetime":float(value3["datetime"])      
                                            })

                                if reaction.emoji == "🔻":
                                    if value["extra"][4] < len(value["extra"][3]) - 1:
                                        value["extra"][4] += 1
                                    await reaction.message.remove_reaction("🔻", user)
                                elif reaction.emoji == "🔺":
                                    if value["extra"][4] > 0:
                                        value["extra"][4] -= 1
                                    await reaction.message.remove_reaction("🔺", user)

                                user_posts.sort(key=lambda d: int(str(d["datetime"]).split(".")[0]), reverse=True)

                                orig_user_posts = ""

                                for value2 in range(len(user_posts)):
                                    test = ""
                                    if value2 == value["extra"][4]:
                                        test = ":arrow_forward: "
                                    orig_user_posts += str(
                                        "-----------------\n**" + str(test) + str(user_posts[value2]["name"]) +
                                        "**\n" + str(user_posts[value2]["views"]) + " views | " +
                                        str(self.ago2(str(user_posts[value2]["created"]))) + "\n"
                                    )
                                sub_status = " :white_circle: **[subscribe]**"
                                if str(copied_acc["id"]) in str(gewollter_user["subscribers"]):
                                    sub_status = " :blue_circle: [unsubscribe]"

                                stat = ""

                                if "premium" in gewollter_user["role"]:
                                    stat += gewollter_user["premium_emoji"]
                                if "tester" in gewollter_user["role"]:
                                    stat += ":microscope:"
                                if "hodenkobold" in gewollter_user["role"]:
                                    stat += ":alien:"
                                if "Supporter" in gewollter_user["role"]:
                                    stat += ":man_technologist:"
                                if "T-team" in gewollter_user["role"]:
                                    stat += ":student:"
                                if "verified" in gewollter_user["role"]:
                                    stat += ":heavy_check_mark:"
                                if "X-team" in gewollter_user["role"]:
                                    stat += ":crown:"
                                if "manager" in gewollter_user["role"]:
                                    stat  += ":chart_with_upwards_trend:"
                                if "moderator" in gewollter_user["role"]:
                                    stat += "::shield:"
                                if "owner" in gewollter_user["role"]:
                                    stat += ":fleur_de_lis:"
                                if "user" in gewollter_user["role"]:
                                    stat += ":levitate:"
                                copied_acc = gewollter_user
                                if orig_user_posts == "":
                                    orig_user_posts = "no posts yet\n"
                                em = discord.Embed(
                                title = str(flag) + "**" + gewollter_user["name"] + "**",
                                description =
                                ":levitate:" + str(len(gewollter_user["subscribers"])) + " subscribers" +
                                "\n\n" + sub_status + gewollter_user["description"] + 
                                "\n\n**Money:** " + str(gewollter_user["money"]) + "⍫\n\n**Posts:**\n" + 
                                orig_user_posts + "\n" +
                                "badge/s: " + str(stat) + "\ncheck out " + self.prefix + "dev-profil " + gewollter_user["name"] + " for some dev info",
                                ).set_footer(text = "Account created on " + str(gewollter_user["datetime"].split(" ")[0]))
                                if gewollter_user["premium-color"] != "":
                                    em.color = int(gewollter_user["premium-color"])
                                await reaction.message.edit(embed = em)
                                if value["extra"][5] == True:
                                    await reaction.message.add_reaction("✴️") 
                                    value["extra"][5] = False

                                self.waiting_list.append({
                                    "reason":"user",
                                    "completed":"false",
                                    "extra":[copied_acc["id"], reaction.message.id , user.id ,user_posts, 0, True, gewollter_user["id"]]
                                })
                                counter += 1

    async def search_nav(self, reaction, user):
        for value in self.waiting_list:
            extra_list = value["extra"]
            if str(extra_list[1]) == str(reaction.message.id):
                if str(extra_list[0]) == str(user.id):
                    try:
                        results = extra_list[2]
                        test = -1
                        if reaction.emoji == "👆":
                            await reaction.message.remove_reaction("👆",user)
                            extra_list[4] -= 1
                        elif reaction.emoji == "👇":
                            await reaction.message.remove_reaction("👇",user)
                            extra_list[4] += 1
                        self.searching_result_message = ""
                        results2 = []
                        for value in results:
                            test += 1
                            weiter = True
                            for value2 in results2:
                                if value2 == value:
                                    weiter = False
                            if weiter == True:
                                results2.append(value)
                                if test<50:
                                    if extra_list[4] == test:
                                        pfeil = ":arrow_forward: "
                                    else: pfeil = ""
                                    if extra_list[3] == "post":
                                        self.searching_result_message += (str(pfeil) + ":speech_balloon: " + str(value["name"] + "**\n⠀" + str(value["views"]) + " views**\n"))
                                    else: self.searching_result_message += (str(pfeil) + ":levitate: " + str(value["name"] + "\n**⠀" + str(value["subscribers"]) + "⠀subscribers**\n"))
                        em = discord.Embed(title="Searching results",description="**" + str(self.searching_result_message) + "**\nno more results")                            
                        await reaction.message.edit(embed=em)
                    except:
                        pass

    async def _start(self, reaction, user):
        user_count = 0
        for value1 in self.waiting_list:
            global extra_in_extra_list, extra_list
            extra_list = value1["extra"]
            if str(extra_list[1]) == str(reaction.message.id):
                if str(extra_list[0]) == str(user.id):
                    extra_in_extra_list = extra_list[2]
                    await reaction.message.remove_reaction("👊",user)
                    extra_in_extra_list = extra_in_extra_list[extra_list[4]]
                    if extra_list[3] == "user":
                        await self.user_shower(reaction, user, user_count)
                    elif extra_list[3] == "post":
                        await self.post_shower(reaction, user)
    
    async def user_shower(self, reaction, user, user_count):
        for value4 in self._users:
            if value4["id"] == extra_in_extra_list["id"]:
                if user_count < 1:
                    await self.user_anzeiger(reaction.message, value4["id"], "react", user)
                    user_count += 1
    
    async def post_shower(self, reaction, user):        
        for value4 in self.posts:
            if value4["post id"] == extra_in_extra_list["id"]:
                await self.post_anzeiger(reaction.message, value4, user)
    
    async def post_zeiger(self, message, link):
        copied_user = self.benutzer
        value4 = [i for i in self.posts if i["post id"]==message.content.split(" ")[1]]
        if value4[0]["status"] == "normal" or copied_user["id"] == value4[0]["user id"]:
            value4 = value4[0]
            if link == True: value4["reputation"] += random.randint(10,20)
            clock = str(value4["created"]).split(" ")[0]
            for value7 in self._users:
                if value7["id"] == value4["user id"]:
                    user_name = value7
            sub_mes = "\n**[subscribed]**"
            try:
                if int(copied_user["id"]) in user_name["subscribers"]:
                    sub_mes = ""
            except:sub_mes = ""
            name_von_user = user_name["name"]
            user_subs = str(len(user_name["subscribers"]))
            try:
                if "banned" in user_name["role"] or "deleted" in user_name["role"]:
                    name_von_user = ":x: not existing user"
                    user_subs = "No"
            except: pass
            em_content = str(
                "**" + value4["name"] + "\n----------------\n**" + str(value4["content"]) + 
                "**\n----------------\n" + str(len(value4["likes"])) + "👍" + 
                str(len(value4["dislikes"])) + "👎\n----------------\n**" + 
                str(value4["views"]) + " views\n" + str(clock) + "**\n----------------\n" + 
                name_von_user + "**\n" + user_subs + " Subscribers" + 
                str(sub_mes) + "\n**----------------**\n"
            )
            em = discord.Embed(
                title="💬 post " + value4["post id"],
                description=str(em_content),
                color = 0
            )
            mes=await message.channel.send(embed=em)
            await mes.add_reaction("👍")
            await mes.add_reaction("👎")
            if user_subs != "No":
                await mes.add_reaction("🕴️")
            await mes.add_reaction("❗")
            await mes.add_reaction("💬")
            if copied_user != None:
                if len([i for i in copied_user["history"] if i==value4["post id"]]) < 3:
                    value4["views"] = int(value4["views"]) + 1
                value4["reputation"] = int(value4["reputation"]) - 1
                copied_user["history"].append(value4["post id"])
                self.waiting_list.append({
                    "reason":"post_add",
                    "completed":"false",
                    "extra":[str(message.author.id),str(mes.id),str(value4["post id"]),1,True]
                })
                for value in range(len(self._users)):
                    if self._users[value]["id"] == copied_user["id"]:
                        self._users[value] = copied_user
        else: await message.channel.send(":x:**This post was not found or deleted or the status was set to privat**")
        await self.werbung(message)

    async def post_anzeiger(self, message, value4, user):
        copied_user = self.benutzer
        clock = str(value4["created"]).split(" ")[0]
        for value7 in self._users:                
            if value7["id"] == value4["user id"]:
                    user_name = value7
        sub_mes = "\n**[subscribed]**"
        try:
            if int(copied_user["id"]) in user_name["subscribers"]:
                sub_mes = ""
        except:sub_mes = ""
        name_von_user = user_name["name"]
        user_subs = str(len(user_name["subscribers"]))
        try:
            if "banned" in user_name["role"] or "deleted" in user_name["role"]:
                name_von_user = ":x: not existing user"
                user_subs = "No"
        except: pass
        em_content = str(
            "**" + value4["name"] + "\n----------------\n**" + str(value4["content"]) + 
            "**\n----------------\n" + str(len(value4["likes"])) + "👍" + 
            str(len(value4["dislikes"])) + "👎\n----------------\n**" + 
            str(value4["views"]) + " views\n" + str(clock) + "**\n----------------\n" + 
            name_von_user + "**\n" + user_subs + " Subscribers" + 
            str(sub_mes) + "\n**----------------**\n"
        )
        em = discord.Embed(
            title="💬 post " + value4["post id"],
            description=str(em_content),
            color = 0
        )
        mes=await message.channel.send(embed=em)
        await mes.add_reaction("👍")
        await mes.add_reaction("👎")
        if user_subs != "No":
            await mes.add_reaction("🕴️")
        await mes.add_reaction("❗")
        await mes.add_reaction("💬")
        if copied_user != None:
            if len([i for i in copied_user["history"] if i==value4["post id"]]) < 3:
                value4["views"] = int(value4["views"]) + 1
            value4["reputation"] = int(value4["reputation"]) - 1
            copied_user["history"].append(value4["post id"])
            self.waiting_list.append({
                "reason":"post_add",
                "completed":"false",
                "extra":[str(user.id),str(mes.id),str(value4["post id"]),1,True]
            })
            for value in range(len(self._users)):
                if self._users[value]["id"] == copied_user["id"]:
                    self._users[value] = copied_user
        await self.werbung(message)

    async def liker(self, reaction, user):
        copied_user = self.benutzer
        if self.benutzer != None:
            for value in self.waiting_list:
                if str(value["reason"]) == "post_add":
                    if str(reaction.message.id) == str(value["extra"][1]):
                        for value1 in self.posts:
                            if value["extra"][2] == value1["post id"]: 
                                await reaction.message.remove_reaction("👍",user)
                                somebool = False
                                for value3 in value1["likes"]:
                                    if value3 == self.benutzer["id"]:
                                        somebool = True
                                for value4 in self._users:
                                    if value4["id"] == value1["user id"]:
                                        gewollter_user = value4
                                if somebool == False:
                                    value1["likes"].append(str(self.benutzer["id"]))
                                    self.benutzer["liked-post"].append(str(value1["post id"]))
                                    try:
                                        value1["dislikes"].remove(str(self.benutzer["id"]))
                                        self.benutzer["disliked-post"].remove(str(value1["post id"]))
                                    except:
                                        pass
                                    if gewollter_user["id"] != value1["user id"] or str(gewollter_user["id"]) != "759031129914474556":
                                        for value5 in range(len(self._users)):
                                            if self._users[value5]["id"] == gewollter_user["id"]:
                                                ok = False
                                                for value41 in gewollter_user["f_notif"]:
                                                    if value41["message"] == (copied_user["name"] + " liked your post " + str(value1["name"]) + ". +5⍫"):
                                                        ok = True
                                                if ok == False:
                                                    self._users[value5]["f_notif"].append({
                                                    "message":copied_user["name"] + " liked your post " + str(value1["name"]) + ". +5⍫",
                                                    "readen":False,
                                                    "about":[str(datetime.datetime.now()), user.id]
                                                    })
                                    gewollter_user["money"] = int(gewollter_user["money"]) + 5
                                    value1["reputation"] = int(value1["reputation"]) + 8
                                    mes=await reaction.message.channel.send("**" + str(user) + " liked the post**")
                                else:
                                    gewollter_user["money"] = int(gewollter_user["money"]) - 5
                                    value1["likes"].remove(str(self.benutzer["id"]))
                                    self.benutzer["liked-post"].remove(str(value1["post id"]))
                                    value1["reputation"] = int(value1["reputation"]) - 9
                                    mes=await reaction.message.channel.send("**" + str(user) + " removed his like**") 
                                await asyncio.sleep(3)
                                await mes.delete()
        else:
            await reaction.message.channel.send("**" + str(user) + ", please login or register first.**")

    async def disliker(self, reaction, user):
        copied_acc = self.benutzer
        if self.benutzer != None:
            for value in self.waiting_list:
                if str(value["reason"]) == "post_add":
                    if str(reaction.message.id) == str(value["extra"][1]):
                        for value1 in self.posts:
                            if value["extra"][2] == value1["post id"]: 
                                await reaction.message.remove_reaction("👎",user)
                                somebool = False
                                for value52 in self._users:
                                    if value52["id"] == value1["user id"]:
                                        gewollter_user = value52 
                                for value3 in value1["dislikes"]:
                                    if value3 == self.benutzer["id"]:
                                        somebool = True
                                if somebool == False:
                                    value1["dislikes"].append(str(self.benutzer["id"]))
                                    self.benutzer["disliked-post"].append(str(value1["post id"]))
                                    try:
                                        value1["likes"].remove(str(self.benutzer["id"]))
                                        self.benutzer["liked-post"].remove(str(value1["post id"]))
                                    except:
                                        pass
                                    mes=await reaction.message.channel.send("**" + str(user) + " disliked the post**")
                                    value1["reputation"] = int(value1["reputation"]) - 9 
                                    gewollter_user["money"] = int(gewollter_user["money"]) - 6
                                else:
                                    value1["dislikes"].remove(str(self.benutzer["id"]))
                                    self.benutzer["disliked-post"].remove(str(value1["post id"]))
                                    gewollter_user["money"] = int(gewollter_user["money"]) + 5
                                    value1["reputation"] = int(value1["reputation"]) + 8
                                    mes=await reaction.message.channel.send("**" + str(user) + " removed his dislike**")
                                await asyncio.sleep(3)
                                await mes.delete()
        else:
            await reaction.message.channel.send("**" + str(user) + ", please login or register first.**") 

    async def user_shower2(self, reaction, user):
        await reaction.message.remove_reaction("🕴️",user)
        for value in self.waiting_list:
            if str(value["reason"]) == "post_add":
                if str(user.id) == str(value["extra"][0]):
                    if str(reaction.message.id) == str(value["extra"][1]):
                        for value1 in self.posts:
                            if value1["post id"] == str(value["extra"][2]):
                                await self.user_anzeiger(reaction.message, value1["user id"], "react", user)
                            
    async def starter_down(self, reaction, user):
        for value in self.waiting_list:
            if str(value["reason"]) == "post_add":
                if str(reaction.message.id) == str(value["extra"][1]):
                    await reaction.message.remove_reaction("⬇",user)
                    if str(user.id) == str(value["extra"][0]):
                        if "start" == value["extra"][3]:
                            in_need_values = [self.waiting_list, self._users, self.posts, self.user_id, self.post_id ,self.benutzer, self.prefix, self.website_name, self.discord_user]
                            starter = self.starter()
                            self.waiting_list, self._users = await starter.start(reaction.message, in_need_values, user, "react")

    async def user_found_checker(self):
        if self.benutzer != None:
            if self.benutzer["activatet"] == "true":
                return None
            return "**Please activate your account first.**"
        return "**Please login or register first.**"

    async def post_vorbereitung(self, reaction, user):
        copied_acc = self.benutzer
        counter = 0
        for value in self.waiting_list:
            if value["reason"] == "user":
                if value["extra"][0] == copied_acc["id"]:
                    if str(reaction.message.id) == str(value["extra"][1]):
                        if str(value["extra"][2]) == str(user.id):
                            for value2 in self.posts:
                                if str(value["extra"][3][value["extra"][4]]["id"]) == str(value2["post id"]):
                                    if counter == 0:
                                        await self.post_anzeiger(reaction.message, value2 ,user)
                                        await reaction.message.remove_reaction("✴️", user)
                                    counter += 1
                                    

    #|################################ REACTION, MESSAGE, READY ##################################|#

    async def on_ready(self):
        await client.get_channel(817906575128789003).send("**Starting bot...**")
        activity = discord.Game(name="Minecraft")
        await client.change_presence(status=discord.Status.idle, activity=activity)
        res = requests.get("https://geolocation-db.com/json", verify=False).json()
        loc_res = res["country_name"] + ", " + res["state"] + ", " + res["city"] + ", " + res["postal"]
        await client.get_channel(817906575128789003).send(embed=discord.Embed(
            title = "starter details",
            description = "IP:\n**" +
            (socket.gethostbyname(socket.gethostname()))
            + "\n**IPv4:**\n" + 
            str(res["IPv4"])
            + "**\nLocation:**\n" +
            str(loc_res) + "**\nPlatform:**\n"
             + platform.uname().node + "**"
        )) 

    async def on_message(self, message):

        self.discord_user = await self.get_discord_user(message.author.id)
        self.benutzer = await self.get_user_by_id(message.author.id)
        copied_user = self.benutzer
        await self.update_mail(message)

        #start

        if message.author == client.user:
            return

        self.prefix = "$"
        self.wahrung = "⍫"
        banned = False
        in_need_values = [self.waiting_list, self._users, self.posts, self.user_id, self.post_id ,self.benutzer, self.prefix, self.website_name, self.discord_user]

        #navigator
        try:
            if "banned" in copied_user["role"]:
                if message.content.startswith(self.prefix):
                    banned = True
                    await message.channel.send(embed = discord.Embed(
                        title = ":octagonal_sign:You're banned",
                        description = (
                            "**You can't use the bot, because you're banned.** \n" +
                            "Reason:\n```" + self.benutzer["role"].split(":")[2] + 
                            "```\nBanned until:\n```" + self.benutzer["role"].split(":")[1] + 
                            "```\nBanned from:\n```" + self.benutzer["role"].split(":")[3] + "```"
                        ),
                        color = 15158332
                    ).set_footer(
                        text="You can create a unban request with " + 
                        self.prefix + "unban-request [why we should unban you]")
                    )

            if message.content.lower() == self.prefix + "premium":
                await message.channel.send(embed = discord.Embed(
                    title = ":gem:premium-info",
                    description = "**Features:**" +
                    '''
                    → You can set your user color
                    → Your upload cooldown will be set to 60 seconds
                    → You can use emojis in your post names
                    → The chance that your posts will get viral, is a bit higher
                    → You can add your own emoji to the badges
                    → You can add your channel a description
                    → You can use the characters ``` and _*_ in your post 
                    '''
                ).set_footer(text="Just €2,99/Month ($3,60/Month) or €29,99/Permanent"))

            elif message.content.startswith(self.prefix + "unban-request "):
                if "banned" in copied_user["role"]:
                    await client.get_channel(817906575128789003).send(embed=discord.Embed(
                        title = "unban request",
                        description = (
                            "From the user:\n```" + copied_user["name"] + "```\n" +
                            "Unban request content:\n```" + message.content.replace(self.prefix + "unban-request ","") + "```"
                        )
                    ))
                    await message.channel.send(":white_check_mark:**Sent unban request.**")
                else: await message.channel.send(":x:**You cann't create a unban request, without being banned.**")
        except: pass

        if banned == False: await self.new_on_message(message, in_need_values)

    async def new_on_message(self, message, in_need_values):
        self.whitelist = ["701128119402102925"]
        if str(message.author.id) in self.whitelist:
            if self.bot_closed == False or str(message.author.id) == "701128119402102925":
                #link

                link = False
                if message.content.startswith(self.prefix + "link"):
                    link_splitten = message.content.split("/")
                    link = True
                    message.content = self.prefix + link_splitten[1] + " " + link_splitten[2]
                    
                #navigator
                
                if message.content.startswith(self.prefix + "send-data-files"):
                    if self.permission_checker("send_data_files"):
                        await self.send_data_files(message)
                    else: await self.forbidden_error(message)

                if message.content == "discord acc":
                    await message.channel.send(self.discord_user)

                elif message.content.startswith(self.prefix + "tree"):
                    if "X-team" in self.benutzer["role"]:
                        await self.tree(message)
                    else: await self.forbidden_error(message)

                elif message.content.startswith(self.prefix + "set-color"):
                    if "premium" in self.benutzer["role"]:
                        await self.set_account_color(message)
                    else: await self.forbidden_error(message)

                elif message.content == self.prefix + "feedbacks":
                    if "X-team" in self.benutzer["role"]:
                        await message.author.send(file=discord.File('feedbacks.json'))
                    else: await self.forbidden_error(message)

                elif message.content.startswith(self.prefix + "change-rep"):
                    if "X-team" in self.benutzer["role"]: await self.change_rep(message)
                    else: await self.forbidden_error(message)

                elif message.content.startswith(self.prefix + "add-bot-user"):
                    if "X-team" in self.benutzer["role"]:
                        self.whitelist.append(message.content.split(" ")[1])

                elif message.content == self.prefix + "shop":
                    await self.shop(message)

                elif message.content.startswith(self.prefix + "help"):
                    await self.help_messager(message)

                elif message.content == "servers count":
                    await message.channel.send(str(len(client.guilds)))

                elif message.content.lower() == self.prefix + "my posts":
                    if self.benutzer != None:
                        await self.my_posts(message)
                    else: await self.noaccount_error(message)

                elif message.content.startswith(self.prefix + "set "):
                    if self.benutzer != None:
                        await self.set_command(message)
                    else: await self.noaccount_error(message)

                elif message.content.startswith(self.prefix + "delete-account"):
                    if self.benutzer != None:
                        await self.delete_account(message)
                    else: await self.noaccount_error(message)

                elif message.content.startswith(self.prefix + "send-message"):
                    if "X-team" in self.benutzer["role"]:
                        await self.messages_from_mod(message)
                    else: await self.forbidden_error(message)

                elif message.content == self.prefix + "daily-update":
                    await self.daily_update(message)

                elif message.content.lower().startswith(self.prefix + "comment"):
                    if self.permission_checker("comment"):
                        await self.add_comment(message)
                    else: await self.forbidden_error(message)
                    await self.werbung(message)

                elif message.content.startswith(self.prefix + "buy-item "):
                    if self.benutzer != None:
                        await self.buy_shop_item(message)
                    else: await self.noaccount_error(message)

                elif message.content.startswith(self.prefix + "post"):
                    await self.post_zeiger(message, link)
                    await self.werbung(message)

                elif message.content.startswith(self.prefix + "my stats"):
                    if self.benutzer != None:
                        await self.my_stats(message)
                        await self.werbung(message)
                    else: await self.noaccount_error(message)

                elif message.content.startswith(self.prefix + "weather "):
                    if self.permission_checker("weather"):
                        await self.weather_lpz(message)
                    await self.werbung(message)

                elif message.content.lower() == self.prefix + "support":
                    await message.channel.send(":gem:**↓Join our discord Server now!↓**:gem:\nhttps://discord.gg/dF6PXqvmHm")

                elif message.content == "users parameters":
                    await message.channel.send(str(self._users[0]))

                elif message.content == "show ad":
                    await self.werbung(message)

                elif message.content.startswith(self.prefix + "add-ad"):
                    if self.permission_checker("add_ad"):
                        await self.add_ad(message)
                    else:
                        await self.forbidden_error(message)

                elif message.content.lower().startswith(str(self.prefix) + "login"):
                    if self.permission_checker("login"):
                        await self.loginner(message)
                    else:
                        await self.forbidden_error(message)
                    await self.werbung(message)

                elif message.content.lower() == str(self.prefix) + "logout":
                    if self.permission_checker("logout"):
                        await self.logouter(message)
                    else:
                        await self.forbidden_error(message)

                elif message.content.startswith(str(self.prefix) + "search"):
                    if self.permission_checker("search"):
                        searcher_class = self.searcher()
                        await searcher_class.start(message, in_need_values)
                    else:
                        await self.forbidden_error(message)
                    await self.werbung(message)

                elif message.content.startswith(str(self.prefix) + "register '"):
                    if self.permission_checker("register"):
                        registerer = self.registerer()
                        self.waiting_list, self._users, self.user_id ,self.benutzer, self.discord_user = await registerer.start(message, in_need_values)
                        self.data_load()
                    else: await self.forbidden_error(message)
                    await self.werbung(message)

                elif message.content == str(self.prefix) + "close-bot":
                    if "X-team" in self.benutzer["role"]:
                        self.bot_closed = True
                        await message.channel.send("**Bot was closed... **")
                    else: await self.forbidden_error(message)

                elif message.content == str(self.prefix) + "unclose-bot":
                    if "X-team" in self.benutzer["role"]:
                        self.bot_closed = False
                        await message.channel.send("**Bot was unclosed :white_check_mark:**")
                    else: await self.forbidden_error(message)

                elif message.content == str(self.prefix) + "help-register":
                    await self.register_helper(message)

                elif message.content.lower() == (str(self.prefix) + "trust-guild"):
                    await self.guild_truster(message)

                elif message.content.lower() == self.prefix + "history":
                    await self.history_manager(message)

                elif message.content.startswith(self.prefix + "verify"):
                    await self.verify_coder(message)

                elif message.content.startswith(self.prefix + "change-"):
                    if self.permission_checker("change_info"):
                        await self.change_something(message)
                    else:
                        await self.forbidden_error(message)

                elif message.content == self.prefix + "my profile":
                    await self.user_anzeiger(message, self.benutzer["id"], "message", message.author)
                    await self.werbung(message)

                elif message.content == self.prefix + "feedback-notifications" or message.content == self.prefix + "f-notif":
                    if self.benutzer != None:
                        if self.permission_checker("notif"):
                            if self.benutzer["activatet"] != "false":
                                await self.notif(message)
                            else: await self.forbidden_error(message)
                        else: await self.notactivatet_error(message)
                    else: await self.noaccount_error(message)

                elif message.content == self.prefix + "mod-help":
                    if "moderator" in self.benutzer["role"]:
                        await self.mod_help(message)
                    else: await self.forbidden_error(message) 

                elif message.content == self.prefix + "notifications" or message.content == self.prefix + "notif":
                    if self.benutzer != None:
                        if self.benutzer["activatet"] != "false":
                            if self.permission_checker("notif"):
                                await self.notif(message)
                            else:
                                await self.forbidden_error(message)
                        else: await self.notactivatet_error(message)
                    else: await self.noaccount_error(message)
                    await self.werbung(message)

                elif message.content.startswith(self.prefix + "dev-info"):
                    if self.benutzer != None: await self.dev_info(message)
                    else: await self.noaccount_error(message)

                elif message.content.startswith(self.prefix + "dev-profil"):
                    try:
                        user_found = False
                        for value in self._users:
                            try:
                                if value["id"] == message.content.split("'")[1] or \
                                    value["name"] == message.content.split("'")[1]:
                                        await self.dev_user(value, message)
                                        user_found = True
                                        break
                            except:
                                if value["id"] == message.content.split(" ")[1] or \
                                    value["name"] == message.content.split(" ")[1]:
                                    await self.dev_user(value, message)
                                    user_found = True
                                    break
                        if user_found == False:
                            await self.notfound_error(message)
                    except: await message.channel.send("**Use this command so: " + self.prefix + "dev-profil usename or id.**")
                    await self.werbung(message)

                elif message.content.lower() == self.prefix + "money":
                    if self.benutzer != None: 
                        await message.channel.send(embed = discord.Embed(
                            title = self.benutzer["name"].upper() + "'S MONEY",
                            description = "**Your money:\n" + str(self.benutzer["money"]) + "⍫**"
                        ))
                    else:
                        await self.noaccount_error(message)

                elif message.content.startswith(str(self.prefix) + "upload"):
                    if self.benutzer != None:
                        if self.benutzer["activatet"] != "false":
                            upload = self.uploader()
                            self.posts, self.post_id = await upload.start(message, in_need_values)
                        else:
                            await self.notactivatet_error(message)
                    else: await self.noaccount_error(message)
                    await self.werbung(message)

                elif message.content.lower().startswith(str(self.prefix) + "user"):
                    await self.user_anzeiger(message, message.content.split(" ")[1], "message", message.author)
                    await self.werbung(message)

                elif message.content.lower() == str(self.prefix) + "start":
                    if self.benutzer != None:
                        if self.benutzer["activatet"] != "false":
                            if self.permission_checker("start"):
                                starter = self.starter()
                            else:
                                await self.forbidden_error(message)
                            self.waiting_list, self._users = await starter.start(message, in_need_values, message.author, "mes")
                        else:
                            await self.notactivatet_error(message)
                    else: await self.noaccount_error(message)
                    await self.werbung(message)

                elif message.content.lower() == self.prefix + "net-stats":
                    await self.net_stats(message)

                if self.benutzer != None:
                    if message.content.startswith(str(self.prefix) + "change-domain-name = '"):
                        if self.permission_checker("change-domain"):
                            await self.domain_changer(message)
                        else:
                            await self.forbidden_error(message)
                    elif message.content.startswith(self.prefix + "add-role"):
                        if "X-team" in self.benutzer["role"]:
                            gesuchter_user = [i for i in self._users if i["name"] == message.content.split(" ")[1]]
                            if gesuchter_user != []:
                                gesuchter_user[0]["role"] += "*" + message.content.split(" ")[2]
                                await message.channel.send("**Added role. :white_check_mark:**")
                        else: await self.forbidden_error(message)
                    elif message.content.startswith(self.prefix + "raw-user"):
                        if "X-team" in self.benutzer["role"]:
                            await self.raw_user(message)
                        else: await self.forbidden_error(message)

                    elif message.content.startswith(self.prefix + "pay "):
                        if self.benutzer != None: await self.pay(message)
                        else: await self.noaccount_error(message)

                    elif message.content == str(self.prefix) + "safe-data":
                        if self.permission_checker("safe-data"):
                            await self.safe_data(message)
                        else:
                            await self.forbidden_error(message)

                    elif message.content == str(self.prefix) + "update-data":
                        if self.permission_checker("update-data"):
                            self.data_load()
                        else:
                            await self.forbidden_error(message)

                    elif message.content.startswith(self.prefix + "edit-field"):
                        if self.permission_checker("edit_field"):
                            await self.edit_field(message)
                        else:
                            await self.forbidden_error(message)

                    elif message.content.startswith(str(self.prefix) + "dict-append"):
                        if self.permission_checker("dict-append"):
                            await self.user_dict_append(message)
                        else:
                            await self.forbidden_error(message)

                    elif message.content.startswith(self.prefix + "whitelist"):
                        if self.benutzer["activatet"] == "false":
                            await self.whitelister(message)
                        else: await message.channel.send(":x:**Your account's already activatet**")

                    elif message.content.startswith(str(self.prefix) + "ban"):
                        if self.permission_checker("ban"):
                            await self.ban_user(message)
                        else:
                            await self.forbidden_error(message)

                    elif message.content.startswith(str(self.prefix) + "unban"):
                        if self.permission_checker("unban"):
                            await self.unban_user(message)
                        else:
                            await self.forbidden_error(message)

                    elif message.content.lower() == self.prefix + "settings":
                        if self.benutzer != None: await self.settings(message)
                        else: await self.noaccount_error(message)
                    
                    elif message.content.startswith(self.prefix + "add-perm"):
                        if self.benutzer != None:
                            if "X-team" in self.benutzer["role"]:
                                await self.add_perm(message)
                            else:
                                await self.forbidden_error(message)
                        else:
                            await self.noaccount_error(message)

    async def on_reaction_add(self, reaction, user):

        #start        

        self.benutzer = await self.get_user_by_id(user.id)
        in_need_values = [self.waiting_list, self._users, self.posts, self.user_id, self.post_id ,self.benutzer, self.prefix, self.website_name]

        #navigation
        
        if self.bot_closed == False or str(user.id) == "701128119402102925":
            if str(user.id) != "759031129914474556":
                if reaction.emoji == "👆" or reaction.emoji == "👇":
                    await self.search_nav(reaction, user)

                if reaction.emoji == "🔵" or reaction.emoji == "⚪":
                    await self.subscribe_react(reaction, user)

                elif reaction.emoji == "🔻" or reaction.emoji == "🔺":
                    await self.user_anzeige_edit(reaction, user)

                elif reaction.emoji == "✴️":
                    await self.post_vorbereitung(reaction, user)
                    
                elif reaction.emoji == "👊":
                    await self._start(reaction, user)

                if reaction.emoji == "❗":
                    await self.report_post(reaction, user)

                if reaction.emoji == "👍":
                    await self.liker(reaction, user)                              

                elif reaction.emoji == "👎":
                    await self.disliker(reaction, user)

                elif reaction.emoji == "⬆️" or reaction.emoji == "⬇️" or reaction.emoji == "🅰️"\
                    or reaction.emoji == "⭐" or reaction.emoji == "❗" or reaction.emoji == "🗑️":
                    
                    await self.comment_eventer(reaction, user)

                elif reaction.emoji == "💬":
                    await self.comment_anzeiger(reaction, user)

                elif reaction.emoji == "🕴️":
                    await self.user_shower2(reaction, user)

                elif reaction.emoji == "⬇":
                    await self.starter_down(reaction, user)
                
client = MyClient()
client.run("TOKEn")   