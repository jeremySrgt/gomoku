# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 15:49:12 2019

v1.2 : amélioration de l'IA pour qu'elle se rapproche directement vers la victoire
blocage de la construction de l'arbre quand la première occurrence d'une victoire (ordi) apparaît
blocage de la construction -> on ne va pas plus loin en profondeur dans l'arbre
exp() -> constante évolutive
"""

import numpy as np
from time import time

nbCase = 8
nbVictoire = 4
matriceJeu = [ [-10 for x in range(nbCase)] for y in range(nbCase) ]
joueur1 = 1
joueur2 = -1
tour = 0
profondeur = 4
profondeurVictoire = 4

class ABR:
	def __init__(self, pRacine={}, pFils=[], pCanExpand=True):
		self.racine = pRacine
		self.fils = pFils
		self.canExpand = pCanExpand

	def getRacine(self):
		return self.racine

	def getFils(self):
		return self.fils

	def getCanExpand(self):
		return self.canExpand

	def setRacine(self, pRacine):
		self.racine = pRacine

	def setFils(self, pFils):
		self.fils = pFils

	def setCanExpand(self, pCanExpand):
		self.canExpand = pCanExpand

	def ajoutFils(self, pFils):
		self.fils.append(pFils)

	def updatePoidsRacine(self, pPoids):
		for coord in self.racine.keys():
			self.racine[coord] = pPoids

def afficheMatrice():

    ligneString = ' ' + '_'*5*nbCase

    for i in range(nbCase):

        print(ligneString + '\n')

        for j in range(nbCase):

            if (len(str(matriceJeu[i][j]))==3):
                char = str(matriceJeu[i][j])
            elif (len(str(matriceJeu[i][j]))==2):
                char = ' ' + str(matriceJeu[i][j])
            else:
                char = ' ' + str(matriceJeu[i][j]) + ' '

            print('|'+char, end=' ')
        print('|')
    print(ligneString)

def initMatriceJeu():

    global matriceJeu

    matriceJeu = [ [ -10 for j in range(nbCase) ] for i in range(nbCase) ]

def updateMatrice(coord, joueur):

    global matriceJeu

    try:
        matriceJeu[coord[0]][coord[1]] = joueur
    except IndexError:
        return False
    else:
        return True

def estValide(coord, matriceTMP):

    X = coord[0]
    Y = coord[1]

    if (tour==1):
        return True
    elif (matriceTMP[X][Y]!=-10):
    	return False

    listeSolution = [[matriceTMP[i][j] for j in range(Y-1,Y+2) if ((0<=i<nbCase) and (0<=j<nbCase) and (i, j)!=(X, Y))] for i in range(X-1, X+2)]

    for ligne in listeSolution:
        if (-1 in ligne) or (1 in ligne):
            return True

    return False

def testVictoireM(matrice, i, j, horizontal, vertical):

	vainqueur = 0
	seriesJoueur1TMP = {x:0 for x in range(1,nbVictoire)}
	seriesJoueur2TMP = {x:0 for x in range(1,nbVictoire)}

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

			elif (j-j2)>=(nbVictoire-longueurMax):

				blocageLigne = True
				try:
					pointAComparer3 = matrice[i2*horizontal+(j2+1)*vertical][(j2+1)*horizontal+i2*vertical]
					blocageLigne = (pointAComparer2==-1*pointAComparer3)
				except IndexError:
					blocageLigne = False
				finally:
					if (not blocageLigne):
						if (vainqueur==1):
							seriesJoueur1TMP[longueurMax] += 1
						elif (vainqueur==-1):
							seriesJoueur2TMP[longueurMax] += 1

				longueurMax = vainqueur = 0

			if (longueurMax==nbVictoire):
				return True, seriesJoueur1TMP, seriesJoueur2TMP

	return False, seriesJoueur1TMP, seriesJoueur2TMP

def testVictoire(matriceTest):

	seriesJoueur1 = {x:0 for x in range(1,nbVictoire)}
	seriesJoueur2 = {x:0 for x in range(1,nbVictoire)}

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

	horizontal, horizontal1, horizontal2 = testVictoireM(matriceCalcul, nbCase, nbCase, 1, 0)
	horizontalI, horizontal1I, horizontal2I = testVictoireM(matriceCalculHI, nbCase, nbCase, 1, 0)
	vertical, vertical1, vertical2 = testVictoireM(matriceCalcul, nbCase, nbCase, 0, 1)
	verticalI, vertical1I, vertical2I = testVictoireM(matriceCalculVI, nbCase, nbCase, 0, 1)
	diagonal1, diagonal11, diagonal12 = testVictoireM(matriceCalculDiagonal11, iHorizontal, nbCase, 1, 0)
	diagonal1I, diagonal11I, diagonal12I = testVictoireM(matriceCalculDiagonal11I, iHorizontal, nbCase, 1, 0)

	for key in range(1,nbVictoire):
		seriesJoueur1[key] += (horizontal1[key]+horizontal1I[key]+vertical1[key]+vertical1I[key]+diagonal11[key]+diagonal11I[key])
		seriesJoueur2[key] += (horizontal2[key]+horizontal2I[key]+vertical2[key]+vertical2I[key]+diagonal12[key]+diagonal12I[key])

	return (vertical or horizontal or diagonal1), seriesJoueur1, seriesJoueur2

def tourJoueur():

    global tour

    coord = input("Coordonnées i,j : ")

    try:
        valeurRetour  = [ int(point) for point in coord.split(',') ]
    except ValueError:
        print('Entrée invalide veuillez recommencer')
        tourJoueur()
    else:
        tour += 1
        return valeurRetour

def tourIA():

	global tour

	tour += 1

	dictionnaireCoordPoids = evalPossibilites(matriceJeu)
	abrFinal = ABR({None:0},[],True)

	for possibilite in dictionnaireCoordPoids.keys():

		matriceTMP = np.copy(matriceJeu)

		if (tour%2==0):
			matriceTMP[possibilite[0]][possibilite[1]] = -1
		else:
			matriceTMP[possibilite[0]][possibilite[1]] = 1

		abrTMP = ABR({possibilite:0},[],True)
		abrFinal.ajoutFils(abrTMP)
		IA(tour+1, profondeur-1, matriceTMP, abrTMP)

	poidsOpti = float('inf')
	coordRetour = tuple

	for fils in abrFinal.getFils():
		for filsCoord in fils.getRacine().keys():
			if (fils.getRacine()[filsCoord]<poidsOpti):
				poidsOpti = fils.getRacine()[filsCoord]
				coordRetour = filsCoord
	# affichageABR(abrFinal)


	return coordRetour

# def affichageABR(abr):

# 	print(abr.getRacine())
# 	for fils in abr.getFils():
# 		affichageABR(fils)

def IA(tourTMP, profondeur, matriceTMP, abrTMP):

	global profondeurVictoire

	dictionnaireTMP = evalPossibilites(matriceTMP)

	if (profondeurVictoire>=profondeur>0 and abrTMP.getCanExpand()):

		for possibilite in dictionnaireTMP.keys():

			matriceTMP2 = np.copy(matriceTMP)

			if ((tour+tourTMP)%2==0):
				matriceTMP2[possibilite[0]][possibilite[1]] = -1
			else:
				matriceTMP2[possibilite[0]][possibilite[1]] = 1

			victoireTMP, seriesJoueur1TMP, seriesJoueur2TMP = testVictoire(matriceTMP2)
			poids = calculPoids(seriesJoueur1TMP, seriesJoueur2TMP, victoireTMP, tourTMP)

			if (abs(5-profondeur)==profondeurVictoire):
				canExpandTMP = False
			else:
				canExpandTMP = True

			if (victoireTMP and (tour+tourTMP)%2==0):
				if (abs(5-profondeur)<profondeurVictoire):
					profondeurVictoire = abs(5-profondeur)
					canExpandTMP = False

			abrTMP2 = ABR({possibilite:poids},[], canExpandTMP)
			abrTMP.ajoutFils(abrTMP2)

			IA(tourTMP+1, profondeur-1, matriceTMP2, abrTMP2)

			del victoireTMP, seriesJoueur1TMP, seriesJoueur2TMP, poids, matriceTMP2

	poidsPere = 0

	if (tour+tourTMP%2==0):
		mini = True
		maxi = False
	else:
		mini = False
		maxi = True

	for fils in abrTMP.getFils():
		for filsPoids in fils.getRacine().values():
			if (maxi and (filsPoids>poidsPere)) or (mini and (filsPoids<poidsPere)):
				poidsPere = filsPoids

	abrTMP.updatePoidsRacine(poidsPere)

def calculPoids(seriesJoueur1TMP, seriesJoueur2TMP, victoireTMP, tourTMP):

	poids = 0

	for indice in range(2,nbVictoire):
		poids += (10**nbVictoire)*(seriesJoueur1TMP[indice]+seriesJoueur2TMP[indice])

	if victoireTMP:
		if ((tour+tourTMP)%2==0):
			poids -= 10**nbVictoire
		else:
			poids += 10**nbVictoire

	return poids

def evalPossibilites(matriceCalcul):

	dictionnaireCoordPoids = {}

	for i in range(nbCase):
		for j in range(nbCase):

			coord = (i,j)

			if (estValide(coord, matriceCalcul) and matriceCalcul[i][j]==-10):
				dictionnaireCoordPoids[coord] = 0

	return dictionnaireCoordPoids

def main():

    global tour

    print('\n\n')

    if ( tour >= (2*nbVictoire-1)):
    	victoire, serieJoueur1TMP, serieJoueur2TMP = testVictoire(matriceJeu)
    	if ( victoire ):
    		return

    if (tour%2==0):
    	print("JOUEUR 1")
    	coordJoueur = tourJoueur()
    	if ( not estValide(coordJoueur, matriceJeu) ):
    		tour -= 1
    	else:
    		updateMatrice(coordJoueur, joueur1)
    else:
    	time1 = time()
    	coordRetour = tourIA()
    	timeDelta = int(time() - time1)
    	if ( not estValide(coordRetour, matriceJeu) ):
    		tour -= 1
    	else:
    		updateMatrice(coordRetour, joueur2)
    	print("JOUEUR 2\n\nTemps de réflexion : "+str(timeDelta)+" secondes")

    afficheMatrice()

    main()

if __name__ == '__main__':
    initMatriceJeu()
    main()

# def start(pMatriceJeu, pTour):

# 	global matriceJeu, tour

	
# 	matriceJeu = pMatriceJeu
# 	tour = pTour
	
# 	return tourIA()

# def initParam(pNbCase, pNbVictoire):
	
# 	global nbCase, nbVictoire

# 	nbCase = pNbCase
# 	nbVictoire = pNbVictoire