import asyncio
import discord
import pandas as pd
import os
import re
from dateutil.parser import parse
from random import randint
from dotenv import load_dotenv
from datetime import date

client = discord.Client()
load_dotenv()
TOKEN = os.getenv('TOKEN')

def parse_currency(currency):
    platinum = gold = electrum = silver = copper = 0
    if 'p' in currency:
        platinum, _, currency = currency.rpartition('p')
    if 'g' in currency:
        gold, _, currency = currency.rpartition('g')
    if 'e' in currency:
        electrum, _, currency = currency.rpartition('e')
        dmisevil = True
    else:
        dmisevil = False
    if 's' in currency:
        silver, _, currency = currency.rpartition('s')
    if 'c' in currency:
        copper, _, _ = currency.rpartition('c')
    total = int(platinum) * 10 + int(gold) + int(electrum) / 2 + int(silver) / 10 + int(copper) / 100
    return total,dmisevil

global gold_df
gold_df = pd.read_csv('partygold.txt',index_col=0)

def save_party_gold():
    global gold_df
    gold_df = gold_df.round(2)
    gold_df.fillna(0,inplace=True)
    gold_df.to_csv('partygold.txt')
    # print('locals:', locals())
    # print('-'*23)                 #something was messy with local/global dataframe. seems fixed.
    # print('globals',globals())
    return gold_df

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$'):
        #DICEROLLS
        if message.content.startswith('$roll'):
            dice_chosen = message.content.split(' ')[1]
            if dice_chosen == 'stats':
                stats_rolled_alldice = []
                stats_rolled_array = []
                message_out = ''
                for i in range(6):
                    rolls = []
                    for j in range(4):
                        rolls.append(randint(1,6))
                    # print(rolls)
                    stats_rolled_alldice.append(rolls.copy())
                    rolls.remove(min(rolls))
                    stats_rolled_array.append(sum(rolls))
                    message_out += f'{i+1}: {stats_rolled_array[i]} - {stats_rolled_alldice[i]}\n'
                message_out = message_out[:-1]
                await message.channel.send(f'4d6k3 rolled stats: \n{message_out}')

            else:
                dice_roll = list(map(int,dice_chosen.split('d')))
                # print(dice_roll)
                dice_total = 0
                rolls = []
                for i in range(dice_roll[0]):
                    rolls.append(randint(1,dice_roll[1]))
                dice_total = sum(rolls)
                await message.channel.send(f'Rolling {dice_chosen}: {dice_total} ( {rolls} )')

        #JLAW GIF - EXPAND TO MORE GIFS?
        elif message.content.startswith('$ohyeahsure'):
            reply_msg = await message.channel.send(f'https://media1.tenor.com/images/f48d05dff1ce06758fe42a5cbc26d33c/tenor.gif?itemid=4486668')
            await reply_msg.add_reaction('👍')
            await reply_msg.add_reaction('👎')
            await message.channel.send(message.author)

        #CALENDAR COMMANDS
        elif message.content.startswith('$cal'):
            calendar_command = message.content.split()[1]
            if calendar_command == 'addevent':
                event_to_add = message.content.replace('$cal addevent ','').split(', ')
                message_reply = f'**Event name**: {event_to_add[0]}\n' \
                                f'**Event time**: {parse(event_to_add[1])}'
                if len(event_to_add) == 3:
                    message_reply += f'\n**Event repeats**: {event_to_add[2]}'
                await message.channel.send(message_reply)

        #HELP SECTION
        elif message.content.startswith('$help'):
            if ' ' in message.content:
                if message.content.split()[1] == '$g':
                    await message.channel.send(f'$g [arg(s)]:\n'
                                               f'  total: displays all gold totals\n'
                                               f'  partyadd/partyspend [#p#g#e#s#c]: splits amount equally between all members\n'
                                               f'  playeradd/playerspend [name] [#p#g#e#s#c]: adds/subtracts from character\n'
                                               f'  lookup [string]: returns all transactions with string in Notes (looks messy!)\n'
                                               f'  lookupdate [date string]: returns all transactions made on specific date (looks messy!)')
                elif message.content.split()[1] == '$cal':
                    await message.channel.send(f'$cal [arg(s)]:\n'
                                               f'  addevent [name] [time] [*repeat:weekly - optional] to add an event')
            else:
                await message.channel.send(f'**Commands**:\n$roll ["stats"/#d#] for dice rolls\n'
                                           f'$cal: type $help $cal for more info\n'# addevent ([name],[time],*[repeats: arg: weekly - not yet implemented]*)'
                                           f'$g: type $help $g for more info')

        #GOLD COMMANDS
        elif message.content.startswith('$g'):
            gold_command = message.content[3:]
            if gold_command.startswith('party'):
                comment = ''
                command, gold_command = gold_command.split(' ',1)
                if ' ' in gold_command:
                    money_amount, comment = gold_command.split(' ',1)
                else:
                    money_amount = gold_command
                if re.search("[^pgesc0-9]", money_amount):
                    await message.channel.send('Bad currency string, try again. Only p,g,e,s,c are allowed')
                    return
                else:
                    total_gold,dmisevil = parse_currency(money_amount)
                    each_gets = round(total_gold / 5, 2)
                    gold_earned = int(each_gets)
                    silver_earned = int(each_gets*10%10)
                    copper_earned = int(each_gets*100%10)
                    if command == 'partyadd':
                        message_reply = f'The party gained {money_amount} total\n' \
                                        f'Each member gets: {gold_earned}g {silver_earned}s {copper_earned}c'
                    elif command == 'partyspend':
                        message_reply = f'The party spent {money_amount} total\n' \
                                        f'Each member spends: {gold_earned}g {silver_earned}s {copper_earned}c'
                        each_gets *= -1
                    if dmisevil:
                        message_reply += f'\nAnd the DM is evil for using electrum'
                    message_reply += f'\nClick 👍 to confirm, 👎 to cancel'
                    reply_msg = await message.channel.send(message_reply)
                    await reply_msg.add_reaction('👍')
                    await reply_msg.add_reaction('👎')

                    def reaction_check(reaction,user):
                        return (user == message.author) and (str(reaction.emoji) == '👍' or str(reaction.emoji) == '👎') and (reaction.message == reply_msg)
                    try:
                        reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=reaction_check)
                    except asyncio.TimeoutError:
                        await message.channel.send('❌ - Sorry, request timed out')
                    else:
                        # print(reaction)
                        if reaction.emoji == '👍':
                            gold_df.iloc[0, [0, 1, 2, 3, 4]] += each_gets
                            gold_df.loc[len(gold_df)] = [each_gets, each_gets, each_gets, each_gets, each_gets,
                                                         date.today().strftime('%Y/%m/%d') + ': ' + comment]
                            save_party_gold()

                            await message.channel.send(f'✅ - Successfully added entry ({money_amount}')
                        elif reaction.emoji == '👎':
                            await message.channel.send(f'Entry ({money_amount}) not added')


            elif gold_command.startswith('player'):
                command,player,amount = gold_command.casefold().split(' ',2)
                if player.casefold() in gold_df.columns:
                    comment = ''
                    if ' ' in amount:
                        amount,comment = amount.split(' ',1)
                    spent_money,dmisevil = parse_currency(amount)
                    if command == 'playeradd':
                        spent_money *= -1
                        message_reply = f'{player.title()} received {amount}'
                        # await message.channel.send(f'{player.capitalize()} received {amount}')
                    elif command == 'playerspend' or command == 'playerspent':
                        message_reply = f'{player.title()} spent {amount}'
                        # await message.channel.send(f'{player.capitalize()} spent {amount}')

                    message_reply += f'\nClick 👍 to confirm, 👎 to cancel'
                    reply_msg = await message.channel.send(message_reply)
                    await reply_msg.add_reaction('👍')
                    await reply_msg.add_reaction('👎')

                    def reaction_check(reaction,user):
                        return (user == message.author) and (str(reaction.emoji) == '👍' or str(reaction.emoji) == '👎') and (reaction.message == reply_msg)

                    try:
                        reaction, user = await client.wait_for('reaction_add', timeout=30.0, check=reaction_check)
                    except asyncio.TimeoutError:
                        await message.channel.send('❌ - Sorry, request timed out')
                    else:
                        # print(reaction)
                        if reaction.emoji == '👍':
                            gold_df.at['total', player] -= spent_money
                            gold_df.loc[len(gold_df), [player.casefold(), 'Notes']] = [-spent_money,f'{date.today().strftime("%Y/%m/%d")}: {comment}']
                            save_party_gold()

                            await message.channel.send(f'✅ - Successfully added entry ({amount})')
                        elif reaction.emoji == '👎':
                            await message.channel.send(f'Entry ({amount}) not added')
                else:
                    await message.channel.send(f'{player} not found, try again.')

            elif gold_command.startswith('total'):
                message_reply = ''
                for i in range(5):
                    total_gold = gold_df.iloc[0,i]
                    message_reply += f'{gold_df.columns[i].title()}: {int(total_gold)}g {int(total_gold*10%10)}s {int(total_gold*100%10)}c\n'
                await message.channel.send(message_reply)

            elif gold_command.startswith('lookupdate'):
                lookup_date = gold_command[11:]
                parsed_lookup_date = parse(lookup_date).strftime('%Y/%m/%d')
                result_gold_df = gold_df.loc[gold_df['Notes'].str.contains(parsed_lookup_date)]
                if result_gold_df.empty:
                    await message.channel.send('No Results Found')
                else:
                    await message.channel.send(result_gold_df)
            elif gold_command.startswith('lookup'):
                lookup = gold_command[7:]
                result_gold_df = gold_df.loc[gold_df['Notes'].str.contains(lookup)]
                if result_gold_df.empty:
                    await message.channel.send('No Results Found')
                else:
                    await message.channel.send(result_gold_df)

    if 'this is america' in message.content.casefold():
        await message.channel.send('https://www.youtube.com/watch?v=YUWq_aBiE_s')

client.run(TOKEN)