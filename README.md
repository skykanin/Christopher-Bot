# Christopher-Bot
Simple discord administration bot made in discord.py. This bot was primarily made for my personal guild only, without regard for
implimentation in other guilds.

## Commands
Prefix for the commands can be changed in the config file. All commands follow this structure `!<command> [argument(s)]`

| Command                    | Description                               |
|:---------------------------|:------------------------------------------|
| `ping`                     |Shows timedelta between client and server  |
| `mute [userMention]`       |Mutes a user in all channels               |
| `unmute [userMention]`     |Unmutes a user                             |
| `twitter`                  |Returns latest tweet from a twitter user   |
| `live`                     |Checks if twitch user is live or not       |
| `values [username]`        |Returns imgur url for a specific user from saved 8values list. If no argument is given, returns url for message author|
| `addValues [username, url]`|Add a imgur url to a user in the values list |
| `roll [dx]`                |Rolls a dice from given argument, default dice is d100|
| `about`                    |Info about the bot and author with link to github|
| `commands`                 |Links to this page                         |

## Reactions
This bot is able to add reactions to certain messages. You can edit the list `list_of_strings` to change what strings are reacted to
by the bot.

## Combo counter
This bot is able to count emote combos. The combo has to be made by unique users (you cannot combo with yourself).
When someone breaks the combo the bot responds with a message detailing the combo cunt and what emote was comboed.

Here in an example of how the combo counter works:

![alt text](https://image.prntscr.com/image/fLjqNh-wQzu5MJFBOkcsAA.png)
