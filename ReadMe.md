# Grapheight

A program to automatically create Top 8 graphics for Challonge and Start.gg tournaments. Tailored to the Arizona Rivals of Aether scene.

## Quick Start

### Add your Challonge and Start.gg API Keys

These keys are obtained from your Challonge and Start.gg accounts. Protect these Keys like you would a password to those accounts.

1) **Copy** and **Paste** your API Keys from Challonge and Start.gg in the `API_KEYS.csv` on the respective line
   1) ex/ `CHALLONGE_API_KEY,<Key>`

### Obtaining API Keys

* Instructions for Challonge API Keys [Challonge Developer Settings](https://challonge.com/settings/developer)
* Instructions for Start.gg API Keys [Start.gg Developer Settings](https://start.gg/admin/profile/developer)

### Opening the Application

Requires Python installed.

Run `Grapheight.bat`

### Importing Tournaments

With the UI open, 
1) **Click** *File* 
2) **Click** *Import...*

#### Challonge

1) **Copy** the tournament name from the URL.
   1) From `https://challonge.com/kreggkragg21` copy the `kreggkragg21`
2) **Paste** into the text box
3) **Click** *Import from Challonge*


#### Start.gg

1) **Copy** the tournament name from the URL.
    1) From `https://www.start.gg/tournament/bracket-demons-41-az-roa-monthly/details` copy the `bracket-demons-41-az-roa-monthly`
2) **Paste** into the text box
3) **Click** *Import from Start.gg*

### Generating the Top 8 Graphic

Once the Player names and Characters are verified, simply **Click** *Generate* and the script will open the png in your default photo viewer.

The script will update the `FinalGraphic.png` file located in the *Graphic* folder.

## Additional Setup Information

Custom portrait images can be added and linked to specific player names. For example a Custom Color AZ Shovel Knight portrait is used whenever the name `Sigmin` is entered into one of the player text boxes. These connections are defined in the `PlayerPortraits.csv` file. By default this file has AZ players and images linked but can be updated.

### Added Custom Images

Once a new portrait image (in the .png format) is created, rename it to the player's name (ex/ `Sigmin.png`) and place it in the respective Characters folder (ex/ `Characters/Shovel Knight`) 

### Linking characters and/or images to player names

1) **Open** `PlayerPortraits.csv` file
2) **Add** a new line and **Fill In** the Player's name, character, and image in the following format:
   1) `<Player>,Characters/<Character>/1.png,Characters/<Character>/<Player>.png`
   2) ex/ `Sigmin,Characters/Shovel Knight/1.png,Characters/Shovel Knight/Sigmin.png`
3) **Save** the file and **Launch** Grapheight

### Building Executable from .py (Developer)

1) Install cx_Freeze, (open your command prompt and type pip install cx_Freeze.
2) Install idna, (open your command prompt and type pip install idna.
3) In the setup.py file, update the version.
4) In IDE terminal, type `python`
5) In IDE terminal, type `python setup.py build`
6) Check the newly created folder build.


## Author

    Sigmin | Lead Developer

## Special Thanks

    SBS | Custom High Quality Character Portraits
