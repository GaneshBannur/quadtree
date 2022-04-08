#program to demonstrate the quadtree and its methods
from quadtree import node
import random
import sys
import time
import matplotlib.pyplot

def display(points):
    x_coordinates=[]
    y_coordinates=[]
    for point in points:
        x_coordinates.append(point[0])
        y_coordinates.append(point[1])
    matplotlib.pyplot.scatter(x_coordinates, y_coordinates)

full_range = [(-1000, 1000), (-1000, 1000)]
root = node()
root.node_range = full_range
while True:
    print("Enter 1 to insert, 2 to delete, 3 to query a range, 4 for approximate n nearest, 5 for n nearest, 6 for random fill n points, 7 to display all nodes, 8 to exit")
    choice = int(input())
    if choice==1:
        print("Enter point as x y")
        x, y = input().split()
        x = int(x)
        y = int(y)
        root.insert(point=(x, y))
    elif choice==2:
        print("Enter point as x y")
        x, y = input().split()
        x = int(x)
        y = int(y)
        root.delete(point=(x, y))
    elif choice==3:
        print("Enter x range as x_min x_max")
        x1, x2 = input().split()
        x1 = int(x1)
        x2 = int(x2)
        print("Enter y range as y_min y_max")
        y1, y2 = input().split()
        y1 = int(y1)
        y2 = int(y2)
        start_time = time.time()
        result = root.get_points_in_range([(x1, x2), (y1, y2)])
        end_time = time.time()
        print("Running time", end_time-start_time)
        print("Number of points found in query range are", len(result))
        print("Query Result", result)
        display(points=root.get_points_in_range(query_range=full_range))
        display(points=result)
        matplotlib.pyplot.show()
    elif choice==4:
        print("Enter point as x y")
        x, y = input().split()
        x = int(x)
        y = int(y)
        print("Enter number of neighbours to be found")
        n = int(input())
        start_time = time.time()
        result = root.n_nearest_approx(point=(x, y), n=n)
        end_time = time.time()
        print("Running time", end_time-start_time)
        print("Number of approximate nearest points", len(result))
        print("Approximate nearest points", result)
        display(points=root.get_points_in_range(query_range=full_range))
        display(points=result)
        matplotlib.pyplot.show()
    elif choice==5:
        print("Enter point as x y")
        x, y = input().split()
        x = int(x)
        y = int(y)
        print("Enter number of neighbours to be found")
        n = int(input())
        start_time = time.time()
        result = root.n_nearest(point=(x, y), n=n)
        end_time = time.time()
        print("Running time", end_time-start_time)
        print("Number of nearest points", len(result))
        print("Nearest points", result)
        display(points=root.get_points_in_range(query_range=full_range))
        display(points=result)
        matplotlib.pyplot.show()
    elif choice==6:
        print("Enter number of points to be inserted")
        n = int(input())
        for i in range(n):
            root.insert(point=(random.randint(full_range[0][0], full_range[0][1]), random.randint(full_range[1][0], full_range[1][1])))
    elif choice==7:
        display(points=root.get_points_in_range(query_range=full_range))
        matplotlib.pyplot.show()
    elif choice==8:
        sys.exit()