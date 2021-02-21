# Nickname bot

## WARNING: THIS BOT IS HORRIBLY INSECURE AND SHOULD ABSOLUTELY **NOT** BE USED EXCEPT IN PRIVATE SERVERS ("just for friends" type situations)

It has **NO** restrictions on who can and can't change whose nickname(s), and there's **NO WAY** to add that functionality (unless you want to fork the project and add it yourself).  
Technically you could restrict who can change whose nickname by placing the bot's role above roles with users you want users to be able to change the nicknames of, but below roles with users you don't want users to be able to change the nicknames of, but that's rather crude.  
I suppose you may use it if you really want to. Here's the link to [add it to your server](https://discord.com/api/oauth2/authorize?client_id=813147271160004629&permissions=201411584&scope=bot).  
Please ensure you place the bot's role at the top of the role list OR above all of the roles that you want users to be able to change the name of. If a user has ANY role that is ANYWHERE above the bot's role, their name will not be change-able with the bot's command.

## Selfhosting
### Outside of Docker
Head over to the [releases](https://github.com/NaCl10/nickname-bot/releases) and download the file main.py from the latest stable release.

Run main.py (Make sure you're in the same directory with main.py and that it's a directory where you're okay with main.py living semi-permanately):
```shell
python3 main.py
```
It will error out. This is because you need to enter a valid bot token in config.ini. See [configuration](https://github.com/NaCl10/nickname-bot#configuration) for more information on that.

After configuration, run main.py again to actually start the bot. It's recommended to use some way of autostarting the script and to run it on a machine that will have high uptime, like a server.

### With Docker

Pull and run the container:
```shell
docker run -v /path/to/config.ini:/bot/config.ini --restart always -d --name nickname-bot nacl10/nickname-bot
```
NOTES: You can specify a particular version of the bot by adding `:release-<version number here>` (DO NOT prefix the version number with "v") to the end of `nacl10/nickname-bot`. The path to config.ini shouldn't actually have a file called config.ini in it yet, it should just be where you want config.ini to be.  Make sure the path to config.ini ends in config.ini, even though config.ini doesn't exist yet. You can *technically* call the container something other than "nickname-bot", but it's not recommended.

It will error out. This is because you need to enter a valid bot token in config.ini. See [configuration](https://github.com/NaCl10/nickname-bot#configuration) for more information on that.

After configuration, start the container again:
```shell
docker start nickname-bot
```
It's recommended to run the container on a machine that will have high uptime, like a server.

### Configuration

First, make sure you've run main.py (or the Docker container) at least once to generate the config file.

Then, edit the configuration file with your text editor of choice. Outside of Docker, it'll be wherever main.py is (provided you ran main.py from the directory that contains main.py). With Docker, it'll be wherever you put it.

Values:
| Value | Description | Required |
| ----- | ----------- | -------- |
| token | The bot token. Information about getting a bot token can be found in [the only good part of the discord.py documentation](https://discordpy.readthedocs.io/en/latest/discord.html#discord-intro). | Yes |
| status | Discord will display this as what the bot is "playing". It comes set to "echo 'R'; while true; do echo 'E'; done" by default, you can set it to whatever you want. | No |

Ignore the "prefixes" section. It should only be edited by the bot itself except in extremely rare edge cases.

## Updating
### Outside of Docker
Delete main.py (DO NOT delete config.ini), download the new main.py from the [releases](https://github.com/NaCl10/nickname-bot/releases), put it where the old main.py was, and run it again/restart your service. Simple as that.

### With Docker
First, pull the new image:
```shell
docker pull nacl10/nickname-bot
```
Then, stop and remove the old container:
```shell
docker stop nickname-bot && docker rm nickname-bot
```
Finally, re-create the container with the new image:
```shell
docker run -v /path/to/config.ini:/bot/config.ini --restart always -d --name naclbot nacl10/nickname-bot
```
