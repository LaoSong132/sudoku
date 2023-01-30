# This repository includes activities for 520 project

## Index
* [Group members](#Group-members)
* [Project Description](#Project-Description)
* [Sudoku as Constraint Satisfaction Problem](#Sudoku-as-Constraint-Satisfaction-Problem)
* [Sudoku as the Exact Cover problem](#Sudoku-as-the-Exact-Cover-problem)

## Group members
    Yugalee Vijay Patil
    Yuanming Song

## Project Description:
### Sudoku is a popular number game that involves filling up 9x9 square grid with numbers ranging from 1 to 9. The 9x9 square grid is further divided into nine 3x3 square grids and each such grid should contain values from 1 to 9, and additionally, each column and row should also contain numbers ranging from 1 to 9. The initial state is a partially filled grid and based on the constraints and logic, the final completely filled state is achieved.
### In our project, we have implemented a sudoku solver as a constraint satisfaction problem (CSP) and also as an exact cover problem. In implementing both approaches, we compared the result based on the time taken to solve each level of difficulty of the sudoku problem. There are three levels of difficulty that we tested- easy, intermediate, and difficult.

## Sudoku as Constraint Satisfaction Problem (CSP) - SudokuSolver_CSP.py
### We implemented this problem in Python using the concept of forward checking, backtracking, and minimum remaining value. The initial_grid() function reads the input file and the initial_domains() assigns values to the domain of each unit of the grid. The MRV() function is called to choose a unit having the least number of values in its domain and assign that value to the grid if it is a valid assignment. Then we perform the forward checking algorithm in which after assigning a value to the grid, the domains of each unit of the grid are updated i.e all constraints are checked and values that do not satisfy those constraints are removed from the domain. The program outputs the total time taken in seconds but for comparison we changed the time unit to milliseconds

Usage:
To run the code, type the command python SudokuSolver_CSP.py <input_type> on cmd where <input_type> is the input filename.
`python SudokuSolver_CSP.py sudoku1.txt`

Input: Data is read from Input_Files/ folder
Output: Program outputs the initial sudoku, solved (resulting) sudoku and total time taken on cmd.

File Structure:
SudokuSolver_CSP.py - The runable code i.e. actual execution of the algorithm to solve sudoku as constraint satisfaction problem.

## Sudoku as the Exact Cover problem
### We implemented this problem in Python using the concept of exact cover problem, algorithm X, and dancing links. Since the sudoku puzzle needs to ensure only one number per cell and prohibits placing the number in any other cell sharing the same column, row, or box, it is an exact cover problem. The dancing links consider the exact cover problem as a matrix of 1’s and 0’s. It will find a set or more rows in which precisely one 1 will appear for each column. It takes advantage of doubly-linked lists. The dancing links take the exact cover matrix into a toroidal doubly linked list. A solution is found when all the columns have been removed from the matrix.
### To run the code, type the command python DL_ALGX_sudoku.py <input_type> on cmd where <input_type> is the input filename.
`python DL_ALGX_sudoku.py sudoku1.txt`
