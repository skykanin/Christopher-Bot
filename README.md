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
| `youtube`                  |Returns latest youtube video from user     |
| `live`                     |Checks if twitch user is live or not       |
| `roll [dx]`                |Rolls a dice from given argument, default dice is d100|
| `disableToggle`            |Disables twitter, youtube and live commands|
| `nc`                       |Returns todays nc posts                    |
| `about`                    |Info about the bot and author with link to github|
| `commands`                 |Links to this page                         |

## Reactions
This bot is able to add reactions to certain messages. You can edit the list `list_of_strings` to change what strings are reacted to
by the bot.

## Logs
This bot also logs deleted and edited messages. When this bot is added to a guild it will make a #logs channel and post all deleted and
edited messages there. On top of that it will also save all of these messages in a database which is used to query spesific messages via
bot commands.

## Development
To see the development status of this bot click **[here](https://github.com/skykanin/Christopher-Bot/projects)**
