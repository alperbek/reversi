# Reversi - an automated player

## How to run 

```shell
cd reversi\python
python reversi.py
```

Just follow the command menu which will ask you to choose a player type for black and white.  

```sell
Choose a black player type
[1] Random Player
[2] MiniMax (Naive) Player
[3] MiniMax (Alpha Beta Pruning) Player
[4] Manual (Human) Player
Enter [1-4]: 
```

The following sections will explain available player types.

## Random Player

This player randomly chooses a move from the legal moves.

- not very strong
- occasionally hits a very nice move
- very quick to decide the next move
- does not learn from experience

## Manual (aka Human) Player

You can play by entering your move.

```shell
[21:59:56] Turn: 6 (ManualPlayer)
 | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 
----------------------------------
0|   |   |   |   |   |   |   |   | 
----------------------------------
1|   |   |   |   |   |   |   |   | 
----------------------------------
2|   |   |   |   |   | @ |   | @ | 
----------------------------------
3|   |   |   | O | O | O | @ |   | 
----------------------------------
4|   |   |   | @ | @ | @ |   |   | 
----------------------------------
5|   |   |   |   |   |   |   |   | 
----------------------------------
6|   |   |   |   |   |   |   |   | 
----------------------------------
7|   |   |   |   |   |   |   |   | 
----------------------------------
Black: 6 White: 3
Enter a move row, col: 5,2   <= enter your move!
```

- weak or strong (depends on the mood)
- can be thinking very long but won't forgive the opponent for taking time 
- could/would/should learn from experience

## Minimax Player (aka Naive Minimax)

This player uses the [minimax](https://en.wikipedia.org/wiki/Minimax) decision rule. 

- requires a max_depth parameter (how deep it should think ahead)
  + max_depth = 3 => it's quick but not very strong
  + max_depth = 5 => it's slow and stronger than RandomPlayer

A big max_depth (>5) means you need to wait much longer as it will drill down 
into all the possible moves up to the max depth.

If you are human, you'll need to be doing something else while waiting.  

The below image shows when I was playing while reading an article on wikipedia.

<img src="images/reversi_play.png" width="30%"/>

## Minimax with Alpha Beta Pruning

This player uses [an improved minimax](https://en.wikipedia.org/wiki/Alpha–beta_pruning) logic.

- skips unnecessary tree search (faster than the naive minimax logic)

It is faster than the naive Minimax player.  You can try with max_depth = 7 which
is pretty strong.  

It takes a few minutes per turn which you may still feel quite slow.
It is still going through many possible plies recursively.

Also, you it plays the same opening moves every time as there is no randomness involved.
I could introduce some randomness when there are multiple best moves available but
let's not spend too much effort and move on to the next player type which naturally
makes use of randomness.

## Monte Carlo Tree Search

This player uses [random (monte carlo) simulation of tree search](https://en.wikipedia.org/wiki/Monte_Carlo_tree_search) to find out 
which move will most likely make the player win.

It does not check all the possible game turns (plies) recursively.  
It randomly chose a path till the end to find out the ultimate outcome (win/lose).
This process is repeated within a time frame give (say 5 seconds).
Then, it decides which move is most likely to make the player a winner.

## Deep-Q Network

TODO implementing...

This player uses [Q-learning](https://en.wikipedia.org/wiki/Q-learning) (from Reinforcement Learning) with Neural Network as the value function.

## References
- https://andysalerno.com/2016/03/Monte-Carlo-Reversi
- https://jeffbradberry.com/posts/2015/09/intro-to-monte-carlo-tree-search/
- http://aima.cs.berkeley.edu/python/games.html

