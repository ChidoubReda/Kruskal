# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 11:46:07 2024

@author: L13
"""
import networkx as nx
import matplotlib.pyplot as plt
import random
import string

def generate_random_graph(num_vertices):
    G = nx.gnp_random_graph(num_vertices, 0.5)
    
    # Générer les labels en alphabet pour les sommets
    labels = []
    alphabet = string.ascii_uppercase
    for i in range(num_vertices):
        if i < 26:
            labels.append(alphabet[i])
        else:
            labels.append(alphabet[(i // 26) - 1] + alphabet[i % 26])
    
    # Mapper les labels sur les sommets
    mapping = {i: labels[i] for i in range(num_vertices)}
    G = nx.relabel_nodes(G, mapping)
    
    # Ajouter un coût aléatoire (poids) pour chaque arête
    for (u, v) in G.edges():
        G.edges[u, v]['weight'] = random.randint(1, 9)
    
    return G

def kruskal_minimum_spanning_tree(G):
    # Initialiser l'arbre couvrant minimum
    mst = nx.Graph()
    mst.add_nodes_from(G.nodes)
    
    # Trier les arêtes par poids
    sorted_edges = sorted(G.edges(data=True), key=lambda x: x[2]['weight'])
    
    # Détection des cycles par union-find
    subsets = {node: node for node in G.nodes}
    
    def find(node):
        if subsets[node] != node:
            subsets[node] = find(subsets[node])
        return subsets[node]
    
    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)
        subsets[root1] = root2
    
    # Construire l'arbre couvrant minimum
    total_weight = 0
    for u, v, data in sorted_edges:
        if find(u) != find(v):
            mst.add_edge(u, v, weight=data['weight'])
            total_weight += data['weight']
            union(u, v)
    
    return mst, total_weight

def draw_graph_with_mst(G, mst, mst_weight):
    pos = nx.spring_layout(G)
    
    # Dessiner le graphe entier avec des arêtes en gris
    nx.draw(G, pos, with_labels=True, node_color="skyblue", font_size=10, font_weight="bold", edge_color="lightgray")
    
    # Afficher les poids des arêtes dans le graphe
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    # Dessiner l'arbre couvrant minimum avec des arêtes en rouge
    nx.draw_networkx_edges(mst, pos, edge_color="red", width=2)
    
    # Afficher la somme des coûts de l'arbre couvrant minimum
    plt.title(f"Somme des coûts de l'arbre couvrant minimum : {mst_weight}")
    plt.show()

def main():
    nodes = int(input("saisir le nombre des sommets : "))
    G = generate_random_graph(nodes)
    
    # Calculer l'arbre couvrant minimum et sa somme de coûts
    mst, mst_weight = kruskal_minimum_spanning_tree(G)
    
    print("Graphe généré avec l'arbre couvrant minimum (en rouge) :")
    draw_graph_with_mst(G, mst, mst_weight)

if __name__ == "__main__":
    main()
