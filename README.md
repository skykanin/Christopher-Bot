# Christopher-Bot
Discord administration bot made with the discord.py framework by skykanin with ❤️. This bot was primarily made for my personal guild only, without regard for implimentation in other guilds. After update 1.5 I will have streamlined the bot so that it can be used by others and not just for me personally™. 

## Regular Commands
Prefix for all the commands can be changed in the config file. All commands follow this structure `!<command> [argument(s)]`

| Command                    | Description                               |
|:---------------------------|:------------------------------------------|
| `ping`                     |Shows timedelta between client and server  |
| `mute [userMention]`       |Mutes a user in all channels (required admin role)|
| `unmute [userMention]`     |Unmutes a user (required admin role)       |
| `twitter`                  |Returns latest tweet from a twitter user   |
| `youtube`                  |Returns latest youtube video from user     |
| `osu profile [user] [mode]`|Returns the osu player profile for a given mode, defualt mode is standard|
| `osu best [user] [mode]`   |Returns the top play of a user for a given mode, defualt mode is standard|
| `live`                     |Checks if twitch user is live or not       |
| `roll [dx]`                |Rolls a dice from given argument, you can find full dice documentation [here](https://github.com/borntyping/python-dice)|
| `nc`                       |Returns todays [nc](https://www.nakedcapitalism.com/) posts|
| `about`                    |Info about the bot and author with link to github|
| `commands`                 |Links to this page                         |

## Per guild configuration
This bot also includes the ability to configure per-guild settings. These are the settings that are available:

| Key                    | Default Value          | Description                         |
|:-----------------------|:-----------------------|:------------------------------------|
| commands_disabled      |False                   |Controls wether or not the `twitter`, `youtube` and `live` commands are disabled|
| roll_channel           |Random text channel     |Controls which channel you can use the `roll` command in|
| osu_channel            |Random text channel     |Controls which channel you can use the `osu` command in|
| admin_role             |Admin                   |Controls what role gives a user permission to use the bots admin commands|

These settings can be changed by using the `query` command group. The commands are as follows:

| Command                    | Description                               |
|:---------------------------|:------------------------------------------|
| `query [query]`            |Write your own custom SQL query            |
| `query print_settings`     |Prints out all the settings for guild you are in|
| `query switch_commands`    |Toggles the commands_disabled key          |
| `query update_roll_channel [channel]`|Updates the roll_channel key to the input channel|
| `query update_osu_channel [channel]`|Updates the osu_channel key to the input channel|
| `query update_admin_role [role]`|Updates the admin_role key to the input role|

## Reactions
This bot is able to add reactions to certain messages. You can edit the list `list_of_strings` to change what strings are reacted to
by the bot.

## Logs
This bot also logs deleted and edited messages. When this bot is added to a guild it will make a #logs channel if it doesn't already exist and post all deleted and edited messages there.

## Download the bot yourself
If you want to download and run the bot yourself you need to have [Python3.6.5](https://www.python.org/downloads/release/python-365/) installed. You can download the bot by cloning this repository. To be able to use the bot you need to have all the api keys in your `config.json` file. I have added a `config_example.json` file for reference. To run the bot you first need to install all the dependencies by going into the root directory and running the command ```python setup.py develop```. Then simply start the bot by running ```python christopher.py```

## Development
You can checkout the development status of this bot **[here](https://github.com/skykanin/Christopher-Bot/projects)**
