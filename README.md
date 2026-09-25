# Astar-algorithm
The Astar algorithm is a type of pathfinding algorithm that searches for the target using a 'sense of direction' _(h-cost)_ in addition to a movement cost between nodes _(g-cost)_. In other words, this algorithm is designed for weighted graphs where the algorithm carefully selects each node on the graph with the lowest weight. This results in one of the fastest search algorithms because it does not waste time searching for nodes that are irrelevant.

## implementation
I created this algorithm based on my understanding from youtube videos and countless months of research using A.I and websites.

-**Version 1:** relies on pygame.Rect objects and their positions which adds a slight overhead due to its collision mechanic for detecting neighbors on the map.

-**Version 2:** I implemented a grid system array of the map where the algorithm navigates by indexing specific locations on the map which is constant time lookup O(1).
 
## performance
After many optimizations, the latest version performs on average 5-7ms faster than my old version.

## how to use

firstly, to see how my algorithm searches for paths, ensure that you are running Astar-DEMO.py in order to see the visualization of the algorithm. The other file (Astar.py) does not have that feature as it will show instead how fast the algorithm has performed. 

Please note that can you change the maps. Here are the lists of maps corresponding to each number: 



While the program is running, simply press the number corresponding to you map choice and press SPACE on your keyboard to watch the algorithm pathfind to its target.

Please note that can you change the maps. Here are the lists of maps corresponding

Feel free to check out my code and let me know your thoughts. 




