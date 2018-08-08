# discord-bot
Intended to be deployed on heroku. Barebones only has a join, leave and me commands. Can be built upon if you want just fork master. I plan to build my own bot in the hitcircles-bot branch.

Config Vars:
1. TOKEN = {your bot's token}

Buildpacks:
1. heroku/python (Should automatically install)
2. https://github.com/Hitsounds/Opus-Buildpack.git (must for the voice commands)
