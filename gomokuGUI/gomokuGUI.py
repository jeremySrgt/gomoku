# coding: utf-8

try:
	from tkinter import *
	from fonctions import *
	from math import exp
	import ctypes, random, time
except ImportError as error:
	print("Un ou plusieurs module(s) et/ou fonction(s) sont manquant(s).")
	exit()
except Exception as error:
	print("L'erreur : \n"+str(error)+"\nlors de la compilation du programme.")
	exit()

user32 = ctypes.windll.user32
screensize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def main():

	##print("Dans main.")

	# creation fenetreAccueil accueil

	fenetreAccueilObjet = Fenetre("GOMOKU", "300x270+0+0", False)
	fenetreAccueilObjet.create()
	fenetreAccueil = fenetreAccueilObjet.getFenetre()
	fenetreAccueil.config(bg="#4169E1")

	# creation boutons accueil

	boutonDemarrer = Bouton("Démarrer")
	boutonDemarrer.setFenetre(fenetreAccueil)
	boutonDemarrer.create(True)

	boutonParametres = Bouton("Paramètres")
	boutonParametres.setFenetre(fenetreAccueil)
	boutonParametres.create(True)

	boutonInformations = Bouton("Informations")
	boutonInformations.setFenetre(fenetreAccueil)
	boutonInformations.create(True)

	for bouton in [boutonDemarrer, boutonParametres, boutonInformations]:
		bouton.getBouton().config(font=('calibri', 20, 'italic'), bg="#3184BB")

	# boucle d'attente que l'utilisateur clique sur un bouton

	while (not fenetreAccueilObjet.getSupprimer()):

		while (not boutonDemarrer.getSelect() and not boutonParametres.getSelect() and not boutonInformations.getSelect()):
			try:
				fenetreAccueil.update_idletasks()
				fenetreAccueil.update()
			except:
				break

	# on verifie sur quel bouton l'utilisateur a clique apres avoir supprimer la fenetreAccueil

		if (boutonParametres.getSelect()):
			nbCase = parametres()
			boutonParametres.setSelect(False)
			updateBoutons()
			from fonctions import nomJoueur1, nomJoueur2, listeBoutonDamier
		if (boutonInformations.getSelect()):
			informations()
			boutonInformations.setSelect(False)
		if (boutonDemarrer.getSelect()):
			while(demarrer(True)):
				pass
			exit()


if __name__ == '__main__':
	main()
