# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 15:49:12 2019

v1.2 : amélioration de l'IA pour qu'elle se rapproche directement vers la victoire
blocage de la construction de l'arbre quand la première occurrence d'une victoire (ordi) apparaît
blocage de la construction -> on ne va pas plus loin en profondeur dans l'arbre
exp() -> constante évolutive

@author: Roger
"""

import numpy as np

nbCase = 0
nbVictoire = 0
matriceJeu = None
joueur1 = 1
joueur2 = -1
tour = 0
profondeur = 2
profondeurVictoire = 2

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

# def afficheMatrice():

#     ligneString = ' ' + '_'*5*nbCase

#     for i in range(nbCase):

#         print(ligneString + '\n')

#         for j in range(nbCase):

#             if (len(str(matriceJeu[i][j]))==3):
#                 char = str(matriceJeu[i][j])
#             elif (len(str(matriceJeu[i][j]))==2):
#                 char = ' ' + str(matriceJeu[i][j])
#             else:
#                 char = ' ' + str(matriceJeu[i][j]) + ' '

#             print('|'+char, end=' ')
#         print('|')
#     print(ligneString)

# def initMatriceJeu():

#     global matriceJeu

#     matriceJeu = [ [ -10 for j in range(nbCase) ] for i in range(nbCase) ]

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

def diagonalM(matrice):

	vainqueur = 0
	testBlocageAvant = False
	blocageAvant = [False, tuple]
	blocageApres = [False, tuple]
	tailleBlocage = [x for x in range(2, nbVictoire)]
	serieBlocage = {}

	for k in range(nbCase-1):
		longueurMax = 1
		i2 = nbCase-2
		for j2 in range(k-(nbVictoire//2), k+(nbVictoire-(nbVictoire//2))):

			pointAComparer1 = matrice[j2][i2]
			pointAComparer2 = matrice[j2+1][i2-1]

			if j2 in range(nbCase):

				if (abs(nbCase-j2)>=(nbVictoire-longueurMax)):


					if (pointAComparer1==pointAComparer2) and (pointAComparer1 in [-1, 1]):

						if (not testBlocageAvant):
							try:
								pointAComparer0 = matrice[j2-1][i2+1]
								blocageAvant = [(not (pointAComparer0==-10)), (j2-1, i2+1)]
							except IndexError:
								pass
							finally:
								testBlocageAvant = True	

						longueurMax += 1
						vainqueur = pointAComparer1

					else:

						try:
							pointAComparer3 = matrice[j2+2][i2-2]
							blocageApres = [ (pointAComparer2==-1*pointAComparer3), (j2+2, i2-2)]
						except IndexError:
							pass
						finally:

							if (not blocageApres[0]):

								if (longueurMax in tailleBlocage):

									if (not blocageAvant[0]):

										if (blocageAvant[1] not in serieBlocage.keys()):
											serieBlocage[blocageAvant[1]] = 0
										if (blocageApres[1] not in serieBlocage.keys()):
											serieBlocage[blocageApres[1]] = 0

										serieBlocage[blocageAvant[1]]=vainqueur*10**(longueurMax+1)
										serieBlocage[blocageApres[1]]=vainqueur*10**(longueurMax+1)

									else:

										if (blocageApres[1] not in serieBlocage.keys()):
											serieBlocage[blocageApres[1]] = 0

										serieBlocage[blocageApres[1]]=vainqueur*10**(longueurMax+1)

							else:

								if (longueurMax in tailleBlocage):

									if (not blocageAvant[0]):

										if (blocageAvant[1] not in serieBlocage.keys()):
											serieBlocage[blocageAvant[1]] = 0

										serieBlocage[blocageAvant[1]]=vainqueur*10**(longueurMax+1)

					longueurMax = vainqueur = 0
					blocageAvant = [False, tuple]
					blocageApres = [False, tuple]
					testBlocageAvant = False

				else:
					break

				if (longueurMax==nbVictoire):
					return serieBlocage

		i2 -= 1

	return serieBlocage

def diagonalD(matrice):

	vainqueur = 0
	testBlocageAvant = False
	blocageAvant = [False, tuple]
	blocageApres = [False, tuple]
	tailleBlocage = [x for x in range(2, nbVictoire)]
	serieBlocage = {}

	for k in range(nbCase-1):
		longueurMax = 1
		i2 = 0
		for j2 in range(k-(nbVictoire//2), k+(nbVictoire-(nbVictoire//2))):

			pointAComparer1 = matrice[j2][i2]
			pointAComparer2 = matrice[j2+1][i2+1]

			if j2 in range(nbCase):

				if (abs(nbCase-j2)>=(nbVictoire-longueurMax)):


					if (pointAComparer1==pointAComparer2) and (pointAComparer1 in [-1, 1]):

						if (not testBlocageAvant):
							try:
								pointAComparer0 = matrice[j2-1][i2-1]
								blocageAvant = [(not (pointAComparer0==-10)), (j2-1, i2-1)]
							except IndexError:
								pass
							finally:
								testBlocageAvant = True	

						longueurMax += 1
						vainqueur = pointAComparer1

					else:

						try:
							pointAComparer3 = matrice[j2+2][i2+2]
							blocageApres = [ (pointAComparer2==-1*pointAComparer3), (j2+2, i2+2)]
						except IndexError:
							pass
						finally:

							if (not blocageApres[0]):

								if (longueurMax in tailleBlocage):

									if (not blocageAvant[0]):

										if (blocageAvant[1] not in serieBlocage.keys()):
											serieBlocage[blocageAvant[1]] = 0
										if (blocageApres[1] not in serieBlocage.keys()):
											serieBlocage[blocageApres[1]] = 0

										serieBlocage[blocageAvant[1]]=vainqueur*10**(longueurMax+1)
										serieBlocage[blocageApres[1]]=vainqueur*10**(longueurMax+1)

									else:

										if (blocageApres[1] not in serieBlocage.keys()):
											serieBlocage[blocageApres[1]] = 0

										serieBlocage[blocageApres[1]]=vainqueur*10**(longueurMax+1)

							else:

								if (longueurMax in tailleBlocage):

									if (not blocageAvant[0]):

										if (blocageAvant[1] not in serieBlocage.keys()):
											serieBlocage[blocageAvant[1]] = 0

										serieBlocage[blocageAvant[1]]=vainqueur*10**(longueurMax+1)

					longueurMax = vainqueur = 0
					blocageAvant = [False, tuple]
					blocageApres = [False, tuple]
					testBlocageAvant = False

				else:
					break

				if (longueurMax==nbVictoire):
					return serieBlocage

		i2 += 1

	return serieBlocage

def testVictoireM(matrice, i, j, horizontal, vertical, testBlocage): # on suppose ordi -> '-'

	vainqueur = 0
	seriesJoueur1TMP = {x:0 for x in range(1,nbVictoire)}
	seriesJoueur2TMP = {x:0 for x in range(1,nbVictoire)}
	testBlocageAvant = False
	blocageAvant = [False, tuple]
	blocageApres = [False, tuple]
	tailleBlocage = [x for x in range(2, nbVictoire)]
	serieBlocage = {}

	for i2 in range(i):

		longueurMax = 1

		for j2 in range(1, j):

			pointAComparer1 = matrice[i2*horizontal+j2*vertical][j2*horizontal+i2*vertical]
			pointAComparer2 = matrice[i2*horizontal+(j2-1)*vertical][(j2-1)*horizontal+i2*vertical]

			if ((j-j2)>=(nbVictoire-longueurMax)):

				if ((pointAComparer1 in [-1, 1]) and (pointAComparer1==pointAComparer2)):

					if (not testBlocageAvant):
						try:
							pointAComparer0 = matrice[i2*horizontal+(j2-2)*vertical][(j2-2)*horizontal+i2*vertical]
							blocageAvant = [(not (pointAComparer0==-10)), (i2*horizontal+(j2-2)*vertical , (j2-2)*horizontal+i2*vertical)]
						except IndexError:
							pass
						finally:
							testBlocageAvant = True

					longueurMax += 1
					vainqueur = pointAComparer1

				else: 

					try:
						pointAComparer3 = matrice[i2*horizontal+(j2+1)*vertical][(j2+1)*horizontal+i2*vertical]
						blocageApres = [ (pointAComparer2==-1*pointAComparer3), (i2*horizontal+(j2+1)*vertical , (j2+1)*horizontal+i2*vertical)]
					except IndexError:
						pass
					finally:
						if (not blocageApres[0]):

							if (vainqueur==1):
								seriesJoueur1TMP[longueurMax] += 1
							elif (vainqueur==-1):
								seriesJoueur2TMP[longueurMax] += 1

							if (longueurMax in tailleBlocage):

								if (not blocageAvant[0]):

									if (blocageAvant[1] not in serieBlocage.keys()):
										serieBlocage[blocageAvant[1]] = 0
									if (blocageApres[1] not in serieBlocage.keys()):
										serieBlocage[blocageApres[1]] = 0

									serieBlocage[blocageAvant[1]]=vainqueur*10**(longueurMax)
									serieBlocage[blocageApres[1]]=vainqueur*10**(longueurMax)

								else:

									if (blocageApres[1] not in serieBlocage.keys()):
										serieBlocage[blocageApres[1]] = 0

									serieBlocage[blocageApres[1]]=vainqueur*10**(longueurMax)

						else:

							if (longueurMax in tailleBlocage):

								if (not blocageAvant[0]):

									if (blocageAvant[1] not in serieBlocage.keys()):
										serieBlocage[blocageAvant[1]] = 0

									serieBlocage[blocageAvant[1]]=vainqueur*10**(longueurMax)

					longueurMax = vainqueur = 0
					blocageAvant = [False, tuple]
					blocageApres = [False, tuple]
					testBlocageAvant = False

			else:
				break

			if (longueurMax==nbVictoire):
				return True, seriesJoueur1TMP, seriesJoueur2TMP, serieBlocage

	return False, seriesJoueur1TMP, seriesJoueur2TMP, serieBlocage

def testVictoire(matriceTest, testBlocage):

	seriesJoueur1 = {x:0 for x in range(2,nbVictoire)}
	seriesJoueur2 = {x:0 for x in range(2,nbVictoire)}

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

	horizontal, horizontal1, horizontal2, horizontalBlocage = testVictoireM(matriceCalcul, nbCase, nbCase, 1, 0, testBlocage)
	horizontalI, horizontal1I, horizontal2I, horizontalIBlocage = testVictoireM(matriceCalculHI, nbCase, nbCase, 1, 0, testBlocage)
	vertical, vertical1, vertical2, verticalBlocage = testVictoireM(matriceCalcul, nbCase, nbCase, 0, 1, testBlocage)
	verticalI, vertical1I, vertical2I, verticalIBlocage = testVictoireM(matriceCalculVI, nbCase, nbCase, 0, 1, testBlocage)
	diagonal1, diagonal11, diagonal12, diagonal1Blocage = testVictoireM(matriceCalculDiagonal11, iHorizontal, nbCase, 1, 0, testBlocage)
	diagonal1I, diagonal11I, diagonal12I, diagonal1IBlocage = testVictoireM(matriceCalculDiagonal11I, iHorizontal, nbCase, 1, 0, testBlocage)

	for key in range(2,nbVictoire):
		seriesJoueur1[key] += (horizontal1[key]+horizontal1I[key]+vertical1[key]+vertical1I[key]+diagonal11[key]+diagonal11I[key])
		seriesJoueur2[key] += (horizontal2[key]+horizontal2I[key]+vertical2[key]+vertical2I[key]+diagonal12[key]+diagonal12I[key])

	serieBlocageRetour = {}

	if testBlocage:

		diagonal1Blocage = diagonalD(matriceTest)
		diagonal2Blocage = diagonalM(matriceTest)

		listeBlocage = [horizontalBlocage, horizontalIBlocage, verticalBlocage, verticalIBlocage, diagonal1Blocage, diagonal2Blocage]

		for serie in listeBlocage:
			for key in serie.keys():
				try:
					serieBlocageRetour[key] += serie[key]
				except Exception:
					serieBlocageRetour[key] = 0
					serieBlocageRetour[key] += serie[key]

	return (vertical or horizontal or diagonal1), seriesJoueur1, seriesJoueur2, serieBlocageRetour

# def tourJoueur():

#     global tour

#     coord = input("Coordonnées i,j : ")

#     try:
#         valeurRetour  = [ int(point) for point in coord.split(',') ]
#     except ValueError:
#         print('Entrée invalide veuillez recommencer')
#         tourJoueur()
#     else:
#         tour += 1
#         return valeurRetour

def tourIA():

	global tour, profondeurVictoire

	tour += 1
	profondeurVictoire = profondeur

	dictionnaireCoordPoids = evalPossibilites(matriceJeu)
	serieBlocageTMP = testVictoire(matriceJeu, True)[3]
	abrFinal = ABR({None:0},[],True)

	for possibilite in dictionnaireCoordPoids.keys():

		matriceTMP = np.copy(matriceJeu)

		if (tour%2==0):
			matriceTMP[possibilite[0]][possibilite[1]] = -1
		else:
			matriceTMP[possibilite[0]][possibilite[1]] = 1

		try:
			abrTMP = ABR({possibilite:0},[],True)
			abrTMP.updatePoidsRacine(serieBlocageTMP[possibilite])
		except Exception:
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

	if (profondeurVictoire>profondeur>=0 and abrTMP.getCanExpand()):

		compteurFils = 0

		for possibilite in dictionnaireTMP.keys():

			matriceTMP2 = np.copy(matriceTMP)

			if ((tour+tourTMP)%2==0):
				matriceTMP2[possibilite[0]][possibilite[1]] = -1
			else:
				matriceTMP2[possibilite[0]][possibilite[1]] = 1

			victoireTMP, seriesJoueur1TMP, seriesJoueur2TMP, serieBlocageTMP = testVictoire(matriceTMP2, False)
			poids = calculPoids(seriesJoueur1TMP, seriesJoueur2TMP, victoireTMP, tourTMP)

			if (abs(2-profondeur)<profondeurVictoire):
				canExpandTMP = False
			else:
				canExpandTMP = True

			if (victoireTMP and (tour+tourTMP)%2==0):
				if (abs(2-profondeur)<profondeurVictoire):
					profondeurVictoire = abs(2-profondeur)
					canExpandTMP = False

			abrTMP.ajoutFils(ABR({possibilite:poids},[], canExpandTMP)) #mettre directement dans la parenthèse

			IA(tourTMP+1, profondeur-1, matriceTMP2, abrTMP.getFils()[compteurFils])

			#print([fils.getRacine() for fils in abrTMP.getFils()])

	poidsPere = 0

	if ((tour+tourTMP)%2==0):
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
		poids += (10**indice)*(joueur1*seriesJoueur1TMP[indice]+joueur2*seriesJoueur2TMP[indice])

	if victoireTMP:
		if ((tour+tourTMP)%2==0):
			poids -= 10**(nbVictoire+1)
		else:
			poids += 10**(nbVictoire+1)

	return poids

def evalPossibilites(matriceCalcul):

	dictionnaireCoordPoids = {}

	for i in range(nbCase):
		for j in range(nbCase):

			coord = (i,j)

			if (estValide(coord, matriceCalcul) and matriceCalcul[i][j]==-10):
				dictionnaireCoordPoids[coord] = 0

	return dictionnaireCoordPoids

# def main():

#     global tour

#     print('\n\n')

#     if ( tour >= (2*nbVictoire-1)):
#     	victoire, serieJoueur1TMP, serieJoueur2TMP = testVictoire(matriceJeu)
#     	if ( victoire ):
#     		return

#     if (tour%2==0):
#     	print("JOUEUR 1")
#     	coordJoueur = tourJoueur()
#     	if ( not estValide(coordJoueur, matriceJeu) ):
#     		tour -= 1
#     	else:
#     		updateMatrice(coordJoueur, joueur1)
#     else:
#     	time1 = time()
#     	coordRetour = tourIA()
#     	timeDelta = int(time() - time1)
#     	if ( not estValide(coordRetour, matriceJeu) ):
#     		tour -= 1
#     	else:
#     		updateMatrice(coordRetour, joueur2)
#     	print("JOUEUR 2\n\nTemps de réflexion : "+str(timeDelta)+" secondes")

#     afficheMatrice()

#     main()

# if __name__ == '__main__':
#     initMatriceJeu()
#     main()

def start(pMatriceJeu, pTour):

	global matriceJeu, tour

	
	matriceJeu = pMatriceJeu
	tour = pTour
	
	return tourIA()

def initParam(pNbCase, pNbVictoire):
	
	global nbCase, nbVictoire

	nbCase = pNbCase
	nbVictoire = pNbVictoire