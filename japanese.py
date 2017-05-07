# coding: utf-8

import tkinter as tk
from tkinter import *
import random
from tkinter.ttk import * 

class LearnJap(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master.title("Learn Japanese")
		self.master.geometry('300x260+260+260')
		self.pack(expand=1)

		self.dataDict, self.proList = self.loadData()
		self.createMainMenu()


		


	def createMainMenu(self):
		label_pady = 5

		# frame for labels on the main pane
		self.mainMenuFrame = tk.Frame(self, borderwidth=1, bg="red")
		self.mainMenuFrame.pack(fill=BOTH)

		# labels
		self.viewAllLabel = tk.Label(self.mainMenuFrame, text="View All Characters", borderwidth=2)
		self.viewAllLabel.pack(fill=BOTH, pady=label_pady)

		self.randomReadLabel = tk.Label(self.mainMenuFrame, text="Random Read Test", borderwidth=2)
		self.randomReadLabel.pack(fill=BOTH, pady=label_pady)



		# bind events to main labels
		self.viewAllLabel.bind("<Button-1>", lambda _:self.viewAllCharacters())
		self.randomReadLabel.bind("<Button-1>", lambda _:self.randomRead())

	def viewAllCharacters(self):
		padx_table = 2
		pady_table = 2

		self.master.withdraw()

		self.viewAllCharWindow = tk.Toplevel()
		self.viewAllCharWindow.title( "Check All Characters" )
		self.viewAllCharWindow.protocol('WM_DELETE_WINDOW', self.closeViewAllCharacters)
		self.viewAllCharWindow.geometry('400x600+260+260')

		tableFrame = tk.Frame(self.viewAllCharWindow, borderwidth=1, bg="red")
		tableFrame.pack(fill=BOTH, expand=True)

		# set the scrollar
		scrollbar = Scrollbar(tableFrame)
		scrollbar.pack(side=RIGHT, fill=Y)

		# set the table for characters
		charTable = Treeview(tableFrame)
		charTable.pack(fill=BOTH, expand=1, padx=padx_table, pady=pady_table)
		columnNames = ("平假名中文","平假名","片假名中文","片假名")
		charTable['columns'] = columnNames

		charTable.heading('#0', text='pronounciation', anchor='center')
		charTable.column('#0', anchor='w', width=50)
		for pro in columnNames:
			charTable.heading(pro, text=pro, anchor='center')
			charTable.column(pro, anchor='w', width=50)

		self.insertDataToCharTable(charTable)

		# set scrollbar for charTable
		charTable.config(yscrollcommand=scrollbar.set)
		scrollbar.config(command=charTable.yview)


		# set function frame
		functionFrame = tk.Frame(self.viewAllCharWindow, borderwidth=1, bg="blue")
		functionFrame.pack(side=BOTTOM, fill=X)

		# go back button
		goBackLabel = tk.Label(functionFrame, text="Go Back", borderwidth=2)
		goBackLabel.pack(side=BOTTOM, pady=5)

		# search entry and button
		searchEntry = tk.Entry(functionFrame)
		searchEntry.pack(side=LEFT, fill=X, padx=5, pady=5, expand=1) 

		searchButton = tk.Button(functionFrame, text="Search", 
				command=lambda :self.searchInCharTable(charTable, searchEntry))
		searchButton.pack(side=RIGHT, padx=5, pady=5)

		

		goBackLabel.bind("<Button-1>", lambda _:self.showMainMenu())
		goBackLabel.bind("<Button-1>", lambda _:self.viewAllCharWindow.destroy(), add='+')


	def searchInCharTable(self, table, entry ):
		s = entry.get()
		if s in self.proList:
			table.selection_set(s)
			table.see(s)
		entry.delete(0, END)
		print("end")


	def insertDataToCharTable(self, table):
		for pro in self.proList:
			pin_ch, pin, pian, pian_ch = self.dataDict[pro]
			table.insert('','end',iid=pro, text=pro, values=[pin_ch, pin, pian, pian_ch])

	def closeViewAllCharacters(self):
		self.master.deiconify()
		self.viewAllCharWindow.destroy()


# random read feature window
	def randomRead(self):
		self.master.withdraw()

		self.randomReadWindow = tk.Toplevel()
		self.randomReadWindow.title( "Check All Characters" )
		self.randomReadWindow.protocol('WM_DELETE_WINDOW', self.closeRandomRead)
		self.randomReadWindow.geometry('600x600+300+300')

		chooseModeFrame = tk.Frame(self.randomReadWindow, borderwidth=1, bg="red")
		chooseModeFrame.pack(side=TOP, pady=20)

		# choose mode check box
		pianCheck, pingCheck = IntVar(), IntVar()
		pianCheckButton = tk.Checkbutton(chooseModeFrame, text="平假名",
						variable=pianCheck, onvalue=1, offvalue=0)
		pingCheckButton = tk.Checkbutton(chooseModeFrame, text="片假名",
						variable=pingCheck, onvalue=1, offvalue=0)
		pianCheckButton.pack(side=LEFT, padx=5)
		pingCheckButton.pack(side=LEFT, padx=5)

		# display random choosen frame
		displayFrame = tk.Frame(self.randomReadWindow, borderwidth=1, bg="blue")
		displayFrame.pack(side=TOP, pady=20)

		# submit button
		generateButton = tk.Button(chooseModeFrame, text="Generate", 
				command=lambda : self.dispRandomChars(displayFrame, [pianCheck.get(), pingCheck.get()]))
		generateButton.pack(side=RIGHT, padx=10)



	def dispRandomChars(self, frame, checkChoices):
		if not any(checkChoices):
			return

		# clear the frame
		for child in frame.winfo_children():
			child.destroy()
		
		proList = self.proList
		dataDic = self.dataDict
		rowFramesList = []
		charLabelsList = []
		answerLabelsList = []
		for _ in range(5):
			# row frame to contain a charlabel and a answer label
			rowFrame = tk.Frame(frame, borderwidth=1, bg="yellow")
			rowFrame.pack(fill=X, expand=1)
			rowFramesList.append(rowFrame)

			# generate char label
			charLabel = tk.Label(rowFrame, text="", borderwidth=2)
			charLabel.pack(side=LEFT, padx=10)
			charLabelsList.append(charLabel)

			# generate answer label
			answerLabel = tk.Label(rowFrame, text="", borderwidth=2)
			answerLabel.pack(side=LEFT, padx=10)
			answerLabelsList.append(answerLabel)

			# get the random characters and config the text
			chars, ans = self.randomGenerateChar(checkChoices)
			charLabel.config(text=chars)
			answerLabel.config(text=ans)



	def randomGenerateChar(self, checkChoices, n=5):
		print("checkChoices: ", checkChoices)
		proList = self.proList
		dataDic = self.dataDict

		charsList = random.choices(list(dataDic.items()), k=5)
		ans = [ c[0] for c in charsList ]

		if all(checkChoices):
			chars = [random.choice([c[1][1], c[1][3]]) for c in charsList]
		elif checkChoices[0]==1:
			chars = [ c[1][1] for c in charsList ]
		elif checkChoices[1]==1:
			chars = [ c[1][3] for c in charsList ]

		return " ".join(chars), " ".join(ans)








	def closeRandomRead(self):
		self.master.deiconify()
		self.randomReadWindow.destroy()



# some other functions
	def showMainMenu(self):
		self.master.deiconify()

	def loadData(self, filename='50Data'):
		dic = {}
		proList = []
		with open("50data", "r", encoding='utf8') as f:			
			data = f.read()
			for line in data.split("\n"):
				words = line.split()
				pron, ping_ch, ping, pian_ch, pian = words
				dic[pron] = [ ping_ch, ping, pian_ch, pian ]
				proList.append(pron)
		return dic, proList





root = tk.Tk()
app = LearnJap(master=root)
app.loadData()
app.mainloop()