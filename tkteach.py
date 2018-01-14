# tkteach.py
# By Ryan M. Mones
# www.Comet.cool
# Written on Python 2.7.13 (64-bit)
# Tested on Python 3.6.1 (64-bit)
#
#     __________  __  _______________   __________  ____  __ 
#    / ____/ __ \/  |/  / ____/_  __/  / ____/ __ \/ __ \/ / 
#   / /   / / / / /|_/ / __/   / /    / /   / / / / / / / /  
#  / /___/ /_/ / /  / / /___  / / _  / /___/ /_/ / /_/ / /___
#  \____/\____/_/  /_/_____/ /_/ (_) \____/\____/\____/_____/
#
#
#   Copyright 2018 Ryan M. Mones
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
#

from PIL import Image, ImageTk
import os
import time
import sqlite3 as sq

try:
	import tkinter as tk
except ImportError:
	pass

try:
	import Tkinter as tk
except ImportError:
	pass

try:
	print('tkinter imported, version: '+str(tk.TkVersion))
except NameError:
	print('FATAL ERROR! Unable to import tkinter.')
	exit()

class tkteach:
	
	def __init__(self, master):
		print("-->__init__")
		
		self.master = master
		master.title("tkteach version 001")
		
		master.bind("<Key>", self.keyPressed)
		
		# Create GUI elements:
		
		self.titleLabel = tk.Label(master, text="tkteach version 001")
		self.titleLabel.pack()
		
		# BOTTOM "STATUS BAR" VVVVVVVVVVVVVVVVVVVVVVVVV
		
		self.statusBar = tk.Label(master, text="", relief=tk.RIDGE)
		self.statusBar.pack(side=tk.BOTTOM, fill=tk.X)
		
		self.initialize()
		
		# LEFT FRAME VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
		
		self.frameSeperator00 = tk.Frame(master,width=6,height=1)
		self.frameSeperator00.pack(side=tk.LEFT)
		
		self.frameLEFT = tk.Frame(master,bd=2,relief=tk.SUNKEN)
		self.frameLEFT.pack(side=tk.LEFT)
		
		self.datasetTitleLabel = tk.Label(self.frameLEFT, text="Data Set Selection:")
		self.datasetTitleLabel.pack()
		
		self.dataSetsListbox = tk.Listbox(self.frameLEFT,relief=tk.FLAT)
		for item in self.dataSetsListStr:
			self.dataSetsListbox.insert(tk.END, item)
		self.dataSetsListbox.pack()
		
		self.loadDataSetButton = tk.Button(self.frameLEFT, text="Load Data Set", command=self.loadDataSet)
		self.loadDataSetButton.pack()
		
		self.dataSetStatusLabel = tk.Label(self.frameLEFT, text="No Data Set Loaded!")
		self.dataSetStatusLabel.pack()
		
		self.frameSeperator01 = tk.Frame(master,width=20,height=1)
		self.frameSeperator01.pack(side=tk.LEFT)
		
		# MIDDLE FRAME VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
		
		self.frameMIDDLE = tk.Frame(master, bd=2)
		self.frameMIDDLE.pack(side=tk.LEFT)
		
		self.imgStage = tk.Label(self.frameMIDDLE, text="")
		self.imgStage.pack()
		
		self.imgFileName = tk.Label(self.frameMIDDLE, text="")
		self.imgFileName.pack()
		
		self.frameMIDDLEBUTTONS = tk.Frame(self.frameMIDDLE, bd=2)
		self.frameMIDDLEBUTTONS.pack()
		
		self.prevImageButton = tk.Button(self.frameMIDDLEBUTTONS, text="<- Save & Previous", command=self.prevImage, state=tk.DISABLED)
		self.prevImageButton.pack(side=tk.LEFT)
		
		self.nextImageButton = tk.Button(self.frameMIDDLEBUTTONS, text="Save & Next ->", command=self.nextImage, state=tk.DISABLED)
		self.nextImageButton.pack(side=tk.LEFT)
		
		self.frameMIDDLEIMGLABEL = tk.Frame(self.frameMIDDLE, bd=2)
		self.frameMIDDLEIMGLABEL.pack()
		
		self.imageNumberLabel = tk.Label(self.frameMIDDLEIMGLABEL, text="Image Number:")
		self.imageNumberLabel.pack(side=tk.LEFT)
		
		self.imageNumberInput = tk.Entry(self.frameMIDDLEIMGLABEL, width=10)
		self.imageNumberInput.pack(side=tk.LEFT)
		
		self.skipToImageButton = tk.Button(self.frameMIDDLEIMGLABEL, text="Go", command=self.skipToImage, state=tk.DISABLED)
		self.skipToImageButton.pack(side=tk.LEFT)
		
		self.frameMIDDLEIMGZOOM = tk.Frame(self.frameMIDDLE, bd=2)
		self.frameMIDDLEIMGZOOM.pack()
		
		self.imageZoomLabel = tk.Label(self.frameMIDDLEIMGZOOM, text="Zoom:")
		self.imageZoomLabel.pack(side=tk.LEFT)
		
		self.zoomOutButton = tk.Button(self.frameMIDDLEIMGZOOM, text="-", command=self.zoomOut, state=tk.DISABLED)
		self.zoomOutButton.pack(side=tk.LEFT)
		
		self.zoomInButton = tk.Button(self.frameMIDDLEIMGZOOM, text="+", command=self.zoomIn, state=tk.DISABLED)
		self.zoomInButton.pack(side=tk.LEFT)
		
		self.currentZoomLabel = tk.Label(self.frameMIDDLEIMGZOOM, text=' '+str(self.imgScaleFactor)+'X ')
		self.currentZoomLabel.pack(side=tk.LEFT)
		
		self.frameSeperator02 = tk.Frame(master,width=20,height=1)
		self.frameSeperator02.pack(side=tk.LEFT)
		
		# RIGHT FRAME VVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVVV
		
		self.frameRIGHT = tk.Frame(master, bd=2, relief=tk.SUNKEN)
		self.frameRIGHT.pack(side=tk.LEFT)
		
		self.categoriesLabel = tk.Label(self.frameRIGHT, text="Categories:")
		self.categoriesLabel.pack()
		
		self.categoriesListbox = tk.Listbox(self.frameRIGHT, selectmode=tk.MULTIPLE, selectbackground='#119911',relief=tk.FLAT, bd=2)
		for item in self.categories:
			self.categoriesListbox.insert(tk.END, item)
		self.categoriesListbox.pack()
		self.categoriesListbox.config(state=tk.DISABLED)
		
		self.frameSeperator03 = tk.Frame(master,width=6,height=1)
		self.frameSeperator03.pack(side=tk.LEFT)
	
	def initialize(self):
		print("-->initialize")
		
		#Set parameters:
		self.imgScaleFactor = 2		
		
		#Sub-initializations
		self.initializeDatabase()
		self.initializeDatasets()
		self.initializeCategories()
	
	def initializeDatabase(self):
		print("-->initializeDatabase")
		
		#Load/create database:
		self.db = sq.connect('storage.db')
		self.cursor = self.db.cursor()
		self.cursor.execute('CREATE TABLE IF NOT EXISTS dataSets(id INTEGER NOT NULL PRIMARY KEY, dataSetName TEXT, dataSetPath TEXT UNIQUE)')
		self.cursor.execute('CREATE TABLE IF NOT EXISTS images(id INTEGER NOT NULL PRIMARY KEY, dataSet_id INTEGER, imageName TEXT, imagePath TEXT UNIQUE, FOREIGN KEY(dataSet_id) REFERENCES dataSets(id))')
		self.cursor.execute('CREATE TABLE IF NOT EXISTS categories(id INTEGER NOT NULL PRIMARY KEY, categoryName TEXT UNIQUE)')
		self.cursor.execute('CREATE TABLE IF NOT EXISTS labels(category_id INTEGER, image_id INTEGER, FOREIGN KEY(category_id) REFERENCES categories(id), FOREIGN KEY(image_id) REFERENCES images(id))')
		self.db.commit()
	
	def initializeDatasets(self):
		print("-->initializeDatasets")
		
		#Get Datasets:
		d = '.'
		self.dataSetsListDir = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))]
		self.dataSetsListStr = [x[2:] for x in self.dataSetsListDir]
		if len(self.dataSetsListDir)==0:
			self.statusBar.config(text="ERROR! No datasets found.")
			print("ERROR! No datasets found.")
	
	def initializeCategories(self):
		print("-->initializeCategories")
		
		#Get Categories from categories.txt file:
		try:
			catFile = open('categories.txt','r')
			self.categories = [o.strip() for o in catFile.readlines()]
			catFile.close()
		except IOError:
			self.categories = []
			self.statusBar.config(text="ERROR! No categories found.")
			print("ERROR! No categories found.")
		if len(self.categories)==0:
			self.statusBar.config(text="ERROR! No categories found.")
			print("ERROR! No categories found.")
		
		#Populate db table for categories:		
		for category in self.categories:
			self.cursor.execute('INSERT OR IGNORE INTO categories(categoryName) VALUES(?)',(category,))
		self.db.commit()
		
		#Parse Categories, set ad-hoc category key bindings:
		self.keyBindings=[]
		for keyi in self.categories:
			if keyi[0]=="(" and keyi[2]==")":
				if keyi[1] in self.keyBindings:
					self.statusBar.config(text="ERROR! Multiple categories with the same key binding!")
					print("ERROR! Multiple categories with the same key binding!")
					exit()
				else:
					self.keyBindings.append(keyi[1].lower())
	
	def keyPressed(self, key):
		print("-->keyPressed: "+str(key.char))
		
		if key.keysym == 'Left':
			self.prevImageButton.config(relief=tk.SUNKEN)
			self.prevImageButton.update_idletasks()
			self.prevImage()
			time.sleep(0.05)
			self.prevImageButton.config(relief=tk.RAISED)
		elif key.keysym == 'Right':
			self.nextImageButton.config(relief=tk.SUNKEN)
			self.nextImageButton.update_idletasks()
			self.nextImage()
			time.sleep(0.05)
			self.nextImageButton.config(relief=tk.RAISED)
		elif key.char == '+':
			self.zoomInButton.config(relief=tk.SUNKEN)
			self.zoomInButton.update_idletasks()
			self.zoomIn()
			time.sleep(0.05)
			self.zoomInButton.config(relief=tk.RAISED)
		elif key.char == '-':
			self.zoomOutButton.config(relief=tk.SUNKEN)
			self.zoomOutButton.update_idletasks()
			self.zoomOut()
			time.sleep(0.05)
			self.zoomOutButton.config(relief=tk.RAISED)
		else:
			#Check if this is an ad-hoc keybind for a category selection...
			try:
				if self.categoriesListbox.selection_includes(self.keyBindings.index(key.char.lower())):
					self.categoriesListbox.selection_clear(self.keyBindings.index(key.char.lower()))
				else:
					self.categoriesListbox.selection_set(self.keyBindings.index(key.char.lower()))
			except ValueError:
				pass
	
	def prevImage(self):
		#Go to previous image
		print("-->prevImage")
		self.saveImageCategorization()
		if self.imageSelection>0:
			self.imageSelection-=1
			self.loadImage()
		else:
			self.statusBar.config(text="ERROR! Already at first image.")
			print("ERROR! Already at first image.")
	
	def nextImage(self):
		#Go to next image
		print("-->nextImage")
		self.saveImageCategorization()
		if self.imageSelection<(len(self.imageListDir)-1):
			self.imageSelection+=1
			self.loadImage()
		else:
			self.statusBar.config(text="ERROR! Already at last image.")
			print("ERROR! Already at last image.")
	
	def loadImage(self):
		print("-->loadImage")
		
		#Draw image to screen:
		imageFile = Image.open(self.imageListDir[self.imageSelection])
		canvasImage = ImageTk.PhotoImage(imageFile.resize((imageFile.size[0]*self.imgScaleFactor,imageFile.size[1]*self.imgScaleFactor), Image.NEAREST))
		self.imgStage.config(image=canvasImage)
		self.imgStage.image = canvasImage
		self.imgFileName.config(text=str(self.imageListStr[self.imageSelection]))
		self.imageNumberInput.delete(0, tk.END)
		self.imageNumberInput.insert(0, str(self.imageSelection))
		self.statusBar.config(text="")
		
		#Read from db and update starting categories in listbox if data exists:
		self.categoriesListbox.selection_clear(0,len(self.categories))
		self.cursor.execute('SELECT category_id FROM labels WHERE image_id = ?',(self.db_getImageID(self.imageListDir[self.imageSelection]),))
		for category_id in self.cursor.fetchall():
			self.cursor.execute('SELECT categoryName FROM categories WHERE id = ?',(category_id[0],))
			categoryName = self.cursor.fetchone()[0]
			try:
				self.categoriesListbox.selection_set(self.categories.index(categoryName))
			except ValueError:
				self.statusBar.config(text="FATAL ERROR! Image is saved with invalid category.")
				print('FATAL ERROR! Image is saved with invalid category: '+str(categoryName))
				print('image Name: '+self.imageListStr[self.imageSelection])
				print('This category must be listed in the categories.txt file.')
				exit()
	
	def saveImageCategorization(self):
		print("-->saveImageCategorization")
		
		#Clear out existing category labels for the image...
		self.cursor.execute('DELETE FROM labels WHERE image_id = ?', (self.db_getImageID(self.imageListDir[self.imageSelection]),))
		
		#Insert new category labels for the image...
		for cati in self.categoriesListbox.curselection():
			self.cursor.execute('INSERT INTO labels(image_id, category_id) VALUES(?, ?)',(self.db_getImageID(self.imageListDir[self.imageSelection]), self.db_getCategoryID(self.categories[cati])))
		self.db.commit()
	
	def skipToImage(self):
		print("-->skipToImage")
		try:
			tryImageSelection = int(self.imageNumberInput.get())
			if (tryImageSelection>=0) and (tryImageSelection<len(self.imageListDir)):
				self.imageSelection = tryImageSelection
				self.loadImage()
			else:
				self.statusBar.config(text="ERROR! Image does not exist.")
				print("ERROR! Image does not exist.")
		except:
			self.statusBar.config(text="ERROR! Invalid image selection.")
			print("ERROR! Invalid image selection.")
	
	def loadDataSet(self):
		print("-->loadDataSet")
		
		#Check to see if selection has been made
		try:
			self.dataSetSelection = int(self.dataSetsListbox.curselection()[0])
		except IndexError:
			self.dataSetStatusLabel.config(text='No selection!')
			self.dataSetSelection = -1
		
		#If a valid dataSet is selected...
		if self.dataSetSelection>=0:
		
			#Load images in dataset:
			d = self.dataSetsListDir[self.dataSetSelection]
			self.imageListDir = [os.path.join(d, o) for o in os.listdir(d) if os.path.isdir(os.path.join(d,o))==False]
			self.imageListStr = [o.split('\\')[-1] for o in self.imageListDir]
			self.dataSetStatusLabel.config(text='Dataset: '+str(self.dataSetsListStr[self.dataSetSelection]))
			
			#Create db table entry for this dataSet:
			self.cursor.execute('INSERT OR IGNORE INTO dataSets(dataSetName, dataSetPath) VALUES(?, ?)', (self.dataSetsListStr[self.dataSetSelection], self.dataSetsListDir[self.dataSetSelection]))
			
			#Populate db table entries for all images in this dataSet (this can take a few seconds if over ~2,000 images):
			dataSet_id = self.db_getDataSetID(self.dataSetsListStr[self.dataSetSelection])
			for imagei in range(len(self.imageListStr)):
				self.cursor.execute('INSERT OR IGNORE INTO images(dataSet_id, imageName, imagePath) VALUES(?, ?, ?)',(dataSet_id, str(self.imageListStr[imagei]), str(self.imageListDir[imagei])))
			self.db.commit()
			
			#Prepare image stage:
			self.imageNumberInput.delete(0, tk.END)
			self.imageNumberInput.insert(0, '0')
			self.prevImageButton.config(state=tk.NORMAL)
			self.nextImageButton.config(state=tk.NORMAL)
			self.skipToImageButton.config(state=tk.NORMAL)
			self.categoriesListbox.config(state=tk.NORMAL)
			self.zoomInButton.config(state=tk.NORMAL)
			self.zoomOutButton.config(state=tk.NORMAL)
			
			#Go to first image
			self.skipToImage()
			
			#Communicate:
			self.statusBar.config(text='Dataset loaded: '+str(self.dataSetsListStr[self.dataSetSelection])+' , Number of images: '+str(len(self.imageListDir)))
			print('---->Dataset loaded: '+str(self.dataSetsListStr[self.dataSetSelection])+' , Number of images: '+str(len(self.imageListDir)))
	
	def zoomIn(self):
		#Make image display larger.
		#Since anti-aliasing is NOT used, only integer zoom factors are permitted.
		print("-->zoomIn")
		self.imgScaleFactor += 1
		self.currentZoomLabel.config(text=' '+str(self.imgScaleFactor)+'X ')
		self.loadImage()
	
	def zoomOut(self):
		#Make image display smaller
		#Since anti-aliasing is NOT used, only integer zoom factors are permitted.
		print("-->zoomOut")
		if self.imgScaleFactor>1:
			self.imgScaleFactor -= 1
			self.currentZoomLabel.config(text=' '+str(self.imgScaleFactor)+'X ')
			self.loadImage()
	
	def db_getImageID(self, imageStr):
		#Get from database the image id
		self.cursor.execute('SELECT id FROM images WHERE imagePath = ?',(imageStr,))
		return self.cursor.fetchone()[0]
	
	def db_getCategoryID(self, categoryStr):
		#Get from database the category id
		self.cursor.execute('SELECT id FROM categories WHERE categoryName = ?',(categoryStr,))
		return self.cursor.fetchone()[0]
	
	def db_getDataSetID(self, dataSetStr):
		#Select from database the dataset id
		self.cursor.execute('SELECT id FROM dataSets WHERE dataSetName = ?',(dataSetStr,))
		return self.cursor.fetchone()[0]

if __name__ == "__main__":
	root = tk.Tk()
	my_gui = tkteach(root)
	root.mainloop()