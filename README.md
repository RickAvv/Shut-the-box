# Try to Shut the box :)

This is an attempt to find the best strategy for the game [Shut the box](https://en.wikipedia.org/wiki/Shut_the_box)

There are 2 components to this project, one is a monte carlo simulation that implements a euristic-based strategy (always pick the combination with the highest number, or with the lowest number, or with the most numbers, etc..) in either a solitary or 1v1 game, the other is a series of analytical solutions to the problem of maximizing the probability of "shutting the box" (i.e., flipping down all the tiles of the board) or minimizing average score, recursively computed.

#
The solo.py script simulates n games played solo, 1v1.py simulates *n* matches of *m* games between two players.

- Implement a **strategy** that maximizes the probability of shutting the box, or minimizes the score!
- Make 2 strategies **battle each other** to see which one wins more often! 
- Change the **parameters** (score calculation, number of tiles on the board, number of games per match) and see if different variants of the game require different strategies!

#
prob_best_strategy.py calculates the maximum theoretical probability to shut the box (finding a strategy that maximises it), mean_best_strategy.py calculates the minimum average score obtainable per game (finding a strategy that minimizes the score). 

#
the interactive.py script is a tool which you can use for guided play, i.e. you input the dice results and it tells you the tiles to flip to maximize your probability to shut the box. Use it to best your opponents and astonish your friends!

&nbsp;

## Have Fun!
