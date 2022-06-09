import os.path
from tkinter import *
from tkinter import ttk
import challonge
#from tkinter import messagebox
#from tkinter import filedialog
#import requests


# root.mainloop()
TEST_API_URL = "https://jsonplaceholder.typicode.com/todos/1"
# https://api.challonge.com/v1/
# https://api.challonge.com/v1/tournaments/{tournament}/participants.{json|xml}
CHALLONGE_API_URL = "https://api.challonge.com/v1/"
CHALLONGE_API_KEY = "tIuDkLONDSXpWnVAODVvqCa8cqahooGtPqb745lA"


class mainWindow:
    def __init__(self, window):
        # Define variables
        dirname = os.path.dirname(__file__)
        applicationLogoPath = os.path.join(dirname, "Sigmin AZ SK.png")
        applicationLogo = PhotoImage(file=applicationLogoPath)

        # Construct the window
        window.title("Top 8 Graphic")
        window.iconphoto(False, applicationLogo)

        # Frame of the window
        # mainframe = ttk.Frame(self.root, padding="3 3 12 12")
        # mainframe.grid(column=5, row=2, sticky="N, W, E, S")
        # self.root.columnconfigure(0, weight=1)
        # self.root.rowconfigure(0, weight=1)
        # mainframe.columnconfigure(0, weight=1)
        # mainframe.rowconfigure(2, weight=1)
        window.geometry('800x400+50+50')  # width, height, from top, from left

        # Header bar
        self.menubar = Menu()
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.importContent = importDialog(window)
        self.filemenu.add_command(label="Import...", command=self.importContent.openImportDialog)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=window.quit)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        window.config(menu=self.menubar)
        menubar = Menu(window)

        # Player text fields
        self.playerOne = StringVar()
        self.playerOneEntry = Entry(textvariable=self.playerOne)
        self.playerOneEntry.place(x=40, y=80)
        self.playerOne.set("Player 1")

        self.playerTwo = StringVar()
        self.playerTwoEntry = ttk.Entry(textvariable=self.playerTwo)
        self.playerTwoEntry.place(x=170, y=30)
        self.playerTwo.set("Player 2")

        self.playerThree = StringVar()
        self.playerThreeEntry = ttk.Entry(textvariable=self.playerThree)
        self.playerThreeEntry.place(x=350, y=30)
        self.playerThree.set("Player 3")

        self.playerFour = StringVar()
        self.playerFourEntry = ttk.Entry(textvariable=self.playerFour)
        self.playerFourEntry.place(x=520, y=30)
        self.playerFour.set("Player 4")

        self.playerFive = StringVar()
        self.playerFiveEntry = ttk.Entry(textvariable=self.playerFive)
        self.playerFiveEntry.place(x=170, y=130)
        self.playerFive.set("Player 5")

        self.playerSix = StringVar()
        self.playerSixEntry = ttk.Entry(textvariable=self.playerSix)
        self.playerSixEntry.place(x=300, y=130)
        self.playerSix.set("Player 6")

        self.playerSeven = StringVar()
        self.playerSevenEntry = ttk.Entry(textvariable=self.playerSeven)
        self.playerSevenEntry.place(x=430, y=130)
        self.playerSeven.set("Player 7")

        self.playerEight = StringVar()
        self.playerEightEntry = ttk.Entry(textvariable=self.playerEight)
        self.playerEightEntry.place(x=560, y=130)
        self.playerEight.set("Player 8")


class importDialog:
    def __init__(self, win):
        self.challongeTournament = StringVar()

    def openImportDialog(self):
        # Construct the window
        dlgImport = Toplevel(window)
        dlgImport.title("Import Tournament Information")
        dlgImport.geometry('200x100+50+50')
        dirname = os.path.dirname(__file__)
        applicationLogoPath = os.path.join(dirname, "Sigmin AZ SK.png")
        applicationLogo = PhotoImage(file=applicationLogoPath)
        dlgImport.iconphoto(False, applicationLogo)

        # Import field and button
        challongeTournamentEntry = ttk.Entry(dlgImport, textvariable=self.challongeTournament)
        # challongeTournamentEntry.place(x=40, y=40)
        challongeTournamentEntry.pack()
        importButton = Button(dlgImport, text="Import", command=self.importfromchallonge)
        # importButton.place(x=80, y=80)
        importButton.pack()

    def importfromchallonge(self):
        # Tell pychallonge about your [CHALLONGE! API credentials](http://api.challonge.com/v1).
        challonge.set_credentials("Sigmin", CHALLONGE_API_KEY)

        print(self.challongeTournament.get())
        tournament = challonge.tournaments.show(self.challongeTournament.get())
        participants = challonge.participants.index(tournament["id"])

        # Sort the participants by final rank
        participants.sort(key=lambda x: x['final_rank'])
        top_8 = []
        i = 0

        # Append the top 8 players into their own list by name
        for player in participants:
            if i < 8:
                top_8.append(player["name"])
                i = i + 1

        application.playerOne.set(top_8[0])
        application.playerTwo.set(top_8[1])
        application.playerThree.set(top_8[2])
        application.playerFour.set(top_8[3])
        application.playerFive.set(top_8[4])
        application.playerSix.set(top_8[5])
        application.playerSeven.set(top_8[6])
        application.playerEight.set(top_8[7])


window = Tk()
application = mainWindow(window)
window.mainloop()
