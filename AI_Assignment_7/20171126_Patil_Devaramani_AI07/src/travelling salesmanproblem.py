#the code was written with help from psychicorigami.com and ericphanson.com
from math import sqrt
from random import shuffle
import time
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint

class City(object):

    def __init__(self, dist_matrix, tour):
        self.tour = tour
        self.total = tour_length(dist_matrix, tour)

    def __str__(self):
        return str(self.tour)

# def swapped_cities(tour):                                                             #doesn't return a very desired output
#     '''generator to create all possible variations
#       where two cities have been swapped'''
#     for i,j in all_pairs(len(tour)):
#         if i < j:
#             copy=tour[:]
#             copy[i],copy[j]=tour[j],tour[i]
#             pprint (tour)
#             yield copy
#
# def init_random_tour(tour):
#     for i in range(5):
#         tour = shuffle(tour)
#         yield tour

def steep_ascend_hillclimb(current_city, dist_matrix, run_time):
    start_time = time.time()
    counter = 0
    best_city = None
    least_cost = float('inf')
    while True:
        counter+=1
        for new_city in reversed_sections(current_city.tour):
            if time.time() - start_time >= run_time:
                return best_city, counter
            new_city = City(dist_matrix, new_city)
            if new_city.total < least_cost:
                #print new_city
                least_cost = new_city.total
                best_city = new_city
        current_city = best_city

def basic_hillclimb(current_city, dist_matrix, run_time):
    start_time = time.time()
    counter = 0
    best_city = None
    least_cost = float('inf')
    while True:
        counter+=1
        for new_city in reversed_sections(current_city.tour):
            if time.time() - start_time >= run_time:
                return best_city, counter
            new_city = City(dist_matrix, new_city)
            if new_city.total < least_cost:
                #print new_city
                least_cost = new_city.total
                best_city = new_city
                current_city = best_city
                break

def reversed_sections(tour):                                  #returns all possible variations where the section between two cities are swapped
    for i,j in all_pairs(len(tour)):
        if i != j:
            copy=tour[:]
            if i < j:
                copy[i:j+1]=reversed(tour[i:j+1])
            else:
                copy[i+1:]=reversed(tour[:j])
                copy[:j]=reversed(tour[i+1:])
            if copy != tour:
                yield copy

def all_pairs(size,shuffle=shuffle):                         #forms a pair of cities
    r1=range(size)
    r2=range(size)
    if shuffle:
        shuffle(r1)
        shuffle(r2)
    for i in r1:
        for j in r2:
            yield (i,j)

def tour_length(matrix,tour):                               #returns total length of a given path
    total=0
    num_cities=len(tour)
    for i in range(num_cities):
        j=(i+1)%num_cities
        city_i=tour[i]
        city_j=tour[j]
        total+=matrix[city_i,city_j]
    #print total
    return total

def cartesian_matrix(coords):                               # create a distance matrix for the city coords using euclidian distance
    dist_matrix={}
    for i,(x1,y1) in enumerate(coords):
        for j,(x2,y2) in enumerate(coords):
            dx,dy=x1-x2,y1-y2
            dist=sqrt(dx*dx + dy*dy)
            dist_matrix[i,j]=dist
    #print dist_matrix
    return dist_matrix

def read_coords(coord_file):                                #reads the co-ordinates of cities in a given text file
    coords=[]
    city_num =[]
    #coords = {}
    for line in coord_file:
        name,x,y=line.strip().split(',')
        coords.append((float(x),float(y)))
    #     name,x,y=line.strip().split(',')
    #     coords.update({str(name):(float(x),float(y))})
    for i in range(len(coords)):
        city_num.append(i)
    return coords,city_num

if __name__ == '__main__':
    print "executing"
    coord_file =  open("/home/mihir/Downloads/test/cities_full.txt",'r')
    coord_list,tour = read_coords(coord_file)
    #print tour
    dist_matrix = cartesian_matrix(coord_list)
    #route = tour_length(dist,tour)
    route = tour_length(cartesian_matrix(coord_list),tour)
    #rs = reversed_sections(tour)
    #init_function=lambda: init_random_tour(len(coords))
    #print init_function
    #objective_function=lambda tour: -tour_length(matrix,tour)
    #print objective_function
    run_time = 12                                                               #run_time = 12 for 1 min, 60 for 5 min, 240 for 20 min
    evaluated_cost = []
    for i in range(5):
        shuffle(tour)
        order = City(dist_matrix, tour)
        final_city, total_cycles = steep_ascend_hillclimb(order,
                                                          dist_matrix,
                                                          run_time)
        evaluated_cost.append(final_city.total)    #
    min_cost = min(evaluated_cost)
    #print total_cycles
    print "Least cost: ", min_cost
    plt.plot(zip(*[coord_list[final_city.tour[i % len(final_city.tour)]] \
    for i in range(len(final_city.tour)) ])[0], zip(*[coord_list[final_city.tour \
    [i % len(final_city.tour)]]for i in range(len(final_city.tour)) ])[1], 'xb-', );
    plt.show()

#for basic hill climbing
    raw_input("press any button to run basic hill climbing")
    evaluated_cost = []
    for i in range(5):
        shuffle(tour)
        order = City(dist_matrix, tour)
        final_city, total_cycles = basic_hillclimb(order,
                                                   dist_matrix,
                                                   run_time)
        evaluated_cost.append(final_city.total)
    min_cost = min(evaluated_cost)
    #print total_cycles
    print "Least cost: ", min_cost
    plt.plot(zip(*[coord_list[final_city.tour[i % len(final_city.tour)]]\
    for i in range(len(final_city.tour)) ])[0], zip(*[coord_list[final_city.tour\
    [i % len(final_city.tour)]] for i in range(len(final_city.tour)) ])[1], 'xb-', );
    plt.show()
