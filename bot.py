import asyncio
import discord
import pandas as pd
import os
import re
from dateutil.parser import parse
from random import randint
from dotenv import load_dotenv
from datetime import date, timedelta

import bs4 as BeautifulSoup
from splinter import Browser
import time
from requests import get

intents = discord.Intents.default()

client = discord.Client(intents=intents)
load_dotenv()
TOKEN = os.getenv('TOKEN')

# playerconversion = {
#     130879737437487105: 'kali',
#     132956251993800705: 'ix',
#     233814733688537098: "il'kesh",
#     358065918405771274: 'ekko',
#     338219617015300096: 'glob',
#     810158366583291934: 'dm'
# }
#
# trusted_editors = [130879737437487105, 132956251993800705]
#
# partymembers = ['kali', 'ix', "il'kesh", 'ekko', 'glob']


# def parse_currency(currency):
#     money = {'p': 0, 'g': 0, 'e': 0, 's': 0, 'c': 0}
#     dmisevil = True if 'e' in currency else False
#     currency_split = re.split('([pgesc])', currency)
#     for i in range(0, len(currency_split) - 1, 2):
#         money[currency_split[i + 1]] = currency_split[i]
#     total = round(
#         int(money['p'] or 0) * 10 + int(money['g'] or 0) + int(money['e'] or 0) / 2 + int(money['s'] or 0) / 10 + int(
#             money['c'] or 0) / 100, 2)
#     return total, dmisevil
#
#
# global gold_df
# gold_df = pd.read_csv('partygold.txt', index_col=0)


# def save_party_gold():
#     global gold_df
#     gold_df = gold_df.round(2)
#     gold_df.fillna(0, inplace=True)
#     gold_df.to_csv('partygold.txt')
#     return gold_df
#

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if client.user.id == 824502265783386173 and message.channel.id == 833443954359271495:  # if real client and in testing private channel, don't do anything. otherwise (real bot in real channel or test bot in private channel) it will work
        return
    if message.author == client.user:
        return
    if message.content.startswith('$'):
        def reaction_check(reaction, user):
            return (user == message.author) and (
                    str(reaction.emoji) == '👍' or str(reaction.emoji) == '👎') and (
                           reaction.message == reply_msg)

        # if message.content.startswith('$test'):
        # id = 130879737437487105  # User Id
        # member = client.get_guild(616442390734962709).get_member(id)
        # print(member)

        # namename = await client.fetch_user(int('130879737437487105'))
        # print(namename)

        # DICEROLLS
        if message.content.startswith('$roll'):
            dice_chosen = message.content.split(' ')[1]
            if dice_chosen == 'stats':
                stats_rolled_alldice = []
                stats_rolled_array = []
                message_out = ''
                for i in range(6):
                    rolls = [randint(1, 6) for i in range(4)]
                    stats_rolled_alldice.append(rolls.copy())
                    rolls.remove(min(rolls))
                    stats_rolled_array.append(sum(rolls))
                    message_out += f'{i + 1}: {stats_rolled_array[i]} - {stats_rolled_alldice[i]}\n'
                message_out = message_out[:-1]
                await message.channel.send(f'4d6k3 rolled stats: \n`{message_out}`')

            else:
                dice_roll = list(map(int, dice_chosen.split('d')))
                rolls = [randint(1, dice_roll[1]) for i in range(dice_roll[0])]
                # for i in range(dice_roll[0]):
                #     rolls.append(randint(1,dice_roll[1]))
                dice_total = sum(rolls)
                await message.channel.send(f'Rolling {dice_chosen}: `{dice_total} ( {rolls} )`')
        #
        # # JLAW GIF - EXPAND TO MORE GIFS?
        # elif message.content.startswith('$ohyeahsure'):
        #     reply_msg = await message.channel.send(
        #         f'https://media1.tenor.com/images/f48d05dff1ce06758fe42a5cbc26d33c/tenor.gif?itemid=4486668')
        #
        # # CALENDAR COMMANDS
        # elif message.content.startswith('$afk'):
        #     afk_df = pd.read_csv('afk.txt', index_col=0)
        #     if message.content.startswith('$afkcancel'):
        #         cal_date = message.content.split()
        #         parsed_cal_date = parse(cal_date[1])
        #         if parsed_cal_date.weekday() != 5:
        #             await message.channel.send(f"That's not a Saturday")
        #             return
        #         parsed_cal_date = parsed_cal_date.strftime('%Y-%m-%d')
        #         afk_list = afk_df.loc[parsed_cal_date, 'afk'].split(',')
        #         if str(message.author.nick) in afk_list:
        #             afk_list.remove(str(message.author.nick))
        #             if not afk_list:
        #                 afk_df.drop(index=parsed_cal_date, inplace=True)
        #             else:
        #                 afk_df.loc[parsed_cal_date, 'afk'] = ','.join(afk_list)
        #             await message.channel.send(f'Canceled your afk for {parsed_cal_date}')
        #             afk_df.to_csv('afk.txt')
        #     elif message.content.startswith('$afk '):
        #         cal_date = message.content.split()
        #         parsed_cal_date = parse(cal_date[1])
        #         if parsed_cal_date.weekday() != 5:
        #             await message.channel.send(f"That's not a Saturday")
        #             return
        #         parsed_cal_date = parsed_cal_date.strftime('%Y-%m-%d')
        #         if parsed_cal_date in afk_df.index:
        #             if str(message.author.nick) in afk_df.loc[parsed_cal_date, 'afk']:
        #                 await message.channel.send(f'You are already marked as gone that day ({parsed_cal_date}).')
        #                 return
        #             else:
        #                 afk_df.loc[parsed_cal_date, 'afk'] += f',{message.author.nick}'
        #         else:
        #             afk_df.loc[parsed_cal_date, 'afk'] = message.author.nick
        #         await message.channel.send(f'Ok, you are gone on {parsed_cal_date}')
        #         afk_df.to_csv('afk.txt')
        #     elif message.content.startswith('$afklist'):
        #         saturday = date.today() + timedelta((5 - date.today().weekday()) % 7)
        #         month_of_afks = []
        #         for i in range(0, 28, 7):
        #             if (saturday + timedelta(i)).strftime('%Y-%m-%d') in afk_df.index:
        #                 month_of_afks.append((saturday + timedelta(i)).strftime('%Y-%m-%d'))
        #         if month_of_afks:
        #             await message.channel.send(f'**AFK list for the next month**\n'
        #                                        f'```{afk_df.loc[month_of_afks]}```')
        #
        #
        # elif message.content.startswith('$whendoweplaynext'):
        #     afk_df = pd.read_csv('afk.txt', index_col=0, dtype={'afk': str})
        #     saturday = date.today() + timedelta((5 - date.today().weekday()) % 7)
        #     found_date = False
        #     while not found_date:
        #         if saturday.strftime('%Y-%m-%d') in afk_df.index:
        #             afk_str = afk_df.loc[saturday.strftime('%Y-%m-%d'), 'afk']
        #             if ',' in afk_str:
        #                 afk_list = afk_str.split(',')
        #             else:
        #                 afk_list = [afk_str]
        #             if len(afk_list) > 1:
        #                 await message.channel.send(f'More than 1 person is gone on {saturday} ({",".join(afk_list)})')
        #                 saturday = saturday + timedelta(7)
        #             elif '810158366583291934' in afk_df.loc[saturday.strftime('%Y-%m-%d'), 'afk']:
        #                 await message.channel.send(f'Hard to play without a DM!')
        #                 saturday = saturday + timedelta(7)
        #             else:
        #                 found_date = True
        #         else:
        #             found_date = True
        #     await message.channel.send(
        #         f'Next session should be on {saturday}, {(saturday - date.today()).days} days away\n'
        #         f'(not a guarantee this is accurate)')
        #
        # elif message.content.startswith('$cal'):
        #     calendar_command = message.content.split()[1]
        #     if calendar_command == 'addevent':
        #         event_to_add = message.content.replace('$cal addevent ', '').split(', ')
        #         message_reply = f'**Event name**: {event_to_add[0]}\n' \
        #                         f'**Event time**: {parse(event_to_add[1])}'
        #         if len(event_to_add) == 3:
        #             message_reply += f'\n**Event repeats**: {event_to_add[2]}'
        #         await message.channel.send(message_reply)
        #
        # # HELP SECTION
        # elif message.content.startswith('$help'):
        #     if ' ' in message.content:
        #         if message.content.split()[1] == '$g':
        #             await message.channel.send(f'$g <required args> [optional args]:\n'
        #                                        f'  total: displays all gold totals\n'
        #                                        f'  partyadd/partyspend <#p#g#e#s#c> [comment]: splits amount equally between all members\n'
        #                                        f'  playeradd/playerspend <name> <#p#g#e#s#c> [comment]: adds/subtracts from character\n'
        #                                        f'  ispent/igoto <#p#g#e#s#c> [comment]'
        #                                        f'  lookup [string]: returns all transactions with string in Notes\n'
        #                                        f'  lookupdate [date string]: returns all transactions made on specific date')
        #         elif message.content.split()[1] == '$cal':
        #             await message.channel.send(f'$cal [arg(s)]:\n'
        #                                        f'  addevent [name] [time] [*repeat:weekly - optional] to add an event')
        #     else:
        #         await message.channel.send(f'**Commands**:\n'
        #                                    f'$roll ["stats"/#d#] for dice rolls\n'
        #                                    # f'$cal: type $help $cal for more info\n'# addevent ([name],[time],*[repeats: arg: weekly - not yet implemented]*)'
        #                                    f'$g: type $help $g for more info')
        #
        # # GOLD COMMANDS
        # elif message.content.startswith('$g'):
        #     gold_command = message.content[3:]
        #     if gold_command.startswith('party'):
        #         comment = ''
        #         command, gold_command = gold_command.split(' ', 1)
        #         if ' ' in gold_command:
        #             money_amount, comment = gold_command.split(' ', 1)
        #         else:
        #             money_amount = gold_command
        #         if re.search("[^pgesc0-9]", money_amount):
        #             await message.channel.send('Bad currency string, try again. Only p,g,e,s,c are allowed')
        #             return
        #         else:
        #             total_gold, dmisevil = parse_currency(money_amount)
        #             each_gets = round(total_gold / 5, 2)
        #             gold_earned = int(each_gets)
        #             silver_earned = int(each_gets * 10 % 10)
        #             copper_earned = int(each_gets * 100 % 10)
        #             if command == 'partyadd':
        #                 message_reply = f'The party gained {money_amount} total\n' \
        #                                 f'Each member gets: {gold_earned}g {silver_earned}s {copper_earned}c'
        #             elif command == 'partyspend' or command == 'partyspent':
        #                 if each_gets > min(gold_df.iloc[0, [0, 1, 2, 3, 4]]):
        #                     await message.channel.send("Someone doesn't have enough gold")
        #                     return
        #                 message_reply = f'The party spent {money_amount} total\n' \
        #                                 f'Each member spends: {gold_earned}g {silver_earned}s {copper_earned}c'
        #                 each_gets *= -1
        #             else:
        #                 return
        #             if dmisevil:
        #                 message_reply += f'\nAnd the DM is evil for using electrum'
        #             message_reply += f'\nClick 👍 to confirm, 👎 to cancel'
        #             reply_msg = await message.channel.send(message_reply)
        #             await reply_msg.add_reaction('👍')
        #             await reply_msg.add_reaction('👎')
        #
        #             try:
        #                 reaction, user = await client.wait_for('reaction_add', timeout=15.0, check=reaction_check)
        #             except asyncio.TimeoutError:
        #                 await message.channel.send('❌ - Sorry, request timed out')
        #             else:
        #                 if reaction.emoji == '👍':
        #                     gold_df.iloc[0, [0, 1, 2, 3,
        #                                      4]] += each_gets  # add to totals; at some point change to "add the same amount to each of the named party members
        #                     gold_df.loc[len(gold_df)] = [each_gets, each_gets, each_gets, each_gets, each_gets,
        #                                                  comment, date.today().strftime('%Y-%m-%d'),
        #                                                  message.author]  # add new entry in ledger
        #                     save_party_gold()
        #
        #                     await message.channel.send(f'✅ - Successfully added entry ({money_amount})')
        #                 elif reaction.emoji == '👎':
        #                     await message.channel.send(f'Entry ({money_amount}) not added')
        #
        #     elif gold_command.startswith('player') or gold_command.startswith('ispent') or gold_command.startswith(
        #             'igot') or gold_command.startswith('ispend'):
        #         if gold_command.startswith('i'):
        #             command, amount = gold_command.casefold().split(' ', 1)
        #             player = playerconversion[message.author.id]
        #         else:
        #             command, player, amount = gold_command.casefold().split(' ', 2)
        #
        #         if player.casefold() in gold_df.columns:
        #             comment = ''
        #             if ' ' in amount:
        #                 amount, comment = amount.split(' ', 1)
        #             if re.search("[^pgesc0-9]", amount):
        #                 await message.channel.send('Bad currency string, try again. Only p,g,e,s,c are allowed')
        #                 return
        #             else:
        #                 spent_money, dmisevil = parse_currency(amount)
        #             if command in ['playeradd', 'igot']:
        #                 spent_money *= -1
        #                 message_reply = f'{player.title()} received {amount}'
        #             elif command in ['playerspend', 'playerspent', 'ispent', 'ispend']:
        #                 message_reply = f'{player.title()} spent {amount}'
        #                 if float(spent_money) > gold_df.at['total', player]:
        #                     await message.channel.send('**WARNING: PLAYER DOES NOT HAVE SUFFICIENT GOLD, CONTINUE??**')
        #                     return
        #             else:
        #                 return
        #             message_reply += f'\nClick 👍 to confirm, 👎 to cancel'
        #             reply_msg = await message.channel.send(message_reply)
        #             await reply_msg.add_reaction('👍')
        #             await reply_msg.add_reaction('👎')
        #
        #             try:
        #                 reaction, user = await client.wait_for('reaction_add', timeout=15.0, check=reaction_check)
        #             except asyncio.TimeoutError:
        #                 await message.channel.send('❌ - Sorry, request timed out')
        #             else:
        #                 if reaction.emoji == '👍':
        #                     gold_df.at['total', player] -= spent_money
        #                     gold_df.loc[len(gold_df), [player, 'Notes', 'date', 'user']] = [-spent_money, comment,
        #                                                                                     date.today().strftime(
        #                                                                                         "%Y-%m-%d"),
        #                                                                                     message.author]
        #                     save_party_gold()
        #
        #                     await message.channel.send(f'✅ - Successfully added entry ({amount})')
        #                 elif reaction.emoji == '👎':
        #                     await message.channel.send(f'Entry ({amount}) not added')
        #         else:
        #             await message.channel.send(f'{player} not found, try again.')
        #
        #     elif gold_command.startswith('transfer'):
        #         command_split = gold_command[9:].split()
        #         if not all(i in gold_df.columns for i in [command_split[0], command_split[1]]):
        #             await message.channel.send(f'Double check names!')
        #             return
        #         else:
        #             if re.search("[^pgesc0-9]", command_split[2]):
        #                 await message.channel.send('Bad currency string, try again. Only p,g,e,s,c are allowed')
        #                 return
        #             else:
        #                 total_gold, _ = parse_currency(command_split[2])
        #                 if total_gold > gold_df.loc['total', command_split[0]]:
        #                     await message.channel.send('Cannot give more money than you have')
        #                     return
        #                 message_reply = f'{command_split[0].title()} giving {command_split[1].title()} {command_split[2]}' \
        #                                 f'\nClick 👍 to confirm, 👎 to cancel'
        #                 reply_msg = await message.channel.send(message_reply)
        #                 await reply_msg.add_reaction('👍')
        #                 await reply_msg.add_reaction('👎')
        #
        #                 try:
        #                     reaction, user = await client.wait_for('reaction_add', timeout=15.0, check=reaction_check)
        #                 except asyncio.TimeoutError:
        #                     await message.channel.send('❌ - Sorry, request timed out')
        #                 else:
        #                     if reaction.emoji == '👍':
        #                         gold_df.loc[
        #                             len(gold_df), [command_split[0], command_split[1], 'Notes', 'date', 'user']] = [
        #                             -total_gold, total_gold, ' '.join(command_split[3:]),
        #                             date.today().strftime('%Y-%m-%d'), message.author]
        #                         gold_df.loc['total', command_split[0]] -= total_gold
        #                         gold_df.loc['total', command_split[1]] += total_gold
        #                         save_party_gold()
        #                         await message.channel.send(f'✅ - Successfully added entry')
        #
        #                     elif reaction.emoji == '👎':
        #                         await message.channel.send(f'Entry not added')
        #
        #     elif gold_command.startswith('total'):
        #         message_reply = ''
        #         for i in range(5):
        #             total_gold = gold_df.iloc[0, i]
        #             message_reply += f'{gold_df.columns[i].title()}: {int(total_gold)}g {int(total_gold * 10 % 10)}s {int(total_gold * 100 % 10)}c\n'
        #         await message.channel.send(message_reply)
        #
        #     elif gold_command.startswith('lookupdate'):
        #         lookup_date = gold_command[11:]
        #         parsed_lookup_date = parse(lookup_date).strftime('%Y-%m-%d')
        #         result_gold_df = gold_df.loc[gold_df['date'].str.contains(parsed_lookup_date)]
        #         if result_gold_df.empty:
        #             await message.channel.send('No Results Found')
        #         else:
        #             await message.channel.send(f'```{result_gold_df.drop(columns="user")}```')
        #
        #     elif gold_command.startswith('lookup'):
        #         lookup = gold_command[7:]
        #         result_gold_df = gold_df.loc[gold_df['Notes'].str.contains(lookup)]
        #         if result_gold_df.empty:
        #             await message.channel.send('No Results Found')
        #         else:
        #             await message.channel.send(f'```{result_gold_df.drop(columns="user")}```')
        #
        #     elif gold_command.startswith('backup'):
        #         gold_df.to_csv(f'partygold - backup {date.today().strftime("%Y-%m-%d")}.txt')
        #
        #
        # elif message.content.startswith('$lootstatus'):
        #     loot_df = pd.read_csv('loot.txt', index_col='item', dtype={'quantity': int})
        #     loot_df.sort_index(inplace=True)
        #     await message.channel.send(f'https://i.imgur.com/9bXloIu.mp4')
        #     await message.channel.send(f'```{loot_df}```')
        #
        # elif message.content.startswith('$lootadd'):
        #     if message.author.id not in trusted_editors:
        #         return
        #     loot_df = pd.read_csv('loot.txt', index_col='item')
        #     commands = message.content.split()
        #     if commands[-1] == 'all':  # no reason to loot add "all" of anything, so assume it's a mistake and pop it off
        #         commands.pop()
        #
        #     if commands[-1].isnumeric():
        #         quantity_specified = True
        #         quantity_to_add = int(commands.pop())
        #     else:
        #         quantity_specified = False
        #     item_name = ' '.join(commands[1:])
        #
        #     if item_name in loot_df.index:
        #         loot_df.loc[item_name, 'quantity'] += quantity_to_add if quantity_specified else 1
        #         # if quantity_specified:
        #         #     loot_df.loc[item_name,'quantity'] += int(commands[-1])
        #         # else:
        #         #     loot_df.loc[item_name, 'quantity'] += 1
        #
        #     else:
        #         loot_df.loc[item_name, 'quantity'] = quantity_to_add if quantity_specified else 1
        #         # if quantity_specified:
        #         #     loot_df.loc[item_name,'quantity'] = int(commands[-1])
        #         # else:
        #         #     loot_df.loc[item_name,'quantity'] = 1
        #     loot_df.to_csv('loot.txt')
        #
        # elif message.content.startswith('$lootremove'):
        #     if message.author.id not in trusted_editors:
        #         return
        #     loot_df = pd.read_csv('loot.txt', index_col='item')
        #     commands = message.content.split()
        #     remove_all = False
        #     if commands[-1] == 'all':
        #         remove_all = True
        #         commands.pop()
        #     elif commands[-1].isnumeric():
        #         quantity_specified = True
        #         quantity_to_remove = int(commands.pop())
        #     else:
        #         quantity_specified = False
        #     item_name = ' '.join(commands[1:])
        #
        #     message_reply = f'Removing {"all of" if remove_all else commands[-1] if quantity_specified else "one"} {item_name}' \
        #                     f'\nClick 👍 to confirm, 👎 to cancel'
        #     reply_msg = await message.channel.send(message_reply)
        #     await reply_msg.add_reaction('👍')
        #     await reply_msg.add_reaction('👎')
        #
        #     try:
        #         reaction, user = await client.wait_for('reaction_add', timeout=15.0, check=reaction_check)
        #     except asyncio.TimeoutError:
        #         await message.channel.send('❌ - Sorry, request timed out')
        #     else:
        #         if reaction.emoji == '👍':
        #             if item_name in loot_df.index:
        #                 if remove_all:
        #                     loot_df.drop(index=item_name, inplace=True)
        #                 else:
        #                     if quantity_specified:
        #                         if loot_df.loc[item_name, 'quantity'] < quantity_to_remove:
        #                             await message.channel.send('Cannot remove more than the party owns')
        #                         else:
        #                             loot_df.loc[item_name, 'quantity'] -= quantity_to_remove
        #                     else:
        #                         loot_df.loc[item_name, 'quantity'] -= 1
        #                     if loot_df.loc[item_name, 'quantity'] == 0:
        #                         loot_df.drop(index=item_name, inplace=True)
        #                 loot_df.to_csv('loot.txt')
        #                 await message.channel.send(
        #                     f'✅ - Successfully removed {"all of" if remove_all else commands[-1] if quantity_specified else "one"} {item_name}')
        #             else:
        #                 await message.channel.send('Item not in registry')
        #         elif reaction.emoji == '👎':
        #             await message.channel.send(f'{item_name} not removed')
        #
        # # elif message.content.startswith('$register'):
        # #     _, partynumber = message.content.split(' ')
        # #     party_members_dict = {}
        # #     party_members_dict[message.author.id] = partynumber
        # #     party_members_dict

    if 'this is america' in message.content.casefold():
        await message.channel.send('https://www.youtube.com/watch?v=YUWq_aBiE_s')
    if 'garlic bread' in message.content.casefold():
        await message.channel.send('https://c.tenor.com/gIYmYE_OlzEAAAAC/bread-makes-you-fat-bread.gif')
    if 'fireballllll' in message.content.casefold():
        await message.channel.send(
            'https://media1.tenor.com/images/36798911240cea9497b874122c7f559f/tenor.gif?itemid=18958548')
    if any(terfs in message.content.casefold() for terfs in ['rowling','harry potter','chappelle','chapelle',' atwood','linehan','gervais']):
        await message.channel.send('https://gfycat.com/tamevariablebaiji')
    if 'tiktok.com/' in message.content.casefold() and not message.embeds:
        # print(message.content)
        url = re.search("(?P<url>https?://[^\s]+)", message.content).group("url")
        print('1')
        browser = Browser('firefox', headless=True)
        print('1.5')
        browser.visit(url)
        print('2')
        soup = BeautifulSoup.BeautifulSoup(browser.html, 'html.parser')
        vid_url = soup.find('video')['src']
        # print(vid_url)
        browser.quit()
        print('3')
        # req = get(vid_url)
        # file = open(f'file.mp4', 'wb')
        # for chunk in req.iter_content(1000000):
        #     file.write(chunk)
        # file.close()
        # await message.channel.send(file=discord.File('file.mp4'))
        # os.remove('file.mp4')
        await message.channel.send(vid_url)
client.run(TOKEN)
