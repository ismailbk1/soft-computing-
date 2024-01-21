# Lecture d'une instance :
def lire_instance(chemin_fichier):
    with open(chemin_fichier, 'r') as fichier:
        lignes = fichier.readlines()

    nombre_clients = int(lignes[0].strip())
    coordonnees_demandes_clients = [list(map(int, ligne.split()[1:])) for ligne in lignes[1:nombre_clients + 1]]
    depot = list(map(int, lignes[nombre_clients + 1].split()[1:]))
    capacite_vehicules = int(lignes[nombre_clients + 2].strip())
    nombre_vehicules = int(lignes[nombre_clients + 3].strip())

    return nombre_clients, coordonnees_demandes_clients, depot, capacite_vehicules, nombre_vehicules

#2. Calcul du coût d'une solution :
def calculer_cout_solution(solution, distances):
    cout_total = 0

    for itineraire in solution:
        cout_itineraire = 0
        for i in range(len(itineraire) - 1):
            noeud_depart, noeud_arrivee = itineraire[i], itineraire[i + 1]
            cout_itineraire += distances[noeud_depart][noeud_arrivee]

        cout_total += cout_itineraire

    return cout_total

# Vérification de l'admissibilité d'une solution :

def verifier_admissibilite(solution, capacite_vehicules):
    for itineraire in solution:
        demande_itineraire = sum(demande_client[itineraire[i]] for i in range(1, len(itineraire) - 1))
        if demande_itineraire > capacite_vehicules:
            return False
    return True

