from tkinter import *
from main import *
from math import exp
from IA import *
import random
import time

# variables globales utilisees dans les fonctions

scoreJoueur1 = 0
scoreJoueur2 = 0
nomJoueur1 = "Joueur1"
nomJoueur2 = "Joueur2"
nomJoueurListe = [nomJoueur1, nomJoueur2]
nbVictoire = 5
nbCase = 8
minNbVictoire = 3
minNbCase = 3
maxNbVictoire = 6
maxNbCase = 15
tour = 1
joueurQuiCommence = 1
matriceJeu = None

# classe boutoon

class Bouton:

	global matriceJeu

	def __init__(self, pValeur='', pId=(-1,-1)): # fonction initialisation avec '' comme valeur par defaut

		if (type(pValeur)==str): # verifie que le parametre fourni correpond a une chaine de caractere
			self.valeur = pValeur # attribut qui correspond a la chaine de caractere affichee sur le bouton
			self.select = False # boolean qui permet de verifier si le bouton est selectionne
			self.bouton = None # attribut contenant l'objet tkinter cree
			self.largeur = 10 # int contenant la largeur du bouton
			self.fenetre = None # objet contenant la fenetre dans laquelle le bouton sera affiche
			self.nbClique = 0 # compteur qui compte le nombre de clique sur ce bouton
			self.id = pId
			self.joueur = 0

		else:
			pass

	# fonctions d'accession aux attributs

	def getValeur(self):
		return self.valeur

	def getSelect(self):
		return self.select

	def getBouton(self):
		return self.bouton

	def getLargeur(self):
		return self.width

	def getFenetre(self):
		return self.fenetre

	def getNbClique(self):
		return self.nbClique

	def getId(self):
		return self.id

	def getJoueur(self):
		return self.joueur

	# fonction de modification des attributs

	def setValeur(self, pValeur):
		self.valeur = pValeur

	def setSelect(self, pSelect):
		self.select = pSelect

	def setBouton(self, pBouton):
		self.bouton = pBouton

	def setLargeur(self, pLargeur):
		self.largeur = pLargeur

	def setFenetre(self, pFenetre):
		self.fenetre = pFenetre

	def setNbClique(self, pNbClique):
		self.nbClique = pNbClique

	def setId(self, pId):
		self.id = pId

	def setJoueur(self, pJoueur):
		self.joueur = pJoueur



	def placePack(self): # fonction qui place le bouton dans l'ordre lineaire du code (cf tkinter : le placement pack())
		self.bouton.pack(padx=10, pady=10, ipadx=5, ipady=5)

	def create(self, placement): # fonction qui fait appel a la fonction Button de tkinter pour creer un bouton avec les parametres voulus
		self.bouton = Button(self.fenetre, width=self.largeur, bg="grey", relief="raised", text=self.valeur, command=self.clique)
		if (placement): # en fonction du boolean placement, place le bouton ou laisse une autre methode de placement
			self.placePack()

	def clique(self): # fonction d'incrementation du nombre de clics sur un bouton

		global tour

		if (self.id!=(-1,-1)): #dans bouton damier
			if (((tour==1) or (estValide(self.id))) and (not self.select) and (self.nbClique==0)):
				self.select = not self.select
				self.bouton.config(relief="raised")
				if (tour%2==1 and tour!=0):
					if (joueurQuiCommence==1):
						self.apparenceJoueur1()
					else:
						self.apparenceJoueur2()
					self.joueur = -joueurQuiCommence
				elif (tour%2==0 and tour!=0):
					if (joueurQuiCommence==1):
						self.apparenceJoueur2()
					else:
						self.apparenceJoueur1()
					self.joueur = joueurQuiCommence
				matriceJeu[self.id[0]][self.id[1]] = self.joueur
				# print(matriceJeu)
				tour += 1
				self.nbClique += 1
		else:
			self.select = not self.select
			self.nbClique += 1

		#print("("+str(self.id[0])+":"+str(self.id[1])+")"+" - clique")

	def apparenceJoueur1(self):
		if (self.select):
			self.bouton.config(bg="white")

	def apparenceJoueur2(self):
		if (self.select):
			self.bouton.config(bg="black")

# classe Fenetre

class Fenetre:
	def __init__(self, pTitre, pGeometry, pResizable): # fonction d'initialisation avec trois parametres a passer
		self.titre = pTitre # attribut qui correspond au titre de la fenetre
		self.geometry = pGeometry # attribut qui correpond a la taille et eventuellement au placement de la fenetre
		self.resizable = pResizable # attribut boolean qui precise si la taille de la fenetre peut etre modifiee
		self.fenetre = None # attribut qui va contenir l'objet cree avec tkinter
		self.supprimer = False # attribut qui precise l'etat de suppression de la fenetre

	# fonctions d'accession aux attributs

	def getTitre(self):
		return self.titre

	def getGeometry(self):
		return self.geometry

	def getResizable(self):
		return self.resizable

	def getFenetre(self):
		return self.fenetre

	def getSupprimer(self):
		return self.supprimer

	# fonction de modification des attributs

	def setTitre(self, pTitre):
		self.titre = pTitre

	def setGeometry(self, pGeometry):
		self.geometry = pGeometry

	def setResizable(self, pResizable):
		self.resizable = pResizable


	def create(self): # fonction qui fait appel a la fonction Tk de tkinter pour creer une fenetre avec les parametres
		self.fenetre = Tk() # creation de l'objet fenetre
		self.fenetre.title(self.titre) # modification du titre de l'objet fenetre
		self.fenetre.geometry(self.geometry) # modification de la taille de la fenetre et de son placement
		self.fenetre.protocol("WM_DELETE_WINDOW", self.suppression) # mise en place d'un protocole qui fait appel a lal fonction suppression de la classe lorsque l'on utilise la croix pour quitter la fenetre

		if (not self.resizable): # modification des parametres de modification de la taille de la fenetre en fonction du boolean
			self.fenetre.resizable(width=False, height=False)

	def suppression(self): # fonction de suppression de la fenetre qui utilise un try pour eviter les exceptions
		self.supprimer = True # modification de l'attribut supprimer de la fenetre
		try:
			self.fenetre.destroy()
		except:
			pass

def parametres():

	# on utilisera les variables globales utiles a l'ensemble du programme car elles peuvent etre modifiées
	global nbVictoire, nbCase, maxNbVictoire, maxNbCase, minNbVictoire, minNbCase, nomJoueur1, nomJoueur2, listeBoutonDamier

	#print("Dans parametres")

	# creation des objets necessaires :
	#  - la fenetre
	#  - les differents textes a afficher
	#  - les differents boutons a afficher

	fenetreParametresGeometry = str(int(screensize[1]*0.7))+"x"+str(int(screensize[1]*0.7))+"+0+0"
	fenetreParametresObjet = Fenetre("PARAMETRES", fenetreParametresGeometry, False)
	fenetreParametresObjet.create()
	fenetreParametres = fenetreParametresObjet.getFenetre()
	fenetreParametres.config(bg="#4169E1")

	cadreFenetreParametres = Frame(fenetreParametres, width=int(screensize[1]*0.7), height=int(screensize[1]*0.7), bg="#4169E1")
	cadreFenetreParametres.grid(row=0, column=0)
	cadreFenetreParametres.grid_propagate(0)

	cadreFenetreParametres.grid_rowconfigure(0, weight=2)
	cadreFenetreParametres.grid_rowconfigure(1, weight=2)
	cadreFenetreParametres.grid_rowconfigure(2, weight=2)
	cadreFenetreParametres.grid_rowconfigure(3, weight=1)
	cadreFenetreParametres.grid_columnconfigure(0, weight=1)

	cadreParamDamier = Frame(cadreFenetreParametres, bd=4, bg="#4169E1", relief="groove")
	cadreParamDamier.grid(row=0, column=0, sticky="EWSN", padx=20, pady=20)
	cadreParamDamier.grid_rowconfigure(0, weight=2)
	cadreParamDamier.grid_rowconfigure(1, weight=3)
	cadreParamDamier.grid_columnconfigure(0, weight=1)
	cadreParamDamier.grid_columnconfigure(1, weight=3)
	cadreParamDamier.grid_columnconfigure(2, weight=1)

	cadreParamVictoire = Frame(cadreFenetreParametres, bd=4, bg="#4169E1", relief="groove")
	cadreParamVictoire.grid(row=1, column=0, sticky="EWSN", padx=20, pady=20)
	cadreParamVictoire.grid_rowconfigure(0, weight=2)
	cadreParamVictoire.grid_rowconfigure(1, weight=3)
	cadreParamVictoire.grid_columnconfigure(0, weight=1)
	cadreParamVictoire.grid_columnconfigure(1, weight=3)
	cadreParamVictoire.grid_columnconfigure(2, weight=1)

	cadreNomJoueur = Frame(cadreFenetreParametres, bd=4, bg="#4169E1", relief="groove")
	cadreNomJoueur.grid(row=2, column=0, sticky="EWSN", padx=20, pady=20)
	cadreNomJoueur.grid_rowconfigure(0, weight=2)
	cadreNomJoueur.grid_rowconfigure(1, weight=3)
	cadreNomJoueur.grid_columnconfigure(0, weight=3)
	cadreNomJoueur.grid_columnconfigure(1, weight=2)

	texteParametres1 = Label(cadreParamVictoire, text="Nombre de pions à aligner pour gagner :", bg="#4169E1", font=('calibri', 20, 'italic', 'underline'))
	texteParametres2 = Label(cadreParamDamier, text="Largeur du damier :", bg="#4169E1", font=('calibri', 20, 'italic', 'underline'))

	texteNombreVictoire = Label(cadreParamVictoire, text=str(nbVictoire), bg="#4169E1", font=('calibri', 20, 'bold'))
	texteNombreCase = Label(cadreParamDamier, text=str(nbCase), bg="#4169E1", font=('calibri', 20, 'bold'))

	texteJoueur1 = Label(cadreNomJoueur, text="Nom du Joueur 1 :", font=('calibri', 20, 'italic', 'underline'), bg="#4169E1")
	texteJoueur2 = Label(cadreNomJoueur, text="Nom du Joueur 2 :", font=('calibri', 20, 'italic', 'underline'), bg="#4169E1")

	entreeJoueur1 = Entry(cadreNomJoueur)
	entreeJoueur1.insert(END, nomJoueur1)
	entreeJoueur2 = Entry(cadreNomJoueur)
	entreeJoueur2.insert(END, nomJoueur2)

	boutonValider = Bouton("Valider les paramètres")
	boutonValider.setFenetre(cadreFenetreParametres)
	boutonValider.create(False)

	boutonMoins1 = Bouton("-")
	boutonMoins1.setFenetre(cadreParamVictoire)
	boutonMoins1.create(False)
	boutonMoins1Valeur = 0 # utilisation de compteur pour chaque bouton pour verifier le clic de chacun dans la boucle

	boutonPlus1 = Bouton("+")
	boutonPlus1.setFenetre(cadreParamVictoire)
	boutonPlus1.create(False)
	boutonPlus1Valeur = 0

	boutonMoins2 = Bouton("-")
	boutonMoins2.setFenetre(cadreParamDamier)
	boutonMoins2.create(False)
	boutonMoins2Valeur = 0

	boutonPlus2 = Bouton("+")
	boutonPlus2.setFenetre(cadreParamDamier)
	boutonPlus2.create(False)
	boutonPlus2Valeur = 0

	for bouton in [boutonMoins1, boutonMoins2, boutonPlus1, boutonPlus2]:
		bouton.getBouton().config(font=('calibri', 10, 'italic'), bg="#3184BB")

	boutonValider.getBouton().config(font=('calibri', 20, 'italic'), bg="#6eb53a", relief="flat")

	texteParametres1.grid(row=0, column=0, columnspan=3, sticky="EWSN", ipadx=5, ipady=5)
	boutonMoins1.getBouton().grid(row=1, column=0, ipadx=5, ipady=5)
	texteNombreVictoire.grid(row=1, column=1, sticky="EWSN", ipadx=5, ipady=5)
	boutonPlus1.getBouton().grid(row=1, column=2, ipadx=5, ipady=5)
	texteParametres2.grid(row=0, column=0, columnspan=3, sticky="EWSN", ipadx=5, ipady=5)
	boutonMoins2.getBouton().grid(row=1, column=0, ipadx=5, ipady=5)
	texteNombreCase.grid(row=1, column=1, sticky="EWSN", ipadx=5, ipady=5)
	boutonPlus2.getBouton().grid(row=1, column=2, ipadx=5, ipady=5)
	texteJoueur1.grid(row=0, column=0, sticky="W", ipadx=5, ipady=5)
	entreeJoueur1.grid(row=0, column=1, sticky="EWSN", ipadx=5, ipady=5)
	texteJoueur2.grid(row=1, column=0, sticky="W", ipadx=5, ipady=5)
	entreeJoueur2.grid(row=1, column=1, sticky="EWSN", ipadx=5, ipady=5)
	boutonValider.getBouton().grid(row=3, column=0, sticky="EWSN", ipadx=5, ipady=5)

	while (not boutonValider.getSelect() and not fenetreParametresObjet.getSupprimer()):

		#placement des differents objets a afficher

		# 4 tests pour verifier le clic de chacun des boutons avec la modification du texte concerne si les conditions sur les variables globales sont toujours valides
		if (boutonMoins1.getNbClique()>boutonMoins1Valeur):
			if (minNbVictoire<nbVictoire<=maxNbVictoire):
				nbVictoire-=1
				boutonMoins1Valeur+=1
			else:
				boutonMoins1.setNbClique(boutonMoins1.getNbClique()-1)

		if (boutonPlus1.getNbClique()>boutonPlus1Valeur):
			if (minNbVictoire<=nbVictoire<maxNbVictoire) and (nbVictoire<nbCase):
				nbVictoire+=1
				boutonPlus1Valeur+=1
			else:
				boutonPlus1.setNbClique(boutonPlus1.getNbClique()-1)

		if (boutonMoins2.getNbClique()>boutonMoins2Valeur):
			if (minNbCase<nbCase<=maxNbCase) and (nbVictoire<nbCase):
				nbCase-=1
				boutonMoins2Valeur+=1
			else:
				boutonMoins2.setNbClique(boutonMoins2.getNbClique()-1)

		if (boutonPlus2.getNbClique()>boutonPlus2Valeur):
			if (minNbCase<=nbCase<maxNbCase):
				nbCase+=1
				boutonPlus2Valeur+=1
			else:
				boutonPlus2.setNbClique(boutonPlus2.getNbClique()-1)

		#modification des textes concernes
		texteNombreVictoire.config(text=str(nbVictoire))
		texteNombreCase.config(text=str(nbCase))

		# try dans lequel on met a jour la fenetre
		try:
			fenetreParametres.update_idletasks()
			fenetreParametres.update()
		except:
			break

	try:
		if ((entreeJoueur1.get()!=len(entreeJoueur1.get())*' ') and (len(entreeJoueur1.get())<=20)):
			nomJoueur1 = entreeJoueur1.get()

		if ((entreeJoueur2.get()!=len(entreeJoueur2.get())*' ') and (len(entreeJoueur2.get())<=20)):
			nomJoueur2 = entreeJoueur2.get()

		listeBoutonDamier = [[Bouton('', (i,j)) for j in range(nbCase)] for i in range(nbCase)]
		nomJoueurListe = [nomJoueur1, nomJoueur2]
	except Exception:
		pass

	# supression de la fenetre lorsque l'on n'est plus dans la boucle
	fenetreParametresObjet.suppression()

	return nbCase

def informations():

	#print("Dans informations.")

	fenetreInformationsGeometry = str(int(screensize[1]*0.7))+"x"+str(int(screensize[1]*0.7))+"+0+0"

	fenetreInformationsObjet = Fenetre("INFORMATIONS", fenetreInformationsGeometry, False)
	fenetreInformationsObjet.create()
	fenetreInformations = fenetreInformationsObjet.getFenetre()

	cadreFenetreInfos = Frame(fenetreInformations, width=int(screensize[1]*0.7), height=int(screensize[1]*0.7), bg="#4169E1")
	cadreFenetreInfos.grid(row=0, column=0)
	cadreFenetreInfos.grid_propagate(0)

	cadreFenetreInfos.grid_rowconfigure(0, weight=1)
	cadreFenetreInfos.grid_rowconfigure(1, weight=3)
	cadreFenetreInfos.grid_rowconfigure(2, weight=2)
	cadreFenetreInfos.grid_columnconfigure(0, weight=1)

	cadreTexteTitreInfo = Frame(cadreFenetreInfos, bd=4, bg="black", relief="groove")
	cadreTexteTitreInfo.grid(row=0, column=0, sticky="EWSN", padx=20, pady=20)
	cadreTexteTitreInfo.grid_rowconfigure(0, weight=1)
	cadreTexteTitreInfo.grid_columnconfigure(0, weight=1)

	cadreTexteRegle = Frame(cadreFenetreInfos, bd=4, bg="black", relief="groove")
	cadreTexteRegle.grid(row=1, column=0, sticky="EWSN", padx=20, pady=20)
	cadreTexteRegle.grid_rowconfigure(0, weight=1)
	cadreTexteRegle.grid_rowconfigure(1, weight=5)
	cadreTexteRegle.grid_columnconfigure(0, weight=1)

	cadreTexteAuteurs = Frame(cadreFenetreInfos, bd=4, bg="black", relief="groove")
	cadreTexteAuteurs.grid(row=2, column=0, sticky="EWSN", padx=20, pady=20)
	cadreTexteAuteurs.grid_rowconfigure(0, weight=1)
	cadreTexteAuteurs.grid_columnconfigure(0, weight=1)

	texteInformation = Label(cadreTexteTitreInfo, text="Informations sur le jeu", font=('calibri', 20, 'bold'), bg="#4169E1")
	texteInformation.grid(row=0, column=0, sticky="EWSN")

	texteTitreRegle = Label(cadreTexteRegle, text="Règle du jeu", font=('calibri', 16, 'italic', 'underline'), bg="#4169E1")
	texteTitreRegle.grid(row=0, column=0, sticky="EWSN")

	texteRegle = "Le but du jeu est d'aligner horizontalement, verticalement ou en diagonal "+str(nbVictoire)+" cases de votre couleur (blanc ou noir). Le jeu se joue au tour par tour, le premier joueur étant tiré aléatoirement; à chaque tour vous ne pouvez placer vos cases qu'en contact avec les votres ou celles de l'adversaire (8 cases autour) sauf au premier tour."
	texteRegleLabel = Label(cadreTexteRegle, text=texteRegle, font=('calibri', 12), bg="#4169E1", wraplength=int(screensize[1]*0.6), justify="left")
	texteRegleLabel.grid(row=1, column=0, sticky="EWSN", ipadx=5, ipady=5)

	texteAuteurs = "Le projet a été réalisé par :\n\nPRIOU Roger\nSURGET Jérémy\nTHAK Victor"
	texteAuteursLabel = Label(cadreTexteAuteurs, text=texteAuteurs, font=('calibri', 12), bg="#4169E1", wraplength=int(screensize[1]*0.6), justify="center")
	texteAuteursLabel.grid(row=0, column=0, sticky="EWSN", ipadx=5, ipady=5)

	while (True):
		try:
			fenetreInformations.update_idletasks()
			fenetreInformations.update()
		except:
			break

	fenetreInformationsObjet.suppression()

def updateBoutons():

	global listeBoutonDamier

	listeBoutonDamier = [[Bouton('', (i,j)) for j in range(nbCase)] for i in range(nbCase)]

def alea(listeChoix):

	currentTime = time.time()
	randomObject = random.Random()

	randomObject.seed(int(currentTime))

	return randomObject.choice(listeChoix)

def affichageDamier(listeBoutons, fenetre):

	for ligne in listeBoutons:
		for bouton in ligne:
			bouton.setFenetre(fenetre)
			bouton.setLargeur(6)
			bouton.create(False)
			bouton.getBouton().config(height=3, relief="sunken", bg="#3CB371")
			bouton.getBouton().grid(row=bouton.getId()[0], column=bouton.getId()[1], pady=0, padx=0, sticky="EWSNs")
			bouton.getBouton().grid_propagate(0)

def estValide(boutonId):

	boutonI = boutonId[0]
	boutonJ = boutonId[1]

	#print("dans test")
	#print(nbCase)
	#print("\n")
	#print([ligne for ligne in [[listeBoutonDamier[i][j].getSelect() for j in range(boutonJ-1, boutonJ+2) if ((boutonI, boutonJ)!=(i, j) and (0<=i<nbCase) and (0<=j<nbCase))] for i in range(boutonI-1, boutonI+2)] if True in ligne])
	#print("\n")

	return len([ligne for ligne in [[listeBoutonDamier[i][j].getSelect() for j in range(boutonJ-1, boutonJ+2) if ((boutonI, boutonJ)!=(i, j) and (0<=i<nbCase) and (0<=j<nbCase))] for i in range(boutonI-1, boutonI+2)] if True in ligne])>0

def testVictoireM(matrice, i, j, horizontal, vertical):

	vainqueur = 0

	for i2 in range(i):

		longueurMax = 1

		for j2 in range(1, j):

			pointAComparer1 = matrice[i2*horizontal+j2*vertical][j2*horizontal+i2*vertical]
			pointAComparer2 = matrice[i2*horizontal+(j2-1)*vertical][(j2-1)*horizontal+i2*vertical]

			if ((j-j2)>=(nbVictoire-longueurMax) and (pointAComparer1 in [-1, 1]) and (pointAComparer1==pointAComparer2)):

				if (longueurMax==0):
					longueurMax = 2
				else:
					longueurMax += 1
					vainqueur = pointAComparer1

			else:

				longueurMax = vainqueur = 0

			if (longueurMax==nbVictoire):
				return True

	return False

def testVictoire(matriceTest):

	# seriesJoueur1 = {x:0 for x in range(1,nbVictoire)}
	# seriesJoueur2 = {x:0 for x in range(1,nbVictoire)}

	matriceCalcul = [ [ matriceTest[i][j] for j in range(nbCase) ] for i in range(nbCase) ]

	matriceCalculHI = [ [ matriceTest[i][j] for j in range(nbCase-1, -1, -1) ] for i in range(nbCase) ]
	matriceCalculVI = [ [ matriceTest[i][j] for j in range(nbCase) ] for i in range(nbCase-1, -1, -1) ]
	matriceCalculDiagonal1 = [[-10 for j in range(2*nbCase-1)] for i in range(2*nbCase-1)]

	for i in range(len(matriceCalcul)):
		for j in range(len(matriceCalcul[i])):
			matriceCalculDiagonal1[i+j][(nbCase-1)+(j-i)] = matriceCalcul[i][j]

	matriceCalculDiagonal11 = []

	for i in range(nbVictoire-1, 2*nbCase-nbVictoire):

		ligne1 = []
		ligne2 = []

		for j in range(2*nbCase-1):

			if (matriceCalculDiagonal1[i][j] in [-1,1]):
				ligne1.append(matriceCalculDiagonal1[i][j])
			if (matriceCalculDiagonal1[j][i] in [-1,1]):
				ligne2.append(matriceCalculDiagonal1[j][i])

		while (len(ligne1)<nbCase):
			ligne1.append(-10)

		while (len(ligne2)<nbCase):
			ligne2.append(-10)

		matriceCalculDiagonal11.append(ligne1)
		matriceCalculDiagonal11.append(ligne2)



	iHorizontal = len(matriceCalculDiagonal11)

	matriceCalculDiagonal11I = [ [ matriceCalculDiagonal11[i][j] for j in range(nbCase-1, -1, -1) ] for i in range(iHorizontal) ]

	horizontal = testVictoireM(matriceCalcul, nbCase, nbCase, 1, 0)
	horizontalI = testVictoireM(matriceCalculHI, nbCase, nbCase, 1, 0)
	vertical = testVictoireM(matriceCalcul, nbCase, nbCase, 0, 1)
	verticalI = testVictoireM(matriceCalculVI, nbCase, nbCase, 0, 1)
	diagonal1 = testVictoireM(matriceCalculDiagonal11, iHorizontal, nbCase, 1, 0)
	diagonal1I = testVictoireM(matriceCalculDiagonal11I, iHorizontal, nbCase, 1, 0)

	return (vertical or horizontal or diagonal1)

def redemarrer():

	global tour

	fenetreRedemarrerObjetGeometry = str(int(screensize[1]*0.5))+"x"+str(int(screensize[1]*0.3))+"+0+0"
	fenetreRedemarrerObjet = Fenetre("QUESTION", fenetreRedemarrerObjetGeometry, False)
	fenetreRedemarrerObjet.create()
	fenetreRedemarrer = fenetreRedemarrerObjet.getFenetre()

	cadreFenetreRedemarrer = Frame(fenetreRedemarrer, width=int(screensize[1]*0.5), height=int(screensize[1]*0.3), bg="#4169E1", bd=5, relief="groove")
	cadreFenetreRedemarrer.grid(row=0, column=0)
	cadreFenetreRedemarrer.grid_propagate(0)
	cadreFenetreRedemarrer.grid_rowconfigure(0, weight=2)
	cadreFenetreRedemarrer.grid_rowconfigure(1, weight=1)
	cadreFenetreRedemarrer.grid_columnconfigure(0, weight=1)

	cadreReponse = Frame(cadreFenetreRedemarrer, bg="#4169E1", relief="flat")
	cadreReponse.grid(row=1, column=0, sticky="EWSN", padx=20, pady=20)
	cadreReponse.grid_rowconfigure(0, weight=1)
	cadreReponse.grid_columnconfigure(0, weight=1)
	cadreReponse.grid_columnconfigure(1, weight=1)

	texteQuestion = Label(cadreFenetreRedemarrer, text="Voulez-vous continuer ?", wraplength=int(screensize[1]*0.4), font=('calibri', 30, 'italic'), bg="#4169E1")
	texteQuestion.grid(row=0, column=0, sticky="EWSN", ipadx=5, ipady=5)

	boutonOui = Bouton('Oui \n Recommencer')
	boutonOui.setFenetre(cadreReponse)
	boutonOui.create(False)
	boutonOui.getBouton().config(font=('calibri', 14, 'bold'), bg="#6eb53a")
	boutonOui.getBouton().grid(row=0, column=0, ipadx=10, ipady=10)

	boutonNon = Bouton('Non \n Quitter')
	boutonNon.setFenetre(cadreReponse)
	boutonNon.create(False)
	boutonNon.getBouton().config(font=('calibri', 14, 'bold'), bg="#6eb53a")
	boutonNon.getBouton().grid(row=0, column=1, ipadx=10, ipady=10)

	while (not fenetreRedemarrerObjet.getSupprimer()) and (not boutonOui.getSelect()) and (not boutonNon.getSelect()):

		try:
			fenetreRedemarrer.update_idletasks()
			fenetreRedemarrer.update()
		except:
			return False

	if (boutonOui.getSelect()):
		updateBoutons()
		tour = 1
		fenetreRedemarrerObjet.suppression()
		return True

	fenetreRedemarrerObjet.suppression()

	return False

def demarrer(alreadyPlay):

	global joueurQuiCommence, matriceJeu, tour

	initParam(nbCase, nbVictoire)

	if True:

		matriceJeu = creationMatriceJeu()

		fenetreStartObjetGeometry = str(int(screensize[1]*0.9))+"x"+str(int(screensize[1]*0.9))+"+0+0"
		fenetreStartObjet = Fenetre("GOMOKU", fenetreStartObjetGeometry, False)
		fenetreStartObjet.create()
		fenetreStart = fenetreStartObjet.getFenetre()

		cadreFenetreStart = Frame(fenetreStart, width=int(screensize[1]*0.9), height=int(screensize[1]*0.9), bg="#4169E1")
		cadreFenetreStart.grid(row=0, column=0)
		cadreFenetreStart.grid_propagate(0)

		cadreFenetreStart.grid_rowconfigure(0, weight=1)
		cadreFenetreStart.grid_rowconfigure(1, weight=nbCase)
		cadreFenetreStart.grid_rowconfigure(2, weight=1)
		cadreFenetreStart.grid_columnconfigure(0, weight=2)
		cadreFenetreStart.grid_columnconfigure(1, weight=nbCase)
		cadreFenetreStart.grid_columnconfigure(2, weight=2)

		texteTour = "TOUR "+str(tour)
		texteStart = Label(cadreFenetreStart, text=texteTour, font=('calibri', 40, 'bold'), bg="#4169E1")
		texteStart.grid(ipady=10, row=0, column=0, columnspan=3)


		##print(cadreFenetreStart.grid_bbox())

		cadreJoueur1 = Frame(cadreFenetreStart, bd=0, bg="white", relief="flat")
		cadreJoueur1.grid(row=1, column=0, padx=10)

		cadreJoueur1.grid_rowconfigure(0, weight=1)
		cadreJoueur1.grid_rowconfigure(1, weight=1)
		cadreJoueur1.grid_columnconfigure(0, weight=1)

		cadreJoueur2 = Frame(cadreFenetreStart, bd=0, bg="black", relief="flat")
		cadreJoueur2.grid(row=1, column=2, padx=10)

		cadreJoueur2.grid_rowconfigure(0, weight=1)
		cadreJoueur2.grid_rowconfigure(1, weight=1)
		cadreJoueur2.grid_columnconfigure(0, weight=1)

		cadreDamier = Frame(cadreFenetreStart, bd=5, bg="#3CB371", relief="ridge")
		cadreDamier.grid(row=1, column=1)

		for i in range(nbCase):
			cadreDamier.grid_rowconfigure(i, weight=1)
			cadreDamier.grid_columnconfigure(i, weight=1)

		texteJoueur1 = Label(cadreJoueur1, text=nomJoueur1, font=('calibri', 14, 'italic'), bg="#4169E1")
		texteJoueur1.grid(ipady=10, row=0, column=0, sticky="EW")

		texteScoreJoueur1 = Label(cadreJoueur1, text="Score : "+str(scoreJoueur1), bg="#4169E1")
		texteScoreJoueur1.grid(ipady=10, row=1, column=0, sticky="EW")

		texteJoueur2 = Label(cadreJoueur2, text=nomJoueur2, font=('calibri', 14, 'italic'), bg="#4169E1")
		texteJoueur2.grid(ipady=10, row=0, column=0, sticky="EW")

		texteScoreJoueur2 = Label(cadreJoueur2, text="Score : "+str(scoreJoueur2), bg="#4169E1")
		texteScoreJoueur2.grid(ipady=10, row=1, column=0, sticky="EW")

		boutonQuitter = Bouton('Quitter')
		boutonQuitter.setFenetre(cadreFenetreStart)
		boutonQuitter.create(False)
		boutonQuitter.getBouton().config(bg="red", font=('calibri', 14, 'bold'))
		boutonQuitter.getBouton().grid(pady=20, row=2, column=1)

		affichageDamier(listeBoutonDamier, cadreDamier)

		if (not alreadyPlay):
			joueurQuiCommence = alea([-1,1])

		if (joueurQuiCommence==1):
			cadreJoueur1.config(bd=5, bg="white")
		else:
			cadreJoueur2.config(bd=5, bg="black")

		tourAncien = tour

	while (not fenetreStartObjet.getSupprimer() and not boutonQuitter.getSelect()):

		texteTour = "TOUR "+str(tour)
		texteStart.config(text=texteTour)

		if (tour%2==1 and joueurQuiCommence==-1) or (tour%2==0 and joueurQuiCommence==1):
			coordonnneesIA = start(matriceJeu, tour)
			matriceJeu[coordonnneesIA[0]][coordonnneesIA[1]] = -1
			listeBoutonDamier[coordonnneesIA[0]][coordonnneesIA[1]].clique()

		if (tour>tourAncien):
			if (tour%2==0):
				if (joueurQuiCommence==1):
					cadreJoueur1.config(bd=0)
					cadreJoueur2.config(bd=5, bg="black")
				else:
					cadreJoueur1.config(bd=5, bg="black")
					cadreJoueur2.config(bd=0)
			elif (tour%2!=0):
				if (joueurQuiCommence==1):
					cadreJoueur1.config(bd=5, bg="white")
					cadreJoueur2.config(bd=0)
				else:
					cadreJoueur1.config(bd=0)
					cadreJoueur2.config(bd=5, bg="white")

			testVictoireTMP = testVictoire(matriceJeu)

			if (testVictoireTMP):
				break
			tourAncien = tour

		try:
			fenetreStart.update_idletasks()
			fenetreStart.update()
		except:
			return False

	if (redemarrer()):
		joueurQuiCommence = -joueurQuiCommence
		fenetreStartObjet.suppression()
		demarrer(False)

	fenetreStartObjet.suppression()
	return False

# def ia(tourTMP, profondeur, matriceJeuIA, dico):

# 	print("""L'ordinateur est en train de réfléchir...""")

# 	if (profondeur==0):
# 		listePoids = [ poids for poids in dico.values() ]
# 		maxPoids = max(listePoids)
# 		minPoids = min(listePoids)
# 		print(dico)
# 		if ((tour+tourTMP-1)%2==0):
# 			if (joueurQuiCommence==1):
# 				for coord in dico.keys():
# 					if (dico[coord]==maxPoids):
# 						return coord
# 			else:
# 				for coord in dico.keys():
# 					if (dico[coord]==minPoids):
# 						return coord
# 		else:
# 			if (joueurQuiCommence==1):
# 				for coord in dico.keys():
# 					if (dico[coord]==maxPoids):
# 						return coord
# 			else:
# 				for coord in dico.keys():
# 					if (dico[coord]==minPoids):
# 						return coord

# 	dictionnaireCoordPoids = evalPossibilites(matriceJeuIA)

# 	for coordonnees in dictionnaireCoordPoids.keys():

# 		matriceTMP = matriceJeu

# 		if ((tour+tourTMP)%2==0):
# 			if (joueurQuiCommence==1):
# 				matriceTMP[coordonnees[0]][coordonnees[1]] = 1
# 			else:
# 				matriceTMP[coordonnees[0]][coordonnees[1]] = -1
# 		else:
# 			if (joueurQuiCommence==1):
# 				matriceTMP[coordonnees[0]][coordonnees[1]] = 1
# 			else:
# 				matriceTMP[coordonnees[0]][coordonnees[1]] = -1

# 		victoireTMP, seriesJoueur1TMP, seriesJoueur2TMP = testVictoire(matriceTMP)
# 		poids = 0

# 		for indice in range(1,nbVictoire):
# 			poids += exp(indice)*(seriesJoueur1TMP[indice]+seriesJoueur2TMP[indice])

# 		if victoireTMP:
# 			if ((tour+tourTMP)%2==0):
# 				if (joueurQuiCommence==1):
# 					poids += 10000
# 				else:
# 					poids -= 10000
# 			else:
# 				if (joueurQuiCommence==1):
# 					poids += 10000
# 				else:
# 					poids -= 10000

# 		dictionnaireCoordPoids[coordonnees] = poids

# 	print(dictionnaireCoordPoids)


# 	ia(tourTMP+1, profondeur-1, matriceTMP, dictionnaireCoordPoids)
# 	#
# 	# print("\n\n")

# def evalPossibilites(matriceCalcul):

# 	dictionnaireCoordPoids = {}

# 	for i in range(nbCase):
# 		for j in range(nbCase):
# 			coord = (i,j)
# 			if (estValide(coord) and matriceCalcul[i][j]==-10):
# 				dictionnaireCoordPoids[coord] = 0

# 	# print(dictionnaireCoordPoids)

# 	return dictionnaireCoordPoids

def creationMatriceJeu():

	matriceJeuRetour = [[-10 for j in range(nbCase)] for i in range(nbCase)]

	for i in range(nbCase):
		for j in range(nbCase):
			if (listeBoutonDamier[i][j].getSelect()):
				matriceJeuRetour[i][j] = listeBoutonDamier[i][j].getJoueur()

	return matriceJeuRetour

# listeBoutonDamier = [[Bouton('', (i,j)) for j in range(nbCase)] for i in range(nbCase)]
listeBoutonDamier = [[Bouton(str(i)+" | "+str(j), (i,j)) for j in range(nbCase)] for i in range(nbCase)]