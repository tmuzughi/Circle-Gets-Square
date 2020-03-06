# author: Tarik Muzughi
# date: 9/2/2019
# class: 4500 Introduction to Software Profession
# description: Program simulates a game in which "player" traverses a digraph until all nodes have been traveled
#  to at least once. Circles represent vertices of the digraph and arrows represent edges. All circles must
#  have at least one in arrow and at least one out arrow. The digraph must be strongly connected. The central
#  data structure used in the program is a two dimensional list called matrix. Matrix is used as the available
#  path layout for the "player" as the digraph is traversed.

import random

#######################################
# open the infile and the outfile
fInput = open("HW1infile.txt", "r")
fOutput = open("HW2muzughiOutfile.txt", "w")
i = 0
#######################################
# system for checking for strong connection
# this system found on https://www.geeksforgeeks.org/connectivity-in-a-directed-graph/
# and integrated into our program
from collections import defaultdict


# This class represents a directed graph using adjacency list representation
class Graph:

    def __init__(self, vertices):
        self.V = vertices  # No. of vertices
        self.graph = defaultdict(list)  # default dictionary to store graph

    # function to add an edge to graph
    def addEdge(self, u, v):
        self.graph[u].append(v)

        # A function used by isSC() to perform DFS

    def DFSUtil(self, v, visited):

        # Mark the current node as visited
        visited[v] = True

        # Recur for all the vertices adjacent to this vertex
        for i in self.graph[v]:
            if visited[i] == False:
                self.DFSUtil(i, visited)

                # Function that returns reverse (or transpose) of this graph

    def getTranspose(self):

        g = Graph(self.V)

        # Recur for all the vertices adjacent to this vertex
        for i in self.graph:
            for j in self.graph[i]:
                g.addEdge(j, i)

        return g

        # The main function that returns true if graph is strongly connected

    def isSC(self):

        # Step 1: Mark all the vertices as not visited (For first DFS)
        visited = [False] * (self.V)

        # Step 2: Do DFS traversal starting from first vertex.
        self.DFSUtil(0, visited)

        # If DFS traversal doesnt visit all vertices, then return false
        if any(i == False for i in visited):
            return False

        # Step 3: Create a reversed graph
        gr = self.getTranspose()

        # Step 4: Mark all the vertices as not visited (For second DFS)
        visited = [False] * (self.V)

        # Step 5: Do DFS for reversed graph starting from first vertex.
        # Staring Vertex must be same starting point of first DFS
        gr.DFSUtil(0, visited)

        # If all vertices are not visited in second DFS, then
        # return false
        if any(i == False for i in visited):
            return False

        return True
#######################################
# fill the matrix with directional values from our infile
# and validate input file
for line in fInput:
    j = i + 1
    if i == 0:
        if line[0].isspace():
            print("Error: First line of input is invalid, space detected")
            fOutput.write("Error: First line of input is invalid, space detected")
            exit()
        try:
            N = int(line)  # N holds number of circles
        except ValueError:
            print("Error: First line of input is invalid, non-integer detected")
            fOutput.write("Error: First line of input is invalid, non-integer detected")
            exit()
        if N > 20 or N < 2:  # if first line is not in range
            print("Error: First line of input is not in range 2-20")
            exit()
        matrix = [[0 for x in range(N)] for y in range(N)]
        g1 = Graph(N)
    elif i == 1:
        if line[0].isspace():
            print("Error: Second line of input is invalid, space detected")
            fOutput.write("Error: Second line of input is invalid, space detected")
            exit()
        try:
            K = int(line)  # K holds number of arrows

        except ValueError:
            print("Error: Second line of input is invalid, non-integer detected")
            fOutput.write("Error: Second line of input is invalid, non-integer detected")
            exit()

    else:
        if line[0].isspace():
            print("Error: Line", i + 1, ",improper space detected")
            fOutput.write("Error: Line %d, improper space detected" % j)
            exit()
        #  if not line[1].isspace():
        #    print("Error: Line", i + 1, ",space between integers not detected")
        #    fOutput.write("Error: Line %d,space between integers detected" % j)
        #    exit()
        T = line.split()  # T temporarily holds the arrow direction values used to fill matrix
        try:
            var1 = int(T[0])
            var2 = int(T[1])

        except ValueError:
            print("Error: Line", i + 1, ", non-integer detected")
            fOutput.write("Error: Line %d, non-integer detected" % j)
            exit()
        # if not T[3] == "\n":
         #   print("Error: Invalid value on line", i + 1, "following second number")
         #   fOutput.write("Error: Invalid value on line %d following second number" % j)
          #  exit()

        if int(T[0]) < 1 or int(T[0]) > N:
            print("Error: Invalid input at line", i + 1, ",first number is not in range")
            fOutput.write("Error: Invalid input at line %d,first number is not in range" % j)
            exit()
        if int(T[1]) < 1 or int(T[1]) > N:
            print("Error: Invalid input at line", i + 1, ",second number is not in range")
            fOutput.write("Error: Invalid input at line %d,second number is not in range" % j)
            exit()
        g1.addEdge(var1 - 1, var2 - 1)
        matrix[var1-1][var2-1] = var2
    i = i + 1
if not i == K + 2:
    print("Error: Number of lines in file does not match integer at second line")
    fOutput.write("Error: Number of lines in file does not match integer at second line")
    exit()
#######################################
# lets check for in and out arrows
strongList = [[0 for x in range(2)] for y in range(N)]
a = 0
rows = 0
columns = 0
while a < N:
    for x in range(N):
        if matrix[a][x] > 0:  # if true once then circle a has an out arrow
            strongList[a][1] = 1
        if matrix[x][a] > 0:  # if true once then circle a has an in arrow
            strongList[a][0] = 1
    a = a + 1
# prin  t(strongList)  ###testing
count = 0
for x in range(N):
    for y in range(2):
        if strongList[x][y] == 1:
            count += 1
if count == N * 2:
    oneInOneOut = 1
else:
    print("Error: All circles do not have both an in and an out arrow")
    fOutput.write("Error: All circles do not have both an in and an out arrow")
    exit()
#######################################
# actual check for strong connection
if not g1.isSC():
    print("Digraph is not strongly connected")
    fOutput.write("Digraph is not strongly connected")
    exit()
#######################################
# ok lets start the game

# declare arrays to hold values of each game
checksTotal = [0] * 10  # store the number of checks for each game
array2D = [[0 for x in range(N)] for y in range(10)]


mate = 1
while(mate < 11):
    currentCircle = 1  # player starts in circle 1
    checkList = [0] * N  # our checklist for which circles have been traveled to at least once
    checkList[0] = 0  # circle one starts with a check since the game begins there
    # print(checkList)  ###testing
    checkMarkTotal = 0  # total number of check marks (including revisited circles)
    checkMarkTally = [0] * N  # how many times each circle has been visited
    total = 0  # accumulator to test if each circle has been visited at least once
    checkMarkTally[0] = 1  # circle 1 starts off with one tally
    check = 1  # true is the default state for the following while loop
    iterations = 0
    while(check):

        roll = random.randint(1, N)  # randomly select next circle from entire pool

        if matrix[currentCircle-1][roll-1]:  # if selected circle is available from current circle
            # print("Player goes from circle", currentCircle, "to circle", roll) ###testing
            currentCircle = roll  # set new current circle
            checkMarkTotal += 1  # increase overall checks
            array2D[mate - 1][currentCircle - 1] += 1
            checkMarkTally[currentCircle-1] += 1  # increase check tally for current circle
            checkList[currentCircle - 1] = 1  # set true for checkList with index currentCircle
            # print("New current circle is ", currentCircle)  ###testing
        else:
            arbitrary = 1  # do nothing/roll again
            # print("Player cannot travel from circle", currentCircle, "to circle", roll) ###testing
        for x in range(N):
            if checkList[x] == 1:
                total += 1
            else:
                total = 0
            if total == N:  # if each circle has been visited once
                # print("Game Over, man.")  ###testing
                # print(checkList)  ###testing
                check = 0  # set while loop condition to false
        iterations += 1
        if iterations > 1000000:
            print("Error: Number of checks for game", mate, "exceeded 1,000,000")
            fOutput.write("Error: Number of checks for game %d exceeded 1,000,000" % mate)
            exit()
    checksTotal[mate - 1] = checkMarkTotal
    ############################
    # output results of game to console

    print("The total number of circles in the game is", N)
    print("The total number of arrows in the game is", K)
    print("The total number of checks on all circles combined is", checkMarkTotal)
    average = 0
    for x in range(N):
        average += checkMarkTally[x]
    print("The average number of checks is ", average / N)
    maxi = 0
    for x in range(N):
        if checkMarkTally[x] > maxi:
            maxi = checkMarkTally[x]
    print("The maximum number of checks in any one circle is", maxi)
    print("")
    # output results of game to file

    avg = average / N
    fOutput.write("The total number of circles in the game is %d\n" % N)
    fOutput.write("The total number of arrows in the game is %d\n" % K)
    fOutput.write("The total number of checks on all circles combined is %d\n" % checkMarkTotal)
    fOutput.write("The average number of checks is %f\n" % avg)
    fOutput.write("The maximum number of checks in any one circle is %d\n" % maxi)
    fOutput.write("\n")
    mate += 1
    sum = 0
    maxi = 0
    min = checksTotal[0]
    ###############################
    for i in checksTotal:
        sum += i
        if i > maxi:
            maxi = i
        if i < min:
            min = i
    avg = sum / 10
print("The average number of total checks per game is", avg)
fOutput.write("The average number of total checks per game is %d\n" % avg)
print("The maximum number of total checks in a single game is", maxi)
fOutput.write("The maximum number of total checks in a single game is %d\n" % maxi)
print("The minimum number of total checks in a single game is", min)
fOutput.write("The minimum number of total checks in a single game is %d\n" % min)
print("")
fOutput.write("\n")
avgCircles = [0] * N
i = 0
while i < 10:
    j = 0
    while j < N:
        avgCircles[j] += array2D[i][j]
        j += 1
    i += 1
maxCircles = [0] * N
minCircles = [1000000] * N
i = 0
while i < 10:
    j = 0
    while j < N:
        if maxCircles[j] < array2D[i][j]:
            maxCircles[j] = array2D[i][j]
        if minCircles[j] > array2D[i][j]:
            minCircles[j] = array2D[i][j]
        j += 1
    i += 1
i = 0
j = 0
while i < N:
    j = i + 1
    ac = avgCircles[i]/10
    print("The average number of checks on circle", i + 1, "over all games is", avgCircles[i] / 10)
    fOutput.write("The average number of checks on circle %d" % j)
    fOutput.write(" over all games is %d\n" % ac)
    print("The maximum number of checks on circle", i + 1, "over all games is", maxCircles[i])
    fOutput.write("The maximum number of checks on circle %d" % j)
    fOutput.write(" over all games is %d\n" % maxCircles[i])
    print("The minimum number of checks on circle", i + 1, "over all games is", minCircles[i])
    fOutput.write("The minimum number of checks on circle %d" % j)
    fOutput.write(" over all games is %d\n\n" % minCircles[i])
    print("")
    fOutput.write("")
    i += 1
fInput.close()
fOutput.close()
