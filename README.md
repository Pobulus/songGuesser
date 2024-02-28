# songGuesser
Fun little local multiplayer game about guessing songs; made using yacht

## Prerequisites
> this project has so far only been tested on Linux
1. First make sure you install necessary dependecies, on Debian/Ubuntu based distros:
```bash
sudo apt install python3 python3-pip libcairo2-dev libxt-dev libgirepository1.0-dev
```
2. (optional) I'd recommend setting up a virtual environment:
```bash
python3 -m venv /path/to/venv
source /path/to/venv/bin/activate
```
3. install python dependencies through pip:
```bash
pip3 install pydbus pycairo PyGObject thefuzz pyyaml yacht
```

## Usage
Clone this repository and `cd` into its folder. (If you've set up a venv make sure you're using it)

Launch your desired music player, the game uses the first one on the list so you might have to close some browser tabs.
> Youtube in firefox doesn't support changing to next track with MPRIS
 
> Google Chrome doesn't work at all

> Spotify desktop app works well

Run the server with:
```bash
python3 -m yacht sail -m game 
```
You can also specify an address with `-a` and port with `-p`

the default is: `localhost:55555`

Now you can open the game in your browser

> If you want devices on your local network to be able to join, you can set the address to your ip on that LAN

## Gameplay
> choose a starting song on your player and minimize it, perferably mute notifications

Enter your player name, once everyone is on the list press the *I'm ready!* button.
The player will switch to the next track and you will get a prompt to guess the title
Once every player has submitted their guess, the title will be revealed, an players will get a point if their guess was close enough

By navigating to `/spectator.yaml` you can see the current scoreboard and the song title after it has been revealed. It's nice to open this page on a bigger screen for everyone to see, while players join on their smartphones.


## Creddit
This project uses [mpris-python](https://github.com/airtower-luna/mpris-python) to control your local music player
