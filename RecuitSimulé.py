import time
import matplotlib.pyplot as plt
import random
import math

class Ville:
    def __init__(self, x, y, demande):
        self.x = x
        self.y = y
        self.demande = demande
        
temperature_initiale = 100
taux_refroidissement = 0.95
iterations = 5
def distance(ville1, ville2):
    return math.sqrt((ville1.x - ville2.x)**2 + (ville1.y - ville2.y)**2)

def cout_solution(solution):
    cout = 0
    for i in range(len(solution) - 1):
        cout += distance(solution[i], solution[i + 1])
    return cout
def read_data_from_file(filename):
    villes = []
    with open(filename, 'r') as file:
        for line in file:
            b,  x, y,z, demande = map(int, line.split())
            villes.append(Ville(x, y, demande))
    return villes

temperatures_iteration = []

def recuit_simule(villes, temperature_initiale, taux_refroidissement, iterations):
    solution_actuelle = villes[:]
    meilleure_solution = solution_actuelle[:]
    temperature = temperature_initiale

    couts_iteration = []
  
    for iteration in range(iterations):
        
        ville1, ville2 = random.sample(range(len(villes)), 2)
        nouvelle_solution = solution_actuelle[:]
        nouvelle_solution[ville1], nouvelle_solution[ville2] = nouvelle_solution[ville2], nouvelle_solution[ville1]
        cout_actuel = cout_solution(solution_actuelle)
        cout_nouveau = cout_solution(nouvelle_solution)
        if cout_nouveau < cout_actuel or random.uniform(0, 1) < math.exp((cout_actuel - cout_nouveau) / temperature):
            solution_actuelle = nouvelle_solution[:]
            temperature =  temperature * taux_refroidissement
            temperatures_iteration.append(temperature)
            
        if cout_solution(solution_actuelle) < cout_solution(meilleure_solution):
            meilleure_solution = solution_actuelle[:]
        couts_iteration.append(cout_solution(meilleure_solution))
    return meilleure_solution, couts_iteration


filename = 'C:/Users/hayth/OneDrive/Bureau/softcoputingprojet/file.txt'
villes = read_data_from_file(filename)

start_time = time.time()
meilleure_solution, couts_iteration = recuit_simule(villes, temperature_initiale, taux_refroidissement, iterations)

print("Meilleure solution:", meilleure_solution)
print("Coût de la meilleure solution:", cout_solution(meilleure_solution))
end_time = time.time()


execution_time = end_time - start_time
print("Temps d'exécution : {execution_time} secondes")

plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.plot(couts_iteration)
plt.xlabel('Iteration')
plt.ylabel('Cost ')
plt.title(' Cost variation with Simulated Annealing')

plt.subplot(1, 2, 2)
plt.plot(temperatures_iteration, color='orange')
plt.xlabel('Iteration')
plt.ylabel('Temperature')
plt.title('Temperature variation with Simulated Annealing')

plt.tight_layout()
plt.show()