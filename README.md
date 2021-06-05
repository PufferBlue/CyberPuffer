# Cyber Puffer - 赛博河豚🐡

# Deploy with Docker:

```
mkdir /path/to/conf
cd /path/to/conf
```

Then copy contents from the sample config files and edit your own
```
editor config.ini
editor keyword_list.json
```
```
mkdir /path/to/database
```
```
docker run -d \
--restart=always \
--name cyberpuffer \
-v /path/to/conf:/var/bot/conf \
-v /path/to/database:/database/path/in/config \
pufferoverflow/cyberpuffer
```

## Usage:

```
pip install -r requirements.txt
mv conf/config.sample.ini conf/config.ini
mv conf/keyword_list.sample.json conf/keyword_list.json
editor conf/config.ini
editor conf/keyword_list.json
mkdir /path/to/database
python bot.py
```

## Commands:

 - `/start`   Not implemented yet
 - `/uptime`  Reply with bot uptime
 - `/stats`   Reply with how many people bot has seen
 - `/luck`    Get today's luck level (global command)

## Functions:

 - Reply to keywords with text, sticker or forwarded message
 - Auto detect and ban userbots from `tgstat.com`