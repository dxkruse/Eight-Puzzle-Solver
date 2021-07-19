Dietrich Kruse
Intro to Artificial Intelligence
Program 1 - A* Eight Puzzle

My inversion counter seems to be off, but I was unable to figure out what was causing it. I was able to run some with brute force, but set the max iterations to 50,000.

-First cell initializes everything.
-Second cell uses inversion counter and solves what it calculates to be solvable.
-Third cell can be run instead of second cell to brute force specific puzzle if desired.

When I wrote A* last semester for my Robotics/Unmanned Systems class, I set up a parent index for each "node" and my initial state had a parent index of -1.
This allowed me to loop backwards through nodes from goal to initial to retrieve the optimal path. I attempted the same thing this time, but was not able to make it work
in time. 