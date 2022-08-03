import os.path
from tkinter import *
from tkinter import messagebox
import challonge
from PIL import Image, ImageFont, ImageDraw
import csv
import requests
import json
import datetime

# Get API keys from file. This is terrible security, but oh well.
dirname = os.path.dirname(__file__)
apikeys = os.path.join(dirname, "API_KEYS.csv")
with open(apikeys, encoding='UTF8', newline='') as f:
    fileReader = csv.reader(f, delimiter=',')

    # Use linked portrait if player exists
    for row in fileReader:
        if row[0].__contains__("CHALLONGE_API_KEY"):
            CHALLONGE_API_KEY = row[1]
        if row[0].__contains__("STARTGG_API_KEY"):
            STARTGG_API_KEY = row[1]

if not CHALLONGE_API_KEY:
    print("No Challonge API Key Found. Please add one in API_KEYS.csv")

if not STARTGG_API_KEY:
    print("No Start.gg API Key Found. Please add one in API_KEYS.csv")

CHALLONGE_API_URL = "https://api.challonge.com/v1/"
#CHALLONGE_API_KEY = "tIuDkLONDSXpWnVAODVvqCa8cqahooGtPqb745lA"
STARTGG_API_URL = "https://api.start.gg/gql/alpha"
#STARTGG_API_KEY = "e290acba65f27003c0faa36f5b29f36d"
global top_8


class mainWindow:
    def __init__(self, window):
        # Define variables
        dirname = os.path.dirname(__file__)

        # Sprite button settings
        self.characters = ('Absa', 'Clairen', 'Elliana', 'Etalus', 'Forsburn', 'Hodan', 'Kragg', 'Maypul', 'Mollo',
                           'Olympia', 'Orcane', 'Ori and Sein', 'Pomme', 'Ranno', 'Shovel Knight', 'Sylvanos',
                           'Wraster', 'Zetterburn')
        self.playerOneChar = StringVar()
        self.playerTwoChar = StringVar()
        self.playerThreeChar = StringVar()
        self.playerFourChar = StringVar()
        self.playerFiveChar = StringVar()
        self.playerSixChar = StringVar()
        self.playerSevenChar = StringVar()
        self.playerEightChar = StringVar()

        # Player name fields
        self.playerOne = StringVar()
        self.playerOne.set("Player 1")

        self.playerTwo = StringVar()
        self.playerTwo.set("Player 2")

        self.playerThree = StringVar()
        self.playerThree.set("Player 3")

        self.playerFour = StringVar()
        self.playerFour.set("Player 4")

        self.playerFive = StringVar()
        self.playerFive.set("Player 5")

        self.playerSix = StringVar()
        self.playerSix.set("Player 6")

        self.playerSeven = StringVar()
        self.playerSeven.set("Player 7")

        self.playerEight = StringVar()
        self.playerEight.set("Player 8")

        # Create Top 8 Graphic button
        #self.graphicContent = generateFinalGraphic()


class importDialog:
    def __init__(self):
        print("")

    def importfromchallonge(self, event=None):
        # Tell pychallonge about your [CHALLONGE! API credentials](http://api.challonge.com/v1).
        challonge.set_credentials("Sigmin", CHALLONGE_API_KEY)

        # Get request to Challonge
        try:
            self.challongeTournament = input("Challonge Tournament:")
            tournament = challonge.tournaments.show(self.challongeTournament)
        except:
            messagebox.showerror('Import Error', 'There was an import error')
            self.challongeTournament = ''

        global tournamentInfo
        tournamentInfo = tournament
        participants = challonge.participants.index(tournament["id"])

        # Sort the participants by final rank
        participants.sort(key=lambda x: x['final_rank'])
        global top_8
        top_8 = []
        i = 0

        # Append the top 8 players into their own list by name
        for player in participants:
            if i < 8:
                top_8.append(player["name"])
                i = i + 1

        # Clear Start.gg Import Data if it exists
        try:
            startTournamentInfo[0] = ''
            startTournamentInfo[1] = ''
            startTournamentInfo[2] = ''
            startTournamentInfo[3] = ''
        except NameError:
            print("No Start.gg Tournament to clear")

        self.updatePlayers()
        self.graphicContent = generateFinalGraphic()
        self.graphicContent.generateGraphic()

    def importFromStartGG(self, event=None):

        global top_8
        top_8 = []

        headers = {
            'Authorization': 'Bearer'+STARTGG_API_KEY,
            'Content-Type': 'application/json'
        }

        eventIDQuery = """?query=query EventQuery($eventSlug: String){
    event(slug: $eventSlug){
        id
    }
}&variables={
\"eventSlug\": \"tournament/""" + self.challongeTournament.get() + """/event/rivals-of-aether-singles\"
}"""
        eventIDurl = STARTGG_API_URL + eventIDQuery

        idresponse = requests.request("GET", eventIDurl, headers=headers)

        idData = json.loads(idresponse.text)
        eventID = idData['data']['event']['id']

        # Get Tournament Info
        global startTournamentInfo

        infoQuery = """?query=query AttendeeCount($tourneySlug: String!) {
  tournament(slug: $tourneySlug) {
    id
    name
    url
    startAt
    participants(query: {}) {
      pageInfo {
        total
      }
    }
  }
}&variables={
\"tourneySlug\": \"tournament/""" + self.challongeTournament.get() + """\"
}"""
        infoURL = STARTGG_API_URL + infoQuery
        inforesponse = requests.request("GET", infoURL, headers=headers)
        infoData = json.loads(inforesponse.text)
        tourneyName = infoData['data']['tournament']['name']
        tourneyCount = infoData['data']['tournament']['participants']['pageInfo']['total']
        tourneyURL = "start.gg/tournament/" + infoData['data']['tournament']['url']
        tourneyDate = datetime.datetime.fromtimestamp(infoData['data']['tournament']['startAt']).strftime('%x')
        startTournamentInfo = [tourneyName, tourneyURL, tourneyCount, tourneyDate]


        # Get Tournament Participants
        query = """?query=query EventStandings($eventId: ID!, $page: Int!, $perPage: Int!) {
  event(id: $eventId) {
    id
    name
    standings(query: {
      perPage: $perPage,
      page: $page
    }){
      nodes {
        placement
        entrant {
          id
          name
        }
      }
    }
  }
}&variables={  "eventId":""" + str(eventID) + """,  "page": 1,  "perPage": 8}"""
        startggURL = STARTGG_API_URL + query
        payload="{\"query\":\"query EventStandings($eventId: ID!, $page: Int!, $perPage: Int!) {\\r\\n  event(id: " \
                "$eventId) {\\r\\n    id\\r\\n    name\\r\\n    standings(query: {\\r\\n      perPage: $perPage," \
                "\\r\\n      page: $page\\r\\n    }){\\r\\n      nodes {\\r\\n        placement\\r\\n        entrant " \
                "{\\r\\n          id\\r\\n          name\\r\\n        }\\r\\n      }\\r\\n    }\\r\\n  }\\r\\n}\"," \
                "\"variables\":{\"eventId\":" + str(eventID) + ",\"page\":1,\"perPage\":8}} "

        response = requests.request("POST", startggURL, headers=headers, data=payload)


        data = json.loads(response.text)
        contents = data['data']['event']['standings']['nodes']
        for key in contents:
            participant = key['entrant']
            top_8.append(participant['name'])

        # Clear Challonge Import Data if it exists
        try:
            tournamentInfo["name"] = ''
            tournamentInfo["full_challonge_url"] = ''
            tournamentInfo["participants_count"] = ''
            tournamentInfo["started_at"] = ''
        except NameError:
            print("No Challonge Tournament to clear")

        self.updatePlayers()
        self.graphicContent = generateFinalGraphic()
        self.graphicContent.generateGraphic()

    def updatePlayers(self):

        # Open file linking names to portraits
        dirname = os.path.dirname(__file__)
        playerPortaitPath = os.path.join(dirname, "PlayerPortraits.csv")
        PORTRAIT_SIZE = (20, 20)

        # Update icons if player link exists
        if top_8[0]:
            application.playerOne.set(top_8[0])
            with open(playerPortaitPath, encoding='UTF8', newline='') as f:
                fileReader = csv.reader(f, delimiter=',')
                for row in fileReader:
                    if row[0].__contains__(application.playerOne.get()) or application.playerOne.get().__contains__(row[0]):
                        char = row[1].split("/")
                        application.playerOneChar.set(char[1])
        if top_8[1]:
            application.playerTwo.set(top_8[1])
            with open(playerPortaitPath, encoding='UTF8', newline='') as f:
                fileReader = csv.reader(f, delimiter=',')
                for row in fileReader:
                    if row[0].__contains__(application.playerTwo.get()) or application.playerTwo.get().__contains__(row[0]):
                        char = row[1].split("/")
                        application.playerTwoChar.set(char[1])
        if top_8[2]:
            application.playerThree.set(top_8[2])
            with open(playerPortaitPath, encoding='UTF8', newline='') as f:
                fileReader = csv.reader(f, delimiter=',')
                for row in fileReader:
                    if row[0].__contains__(application.playerThree.get()) or application.playerThree.get().__contains__(row[0]):
                        char = row[1].split("/")
                        application.playerThreeChar.set(char[1])
        if top_8[3]:
            application.playerFour.set(top_8[3])
            with open(playerPortaitPath, encoding='UTF8', newline='') as f:
                fileReader = csv.reader(f, delimiter=',')
                for row in fileReader:
                    if row[0].__contains__(application.playerFour.get()) or application.playerFour.get().__contains__(row[0]):
                        char = row[1].split("/")
                        application.playerFourChar.set(char[1])
        if top_8[4]:
            application.playerFive.set(top_8[4])
            with open(playerPortaitPath, encoding='UTF8', newline='') as f:
                fileReader = csv.reader(f, delimiter=',')
                for row in fileReader:
                    if row[0].__contains__(application.playerFive.get()) or application.playerFive.get().__contains__(row[0]):
                        char = row[1].split("/")
                        application.playerFiveChar.set(char[1])
        if top_8[5]:
            application.playerSix.set(top_8[5])
            with open(playerPortaitPath, encoding='UTF8', newline='') as f:
                fileReader = csv.reader(f, delimiter=',')
                for row in fileReader:
                    if row[0].__contains__(application.playerSix.get()) or application.playerSix.get().__contains__(row[0]):
                        char = row[1].split("/")
                        application.playerSixChar.set(char[1])
        if len(top_8) > 6:
            application.playerSeven.set(top_8[6])
            with open(playerPortaitPath, encoding='UTF8', newline='') as f:
                fileReader = csv.reader(f, delimiter=',')
                for row in fileReader:
                    if row[0].__contains__(application.playerSeven.get()) or application.playerSeven.get().__contains__(row[0]):
                        char = row[1].split("/")
                        application.playerSevenChar.set(char[1])
        else:
            application.playerSeven.set('')
        if len(top_8) > 7:
            application.playerEight.set(top_8[7])
            with open(playerPortaitPath, encoding='UTF8', newline='') as f:
                fileReader = csv.reader(f, delimiter=',')
                for row in fileReader:
                    if row[0].__contains__(application.playerEight.get()) or application.playerEight.get().__contains__(row[0]):
                        char = row[1].split("/")
                        application.playerEightChar.set(char[1])
        else:
            application.playerEight.set('')


class generateFinalGraphic:
    def __init__(self):
        print()

    def generateGraphic(self):
        # Image constants
        templateSize = (1423, 800)
        templateRegion = (0, 0, 1423, 800)
        player1Region = (53, 135, 536, 618)  # (left, upper, right, lower)
        player1ImageSize = (483, 483)
        player1Number = (75, 100, 536, 618)
        player2Region = (553, 135, 811, 393)  # (left, upper, right, lower)
        player2ImageSize = (258, 258)
        player2Number = (562, 125, 536, 618)
        player3Region = (831, 135, 1089, 393)  # (left, upper, right, lower)
        player3ImageSize = (258, 258)
        player3Number = (840, 125, 536, 618)
        player4Region = (1110, 135, 1368, 393)  # (left, upper, right, lower)
        player4ImageSize = (258, 258)
        player4Number = (1119, 125, 536, 618)
        player5Region = (552, 441, 745, 634)  # (left, upper, right, lower)
        player5ImageSize = (193, 193)
        player5Number = (561, 431, 536, 618)
        player6Region = (760, 441, 953, 634)  # (left, upper, right, lower)
        player6ImageSize = (193, 193)
        player6Number = (769, 441, 536, 618)
        player7Region = (967, 441, 1160, 634)  # (left, upper, right, lower)
        player7ImageSize = (193, 193)
        player7Number = (976, 431, 536, 618)
        player8Region = (1175, 441, 1368, 634)  # (left, upper, right, lower)
        player8ImageSize = (193, 193)
        player8Number = (1184, 441, 536, 618)
        imageFont = "BLKCHCRY.TTF"

        # Open file linking names to portraits
        dirname = os.path.dirname(__file__)
        playerPortairPath = os.path.join(dirname, "PlayerPortraits.csv")
        background = os.path.join(dirname, "Graphic/BlankParticipants.png")
        backgroundPreview = Image.open(background).convert("RGBA")
        template = os.path.join(dirname, "Graphic/template.png")
        templatePreview = Image.open(template).convert("RGBA")

        # Variables for final image
        outfile = os.path.join(dirname, "Graphic/FinalGraphic.png")
        finalGraphic = Image.new("RGBA", templateSize)

        # Default character portrait
        defaultportraitpath = os.path.join(dirname, "Graphic/blankCharacter.png")
        defaultpreview = Image.open(defaultportraitpath)
        player1Image = defaultpreview.resize(player1ImageSize)
        player2Image = defaultpreview.resize(player2ImageSize)
        player3Image = defaultpreview.resize(player3ImageSize)
        player4Image = defaultpreview.resize(player4ImageSize)
        player5Image = defaultpreview.resize(player5ImageSize)
        player6Image = defaultpreview.resize(player6ImageSize)
        player7Image = defaultpreview.resize(player7ImageSize)
        player8Image = defaultpreview.resize(player8ImageSize)

        # Set Characters selected from UI
        if application.playerOneChar.get():
            player1portraitpath = os.path.join(dirname, 'Characters/' + application.playerOneChar.get() + '/Full.png')
            portraitpreview = Image.open(player1portraitpath).convert("RGBA")
            player1Image = portraitpreview.resize(player1ImageSize)
        if application.playerTwoChar.get():
            player2portraitpath = os.path.join(dirname, 'Characters/' + application.playerTwoChar.get() + '/Full.png')
            portraitpreview = Image.open(player2portraitpath).convert("RGBA")
            player2Image = portraitpreview.resize(player2ImageSize)
        if application.playerThreeChar.get():
            player3portraitpath = os.path.join(dirname, 'Characters/' + application.playerThreeChar.get() + '/Full.png')
            portraitpreview = Image.open(player3portraitpath).convert("RGBA")
            player3Image = portraitpreview.resize(player3ImageSize)
        if application.playerFourChar.get():
            player4portraitpath = os.path.join(dirname, 'Characters/' + application.playerFourChar.get() + '/Full.png')
            portraitpreview = Image.open(player4portraitpath).convert("RGBA")
            player4Image = portraitpreview.resize(player4ImageSize)
        if application.playerFiveChar.get():
            player5portraitpath = os.path.join(dirname, 'Characters/' + application.playerFiveChar.get() + '/Full.png')
            portraitpreview = Image.open(player5portraitpath).convert("RGBA")
            player5Image = portraitpreview.resize(player5ImageSize)
        if application.playerSixChar.get():
            player6portraitpath = os.path.join(dirname, 'Characters/' + application.playerSixChar.get() + '/Full.png')
            portraitpreview = Image.open(player6portraitpath).convert("RGBA")
            player6Image = portraitpreview.resize(player6ImageSize)
        if application.playerSevenChar.get():
            player7portraitpath = os.path.join(dirname, 'Characters/' + application.playerSevenChar.get() + '/Full.png')
            portraitpreview = Image.open(player7portraitpath).convert("RGBA")
            player7Image = portraitpreview.resize(player7ImageSize)
        if application.playerEightChar.get():
            player8portraitpath = os.path.join(dirname, 'Characters/' + application.playerEightChar.get() + '/Full.png')
            portraitpreview = Image.open(player8portraitpath).convert("RGBA")
            player8Image = portraitpreview.resize(player8ImageSize)

        # Add character images
        with open(playerPortairPath, encoding='UTF8', newline='') as f:
            fileReader = csv.reader(f, delimiter=',')

            # Use linked portrait if player exists
            for row in fileReader:
                if application.playerOne.get() != '':
                    if row[0].__contains__(application.playerOne.get()) or application.playerOne.get().__contains__(row[0]):
                        player1portraitpath = os.path.join(dirname, row[2])
                        portraitpreview = Image.open(player1portraitpath).convert("RGBA")
                        player1Image = portraitpreview.resize(player1ImageSize)
                if application.playerTwo.get() != '':
                    if row[0].__contains__(application.playerTwo.get()) or application.playerTwo.get().__contains__(row[0]):
                        player2portraitpath = os.path.join(dirname, row[2])
                        portraitpreview = Image.open(player2portraitpath).convert("RGBA")
                        player2Image = portraitpreview.resize(player2ImageSize)
                if application.playerThree.get() != '':
                    if row[0].__contains__(application.playerThree.get()) or application.playerThree.get().__contains__(row[0]):
                        player3portraitpath = os.path.join(dirname, row[2])
                        portraitpreview = Image.open(player3portraitpath).convert("RGBA")
                        player3Image = portraitpreview.resize(player3ImageSize)
                if application.playerFour.get() != '':
                    if row[0].__contains__(application.playerFour.get()) or application.playerFour.get().__contains__(row[0]):
                        player4portraitpath = os.path.join(dirname, row[2])
                        portraitpreview = Image.open(player4portraitpath).convert("RGBA")
                        player4Image = portraitpreview.resize(player4ImageSize)
                if application.playerFive.get() != '':
                    if row[0].__contains__(application.playerFive.get()) or application.playerFive.get().__contains__(row[0]):
                        player5portraitpath = os.path.join(dirname, row[2])
                        portraitpreview = Image.open(player5portraitpath).convert("RGBA")
                        player5Image = portraitpreview.resize(player5ImageSize)
                if application.playerSix.get() != '':
                    if row[0].__contains__(application.playerSix.get()) or application.playerSix.get().__contains__(row[0]):
                        player6portraitpath = os.path.join(dirname, row[2])
                        portraitpreview = Image.open(player6portraitpath).convert("RGBA")
                        player6Image = portraitpreview.resize(player6ImageSize)
                if application.playerSeven.get() != '':
                    if row[0].__contains__(application.playerSeven.get()) or application.playerSeven.get().__contains__(row[0]):
                        player7portraitpath = os.path.join(dirname, row[2])
                        portraitpreview = Image.open(player7portraitpath).convert("RGBA")
                        player7Image = portraitpreview.resize(player7ImageSize)
                if application.playerEight.get() != '':
                    if row[0].__contains__(application.playerEight.get()) or application.playerEight.get().__contains__(row[0]):
                        player8portraitpath = os.path.join(dirname, row[2])
                        portraitpreview = Image.open(player8portraitpath).convert("RGBA")
                        player8Image = portraitpreview.resize(player8ImageSize)

        # Paste character portraits on final graphic
        finalGraphic.paste(templatePreview)
        try:
            finalGraphic.paste(player1Image, player1Region, player1Image)
        except ValueError:
            print("No player 1 character")

        try:
            finalGraphic.paste(player2Image, player2Region, player2Image)
        except ValueError:
            print("No player 2 character")

        try:
            finalGraphic.paste(player3Image, player3Region, player3Image)
        except ValueError:
            print("No player 3 character")

        try:
            finalGraphic.paste(player4Image, player4Region, player4Image)
        except ValueError:
            print("No player 4 character")

        try:
            finalGraphic.paste(player5Image, player5Region, player5Image)
        except ValueError:
            print("No player 5 character")

        try:
            finalGraphic.paste(player6Image, player6Region, player6Image)
        except ValueError:
            print("No player 6 character")

        try:
            finalGraphic.paste(player7Image, player7Region, player7Image)
        except ValueError:
            print("No player 7 character")

        try:
            finalGraphic.paste(player8Image, player8Region, player8Image)
        except ValueError:
            print("No player 8 character")

        try:
            # If the tournament is a Kregg's Castle, apply custom background
            if tournamentInfo["name"].__contains__("Kregg"):
                castle = os.path.join(dirname, "Graphic/BlankCastle.png")
                castlePreview = Image.open(castle).convert("RGBA")
                finalGraphic.paste(castlePreview, templateRegion, castlePreview)
        except NameError:
            print("Not a Kregg's Castle")
            azrivals = os.path.join(dirname, "Graphic/BlankAZRivals.png")
            azRivalsPreview = Image.open(azrivals).convert("RGBA")
            finalGraphic.paste(azRivalsPreview, templateRegion, azRivalsPreview)


        # Add Text
        # font = ImageFont.truetype(<font-file>, <font-size>)
        firstFont = ImageFont.truetype(imageFont, 170)
        topRowFont = ImageFont.truetype(imageFont, 86)
        bottomRowFont = ImageFont.truetype(imageFont, 60)
        white = (255, 255, 255)
        grey = (100, 100, 100)
        black = (0, 0, 0)
        textDraw = ImageDraw.Draw(finalGraphic)

        # Text shadow
        rightShadow = (5, 5, 0, 0)
        player1Shadow = tuple(map(sum, zip(player1Number, (10, 10, 0, 0))))
        player2Shadow = tuple(map(sum, zip(player2Number, rightShadow)))
        player3Shadow = tuple(map(sum, zip(player3Number, rightShadow)))
        player4Shadow = tuple(map(sum, zip(player4Number, rightShadow)))
        player5Shadow = tuple(map(sum, zip(player5Number, rightShadow)))
        player6Shadow = tuple(map(sum, zip(player6Number, rightShadow)))
        player7Shadow = tuple(map(sum, zip(player7Number, rightShadow)))
        player8Shadow = tuple(map(sum, zip(player8Number, rightShadow)))

        textDraw.text(player1Shadow, "1", grey, font=firstFont)
        textDraw.text(player2Shadow, "2", grey, font=topRowFont)
        textDraw.text(player3Shadow, "3", grey, font=topRowFont)
        textDraw.text(player4Shadow, "4", grey, font=topRowFont)
        textDraw.text(player5Shadow, "5", grey, font=bottomRowFont)
        textDraw.text(player6Shadow, "5", grey, font=bottomRowFont)
        textDraw.text(player7Shadow, "7", grey, font=bottomRowFont)
        textDraw.text(player8Shadow, "7", grey, font=bottomRowFont)

        # Number Placings text
        textDraw.text(player1Number, "1", white, font=firstFont)
        textDraw.text(player2Number, "2", white, font=topRowFont)
        textDraw.text(player3Number, "3", white, font=topRowFont)
        textDraw.text(player4Number, "4", white, font=topRowFont)
        textDraw.text(player5Number, "5", white, font=bottomRowFont)
        textDraw.text(player6Number, "5", white, font=bottomRowFont)
        textDraw.text(player7Number, "7", white, font=bottomRowFont)
        textDraw.text(player8Number, "7", white, font=bottomRowFont)

        # Player Name Shadows
        firstShadowLocation = (30, 480, 0, 0)
        topShadowLocation = (15, 215, 0, 0)
        bottomShadowLocation = (12, 165, 0, 0)
        fontSize = int(450/len(application.playerOne.get()))
        if fontSize < 50:
            fontSize = 50
        if fontSize > 130:
            fontSize = 130
        firstNameFont = ImageFont.truetype(imageFont, fontSize)
        topNameFont = ImageFont.truetype(imageFont, 42)
        bottomNameFont = ImageFont.truetype(imageFont, 28)

        player1NameShadow = tuple(map(sum, zip(player1Region, firstShadowLocation)))
        player2NameShadow = tuple(map(sum, zip(player2Region, topShadowLocation)))
        player3NameShadow = tuple(map(sum, zip(player3Region, topShadowLocation)))
        player4NameShadow = tuple(map(sum, zip(player4Region, topShadowLocation)))
        player5NameShadow = tuple(map(sum, zip(player5Region, bottomShadowLocation)))
        player6NameShadow = tuple(map(sum, zip(player6Region, bottomShadowLocation)))
        player7NameShadow = tuple(map(sum, zip(player7Region, bottomShadowLocation)))
        player8NameShadow = tuple(map(sum, zip(player8Region, bottomShadowLocation)))

        textDraw.text(player1NameShadow, application.playerOne.get(), grey, font=firstNameFont, anchor="ls")
        textDraw.text(player2NameShadow, application.playerTwo.get(), grey, font=topNameFont)
        textDraw.text(player3NameShadow, application.playerThree.get(), grey, font=topNameFont)
        textDraw.text(player4NameShadow, application.playerFour.get(), grey, font=topNameFont)
        textDraw.text(player5NameShadow, application.playerFive.get(), grey, font=bottomNameFont)
        textDraw.text(player6NameShadow, application.playerSix.get(), grey, font=bottomNameFont)
        textDraw.text(player7NameShadow, application.playerSeven.get(), grey, font=bottomNameFont)
        textDraw.text(player8NameShadow, application.playerEight.get(), grey, font=bottomNameFont)

        # Player Names
        firstLocation = (25, 470, 0, 0)
        topLocation = (10, 210, 0, 0)
        bottomLocation = (7, 160, 0, 0)

        player1Name = tuple(map(sum, zip(player1Region, firstLocation)))
        player2Name = tuple(map(sum, zip(player2Region, topLocation)))
        player3Name = tuple(map(sum, zip(player3Region, topLocation)))
        player4Name = tuple(map(sum, zip(player4Region, topLocation)))
        player5Name = tuple(map(sum, zip(player5Region, bottomLocation)))
        player6Name = tuple(map(sum, zip(player6Region, bottomLocation)))
        player7Name = tuple(map(sum, zip(player7Region, bottomLocation)))
        player8Name = tuple(map(sum, zip(player8Region, bottomLocation)))

        textDraw.text(player1Name, application.playerOne.get(), white, font=firstNameFont, anchor="ls")
        textDraw.text(player2Name, application.playerTwo.get(), white, font=topNameFont)
        textDraw.text(player3Name, application.playerThree.get(), white, font=topNameFont)
        textDraw.text(player4Name, application.playerFour.get(), white, font=topNameFont)
        textDraw.text(player5Name, application.playerFive.get(), white, font=bottomNameFont)
        textDraw.text(player6Name, application.playerSix.get(), white, font=bottomNameFont)
        textDraw.text(player7Name, application.playerSeven.get(), white, font=bottomNameFont)
        textDraw.text(player8Name, application.playerEight.get(), white, font=bottomNameFont)

        # Tournament Info
        particpantFont = ImageFont.truetype(imageFont, 28)
        urlFont = ImageFont.truetype(imageFont, 26)
        try:
            textDraw.text((55, 40), tournamentInfo["name"], black, font=topNameFont)
            textDraw.text((910, 49), tournamentInfo["full_challonge_url"].strip("https://"), black, font=urlFont)
            if tournamentInfo["participants_count"]:
                textDraw.text((65, 733), str(tournamentInfo["participants_count"]) + " Participants", black, font=particpantFont)
            if tournamentInfo["started_at"]:
                textDraw.text((1175, 733), str(tournamentInfo["started_at"])[5:10] + "-" + str(tournamentInfo["started_at"])[0:4], black, font=particpantFont)
        except NameError:
            print("No Challonge Tournament Imported")

        try:
            textDraw.text((55, 40), startTournamentInfo[0], black, font=topNameFont)
            textDraw.text((910, 49), startTournamentInfo[1][0:8] + startTournamentInfo[1][20:], black, font=urlFont)
            if startTournamentInfo[2]:
                textDraw.text((65, 733), str(startTournamentInfo[2]) + " Participants", black, font=particpantFont)
            if startTournamentInfo[3]:
                textDraw.text((1175, 733), str(startTournamentInfo[3]), black, font=particpantFont)
        except NameError:
            print("No Start.gg Tournament Imported")

        # Save to file
        finalGraphic.save(outfile, "PNG")

        # Open the file
        finalGraphic.show()

nonGUI = importDialog()
#nonGUI.importfromchallonge()

window = Tk()
application = mainWindow(window)
nonGUI.importfromchallonge()
#window.mainloop()
