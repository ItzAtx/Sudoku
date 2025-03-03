import tkinter as tk
from tkinter import messagebox
import random
import time

def estValide(tableau, row, col, nombre):
    """Vérifie si le Sudoku est résolu"""
    #Vérifie si le nombre est valide dans la ligne
    for x in range(9):
        if tableau[row][x] == nombre:
            return False

    #Vérifie si le nombre est valide dans la colonne
    for x in range(9):
        if tableau[x][col] == nombre:
            return False

    #Vérifie si le nombre est valide dans la sous-grille 3x3
    rowDebut, colDebut = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if tableau[i + rowDebut][j + colDebut] == nombre:
                return False

    return True


def resoudreSudoku(tableau):
    """Résoud le Sudoku"""
    trouver = trouverCasesVides(tableau)
    if not trouver:
        return True
    row, col = trouver

    for nombre in range(1, 10):
        if estValide(tableau, row, col, nombre):
            tableau[row][col] = nombre

            if resoudreSudoku(tableau):
                return True

            tableau[row][col] = 0

    return False


def trouverCasesVides(tableau):
    """Trouve une case vide"""
    for i in range(9):
        for j in range(9):
            if tableau[i][j] == 0:
                return (i, j)
    return None


def genererSudoku():
    """Génère un Sudoku aléatoire"""
    while True:
        tableau = [[0 for _ in range(9)] for _ in range(9)]
        for i in range(9):
            tableau[0][i] = i + 1
        random.shuffle(tableau[0])
        resoudreSudoku(tableau)

        #Vérifie si le Sudoku a une solution unique
        if estSolutionUnique(tableau):
            break

    #Retire certaines cases pour le joueur
    for _ in range(40):
        row = random.randint(0, 8)
        col = random.randint(0, 8)
        tableau[row][col] = 0

    return tableau


def estSolutionUnique(tableau):
    """Vérifie si le Sudoku a une solution unique"""
    return resoudreSudoku([row[:] for row in tableau])


class SudokuPrincip(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sudoku")
        self.grilleSudoku = genererSudoku()
        self.solutionGrille = [row[:] for row in self.grilleSudoku]
        resoudreSudoku(self.solutionGrille)
        self.entrees = []
        self.creerWidgets()
        self.debut = time.time()  #Temps de départ du chronomètre
        self.tempsStop = False  #Indique si le chronomètre est arrêté
        self.chronometre()  #Met à jour le timer

    def creerWidgets(self):
        #Crée les champs d'entrée pour le Sudoku
        for i in range(9):
            for j in range(9):
                entree = tk.Entry(self, width=2, font=('Arial', 20, 'bold'), justify='center')
                entree.grid(row=i, column=j)
                if self.grilleSudoku[i][j] != 0:
                    #Affiche les nombres préremplis dans le Sudoku
                    entree.insert(tk.END, str(self.grilleSudoku[i][j]))
                    #Désactive les champs d'entrée pour les nombres préremplis
                    entree.config(state='disabled')
                self.entrees.append(entree)

        #Bouton pour vérifier la solution de l'utilisateur
        boutonVerifier = tk.Button(self, text="Verifier", command=self.verifierSolution)
        boutonVerifier.grid(row=9, column=0, columnspan=4, sticky='we')

        #Bouton pour afficher la solution
        boutonSolution = tk.Button(self, text="Solution", command=self.montrerSolution)
        boutonSolution.grid(row=9, column=5, columnspan=4, sticky='we')

        #Configure toutes les colonnes avec la même largeur
        for i in range(9):
            self.grid_columnconfigure(i, weight=1)
        
        #Label pour afficher le timer
        self.labelChrono = tk.Label(self, text="Temps écoulé: 00:00")
        self.labelChrono.grid(row=10, column=0, columnspan=9, sticky='we')
    
    def chronometre(self):
        """Met à jour le timer toutes les secondes"""
        if not self.tempsStop:
            tempsActuel = time.time() - self.debut
            minutes = int(tempsActuel // 60)
            secondes = int(tempsActuel % 60)
            self.labelChrono.config(text="Temps écoulé: {:02d}:{:02d}".format(minutes, secondes))
            self.after(1000, self.chronometre)  #Appel récursif pour mettre à jour le timer


    def verifierSolution(self):
        """Récupère la saisie de l'utilisateur et l'évalue"""
        grilleUtilisateur = [[int(self.entrees[i * 9 + j].get()) if self.entrees[i * 9 + j].get() else 0
                              for j in range(9)] for i in range(9)]
        if not estComplet(grilleUtilisateur):
            messagebox.showerror("SudokuErreur", "Sudoku incomplet ! Veuillez saisir toutes les valeurs !")
        elif grilleUtilisateur == self.solutionGrille:
            self.tempsStop = True  #Arrête le chronomètre
            tempsEcoule = time.time() - self.debut  #Calcul du temps écoulé
            tempsM = int(tempsEcoule // 60)
            tempsS = int(tempsEcoule % 60)
            tempsString = "{:02d}:{:02d}".format(tempsM, tempsS)
            messagebox.showinfo("SudokuErreur", f"Félicitations ! Vous avez trouvé la solution !\nTemps écoulé: {tempsString}")
            self.destroy()  #Ferme la fenêtre
        else:
            messagebox.showerror("SudokuErreur", "Dommage ! Votre solution est incorrecte !")

    def montrerSolution(self):
        """Crée la fenêtre de la solution"""
        fenetreSolution = SolutionWindow(self.solutionGrille)  #Affiche la solution dans une nouvelle fenêtre
        fenetreSolution.mainloop()


def estComplet(tableau):
    """Vérifie si le Sudoku est complet"""
    for row in tableau:
        if 0 in row:
            return False
    return True


class SolutionWindow(tk.Toplevel):
    """Crée la fenêtre pour afficher la solution du Sudoku"""
    def __init__(self, tableau):
        super().__init__()  #Appelle le constructeur de la classe parente
        self.title("Sudoku Solution")
        self.geometry("310x325")
        self.tableau = tableau
        self.creerWidgets()

    def creerWidgets(self):
        #Affiche la solution du Sudoku dans une nouvelle fenêtre
        for i in range(9):
            for j in range(9):
                entree = tk.Entry(self, width=2, font=('Arial', 20, 'bold'), justify='center')
                entree.grid(row=i, column=j)
                entree.insert(tk.END, str(self.tableau[i][j]))
                entree.config(state='disabled')  #Désactive les champs d'entrée

#Crée une fenêtre Tkinter principale
root = SudokuPrincip()
root.mainloop()  #Lance la boucle principale de l'application

