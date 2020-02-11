import discord
from discord import utils
 
import config
 
class bot_rolemanager(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
 
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == config.POST_ID:
            channel = self.get_channel(payload.channel_id) # channel's id object
            message = await channel.fetch_message(payload.message_id) # messege's object
            member = utils.get(message.guild.members, id=payload.user_id) # user's object
 
            try:
                emoji = str(payload.emoji) # object of user's emoji
                role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # role's object

                await member.add_roles(role) # givin' role
                print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(member, role))
           
            except KeyError as e:
                print('[ERROR] KeyError, no role found for ' + emoji)
            except Exception as e:
                print(repr(e))
 
    async def on_raw_reaction_remove(self, payload):
        channel = self.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = utils.get(message.guild.members, id=payload.user_id)

        try:
            emoji = str(payload.emoji) # user's emoji object
            role = utils.get(message.guild.roles, id=config.ROLES[emoji]) # role's object
 
            await member.remove_roles(role) # removin' role
            print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))
 
        except KeyError as e:
            print('[ERROR] KeyError, no role found for ' + emoji)
        except Exception as e:
            print(repr(e))
 
# RUN
import os

token = os.getenv('TOKEN')

client = bot_rolemanager()
client.run(token)