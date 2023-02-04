import copy
import sys
import time

start_time = time.time()
grid = []
assigned_units = list()
flag = False
solutionGrid = []
filename = sys.argv[1]


#Reading input file and creating the initial sudoku grid
def initial_grid():
    global grid
    with open('Input_files/' + filename) as f:
        for line in f:
            line = line.strip().split(',')
            each_line = []
            for i in line:
                each_line.append(int(i))
            grid.append(each_line)


#Creating and assigning values to initial domains of each unit
def initial_domains():
    global assigned_units
    domains = {}
    for i in range(9):
        for j in range(9):
            if grid[i][j] == 0:
                domains["Unit" + str(i) + str(j)] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            elif grid[i][j] != 0:
                assigned_units.append("Unit" + str(i) + str(j))
                domains["Unit" + str(i) + str(j)] = grid[i][j]
    return domains


#Updating domains of each unit based on constraints
def updatedomain(grid, row, col, domain_dict):
    if (len(domain_dict) == 0):
        return domain_dict["Unit" + str(row) + str(col)]
    remove_list = []
    #Checking the same row for values and adding it to remove list
    for x in range(9):
        if grid[row][x] != 0:
            remove_list.append(grid[row][x])

    #Checking the same column for values and adding it to remove list
    for x in range(9):
        if grid[x][col] != 0:
            remove_list.append(grid[x][col])
    #Checking for values in 3*3 grid and adding it to remove list
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] != 0:
                remove_list.append(grid[i + startRow][j + startCol])
    #Removing all values present in remove list from the domain
    for val in remove_list:
        if val in domain_dict["Unit" + str(row) + str(col)]:
            domain_dict["Unit" + str(row) + str(col)].remove(val)
    return domain_dict["Unit" + str(row) + str(col)]


#Checking for minimum remaining value and return the unit that has least number of values in its domain
def MRV(domain_dict):
    global grid
    min_length = 100
    for i in range(9):
        for j in range(9):
            unit = "Unit" + str(i) + str(j)
            if grid[i][j] == 0:
                if len(domain_dict[unit]) < min_length:
                    min_length = len(domain_dict[unit])
                    mrv_unit = unit
    if min_length == 100:
        mrv_unit = str(0)
    return mrv_unit


#Checking if the assigned value to a unit is valid assignment and returning True or False based on it
def checkValidAssignment(row, col, d):
    for x in range(9):
        if grid[row][x] == d:
            return False
    for x in range(9):
        if grid[x][col] == d:
            return False
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] == d:
                return False

    return True


#Printing the end solution
def copyOutput():
    global grid
    global end_time
    solutionGrid = copy.deepcopy(grid)
    print("Solution")
    for i in range(9):
        print(solutionGrid[i])
    end_time = time.time()


#Checking if all units are assigned values and returning True or False based on it
def checkTerminatingCondition(grid):
    global flag
    for a in range(9):
        for b in range(9):
            if (grid[a][b] == 0):
                return False
    flag = True
    return True


#Implementation of forward checking with backtracking
def FOR_backtracking(grid, domain_dict, i, j):
    global flag
    global assigned_units
    #If termination condition is achieved then print the solution
    if (checkTerminatingCondition(grid)):
        copyOutput()
        return
    #If grid value is not 0, then it already has a value assigned to it so return
    if (grid[i][j] != 0):
        return
    else:
        unit = "Unit" + str(i) + str(j)
        #For each value in the unit's domain
        for d in domain_dict[unit]:
            if (flag == True):
                break
            #If it is a valid assignment, then assign it to the grid and do forward checking
            if (checkValidAssignment(i, j, d)):
                grid[i][j] = d
                localDomain_dict = copy.deepcopy(domain_dict)
                #Implementation for forward checking and updating domains of other units based on valid assignment of current unit's assignment
                for a in range(9):
                    for b in range(9):
                        if grid[a][b] == 0:
                            localDomain_dict["Unit" + str(a) +
                                             str(b)] = updatedomain(
                                                 grid, a, b, localDomain_dict)
                #If terminating condition is achieved, then print the solution
                if (checkTerminatingCondition(grid)):
                    copyOutput()
                    return
                #Get the next unit by calling the MRV function
                nextUnit = MRV(localDomain_dict)
                if (nextUnit == "0"):
                    return
                nextj = int(nextUnit[-1])
                nexti = int(nextUnit[-2])
                FOR_backtracking(grid, localDomain_dict, nexti, nextj)
                grid[i][j] = 0
        return


#Calling the functions
initial_grid()
domain_dict = initial_domains()
for a in range(9):
    for b in range(9):
        if grid[a][b] == 0:
            domain_dict["Unit" + str(a) + str(b)] = updatedomain(
                grid, a, b, domain_dict)
print("Initial grid")
for i in range(9):
    print(grid[i])
unit = MRV(domain_dict)
FOR_backtracking(grid, copy.deepcopy(domain_dict), int(unit[-2]),
                 int(unit[-1]))
print("Total time taken=", end_time - start_time)
