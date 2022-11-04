from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from decimal import Decimal
from tasks.models import Collection , bound , inf
import requests
import urllib.request
import time
import json
from operator import itemgetter
from bs4 import BeautifulSoup
import numpy as np
import math

# Variables
collection=Collection.objects.all()
type_routage=""
maxsize = float('inf')
nbre_dest=0
N=nbre_dest+1
adj=np.ones((N,N))
final_res=maxsize
final_path = [None] * (N + 1)
visited = [False] * N
list=[]
prdt=[]
longit_1=0
longit_2=0
latit_1=0
latit_2=0

#produit cartesien des noms des entrees 
def produit(*args, repeat=1): 
    iterables = args*repeat 
    result=[()]
  
    for it in iterables: 
        result = produit_cartesien(result,it)  
  
    return result  
  
def produit_cartesien(iterable1,iterable2): 
    for e1 in iterable1:  
        for e2 in iterable2: 
            yield (e1 + (e2,)) 

#web scraping
def scraping(long_1,long_2,lat_1,lat_2):
    url='https://api.distancematrix.ai/maps/api/distancematrix/json?origins='+lat_1+','+long_1+'&destinations='+lat_2+','+long_2+'&key=Ap0Ts3LRNONbJPduwTQCTkKIGBhnC'
    response=requests.get(url)
    #la reponse obtenue par le scraping
    rsp=response.content
    soup=BeautifulSoup(response.text,"html.parser")
    #on parcourtla reponse pour trouver la distance et extraire cette donnee 
    for e in soup : 
        e=e.text 
        index = e.find("distance")
        res=e[index+19:].split()[0]
    return(res)  

#matrice de distance
def matrice_distance(dim,liste):
    A = np.zeros([dim,dim])
    for i in range (len(liste)):
        place_1=liste[i][0]
        place_2=liste[i][1]
        if(int(place_1)!=int(place_2)):
            for j in collection:
                if(place_1==j.lieu):
                    longit_1=j.longitude
                    latit_1=j.latitude
                if(place_2==j.lieu):
                    longit_2=j.longitude
                    latit_2=j.latitude
            dist=scraping(str(longit_1),str(longit_2),str(latit_1),str(latit_2))
            A[int(place_1) , int(place_2)]=dist
            A[int(place_2) , int(place_1)]=dist
    return A



#Affichage de la page index.html
def index(request):
    return render(request,"index.html",context={})

#Recuperer les données de connexion et se diriger vers la page choix.html en cas de validation d'identification
def connection(request):
    c=request.POST.get("user")
    d=request.POST.get("pwd")
    if c=='Martin' and d=='Admin':
          return render(request,"choix.html",context={})
    else:
        return index(request)

#Affichage de la page form pour remplir les infos concernant le routage 
def form(request):
        return render(request,"form.html",context={})
#Recupération des donnees du form 
def resp(request):
    type_routage=request.POST.get("type")
    longitude_depot=Decimal(request.POST.get("longitude"))
    latitude_depot=Decimal(request.POST.get("latitude"))
    nbre_dest=int(request.POST.get("nbre"))
    N=nbre_dest+1
    #creation d'un object dans le modéle collection **objet depot ou bien début du trajet
    Collection.objects.create(lieu="0",longitude=longitude_depot,latitude=latitude_depot)

    #creation des objets dans le modele collection **objets pour destinations
    for i in range(nbre_dest):
        long=Decimal(request.POST.get("longitude"+str(i)))
        lat=Decimal(request.POST.get("latitude"+str(i)))
        Collection.objects.create(lieu=str(i+1),longitude=long,latitude=lat)

    #Ajout des lieux a une liste
    for i in collection:
         list.append(i.lieu)

    #Appliquer le produit cartesien sur la liste créee pour voir tous les trajets possibles
    iterateur = produit(list,repeat=2)
    for e in iterateur: 
         prdt.append(e)

    #Eliminer les éléments répetés
    for j in range (len(prdt)):
        for i in range(j+1,len(prdt)-1):
            if prdt[j][0]==prdt[i][1] and prdt[j][1]==prdt[i][0] :
                prdt.remove(prdt[i])

    #création de la matrice de distance
    B=matrice_distance(N,prdt)
    print(B)
    if type_routage=="exacte":
        TSP(B , N)
        return render(request,"branch.html",{'B':'Exact Method' ,'A':final_res,'N':final_path})
    if type_routage=="quick":
        #Clarck & wright
        distance_matrix=B
        list_i_j_saving=[]
        i=1
        while i<len(distance_matrix)-1:
            j=i+1
            while j<len(distance_matrix):
                saving=distance_matrix[0][i]+distance_matrix[0][j]-distance_matrix[i][j]
                list_i_j_saving.append([i+1,j+1,saving])
                j+=1
            i+=1   
        list_i_j_saving=sorted(list_i_j_saving, key=itemgetter(2), reverse=True)
        print(list_i_j_saving)

        routing=[1,list_i_j_saving[0][0],list_i_j_saving[0][1],1]
        print(routing)
        index=1
        while True:
            if len(routing)==len(distance_matrix)+1:
                break
            if index==len(list_i_j_saving):
                break
            if list_i_j_saving[index][0]==routing[1] and (list_i_j_saving[index][1] not in routing):
                routing.insert(1,list_i_j_saving[index][1])
                index +=1
                print(f'here 1 {index}')
                continue
            if list_i_j_saving[index][0]==routing[-2] and (list_i_j_saving[index][1] not in routing):
                routing.insert(-1,list_i_j_saving[index][1])
                index +=1
                print(f'here 2 {index}')
                continue
            if list_i_j_saving[index][1]==routing[1] and (list_i_j_saving[index][0] not in routing):
                routing.insert(1,list_i_j_saving[index][0])
                index +=1
                print(f'here 3 {index}')
                continue
            if list_i_j_saving[index][1]==routing[-2] and (list_i_j_saving[index][0] not in routing):
                routing.insert(-1,list_i_j_saving[index][0])
                index +=1
                print(f'here 4 {index}')
                continue
            index+=1
        print(routing)
        return render(request,"branch.html",{'B':'Quick Method','A':'----' ,'N':routing})
Collection.objects.all().delete()
bound.objects.all().delete()
inf.objects.all().delete()

#Branch & Bound
def copyToFinal(curr_path ,N):
	final_path[:N + 1] = curr_path[:]
	final_path[N] = curr_path[0]
#
def firstMin(adj, i ,N):
	min = maxsize
	for k in range(N):
		if adj[i][k] < min and i != k:
			min = adj[i][k]

	return min
#
def secondMin(adj, i , N):
	first, second = maxsize, maxsize
	for j in range(N):
		if i == j:
			continue
		if adj[i][j] <= first:
			second = first
			first = adj[i][j]

		elif(adj[i][j] <= second and
			adj[i][j] != first):
			second = adj[i][j]

	return second
#
def TSPRec(adj, curr_bound, curr_weight,level, curr_path, visited , N):
	global final_res
	if level == N:
		if adj[curr_path[level - 1]][curr_path[0]] != 0:
			curr_res = curr_weight + adj[curr_path[level - 1]]\
										[curr_path[0]]
			if curr_res < final_res:
				copyToFinal(curr_path , N)
				final_res = curr_res
		return

	for i in range(N):
		if (adj[curr_path[level-1]][i] != 0 and
							visited[i] == False):
			temp = curr_bound
			curr_weight += adj[curr_path[level - 1]][i]
			if level == 1:
				curr_bound -= ((firstMin(adj, curr_path[level - 1] , N) +
								firstMin(adj, i , N)) / 2)
			else:
				curr_bound -= ((secondMin(adj, curr_path[level - 1] , N) +
								firstMin(adj, i , N)) / 2)
			if curr_bound + curr_weight < final_res:
				curr_path[level] = i
				visited[i] = True
				TSPRec(adj, curr_bound, curr_weight,
					level + 1, curr_path, visited , N)
			curr_weight -= adj[curr_path[level - 1]][i]
			curr_bound = temp
			visited = [False] * len(visited)
			for j in range(level):
				if curr_path[j] != -1:
					visited[curr_path[j]] = True
#
def TSP(adj , N):
	curr_bound = 0
	curr_path = [-1] * (N + 1)
	visited = [False] * N
	for i in range(N):
		curr_bound += (firstMin(adj, i , N) +
					secondMin(adj, i , N))
	curr_bound = math.ceil(curr_bound / 2)
	visited[0] = True
	curr_path[0] = 0
	TSPRec(adj, curr_bound, 0, 1, curr_path, visited , N)

