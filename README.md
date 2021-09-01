# Discord Reminder Bot
Simple bot send text (to tag your friends on scheduled time) and remind them to play together :)


<p align="left">
  <a href="https://replit.com"> <img width="70" height="70" src="https://repl.it/public/images/logo.svg"></a>
  <a href="https://www.python.org/"> <img width="50" height="70" src="https://www.python.org/static/community_logos/python-powered-h.svg"></a>
</p>



## Features
- !ping -> Ping the bot! (Checking connections, etc)
- !add -> Add new schedule. Format = !add [Time] [Text]  --> !add 07.00 Hello everybody!
- !show -> Show registered schedule
- !delete -> Delete a schedule by index. Index can be obtained by using !show command. Format = !delete 1 (Deleting schedule index 1)
- !now -> get local time of the bot. (Currently only supports GMT+7 Timezone. Data saved on UTC format)

# Note

- Fork and run this project on [repl.it!](https://replit.com/@faiznc/DiscordReminderBot#main.py)
- To schedule tagging, without tagging while scheduling, insert "." (dot) after "@" ---> "@.everyone"
- Using local [repl.it](https://replit.com) database to store chedules.
- Configure your own Bot Token at local [repl.it](https://replit.com) environment variables when.
