# Astar-algorithm
The Astar algorithm is a type of pathfinding algorithm that searches for a target using a 'sense of direction' _(h-cost)_ in addition to a movement cost between nodes _(g-cost)_. In other words, this algorithm is designed for weighted graphs where the algorithm carefully selects each node on the graph with the lowest weight. This results in one of the fastest search algorithms because it does not waste time searching for nodes that are irrelevant.

## implementation
I created this algorithm based on my understanding from youtube videos and countless months of research using A.I and websites.

-**Version 1:** relies on pygame.Rect objects and their positions which adds a slight overhead due to its collision mechanic for detecting neighbors on the map.

-**Version 2:** I implemented a grid system array of the map where the algorithm navigates by indexing specific locations on the map which is constant time lookup O(1).
 
## performance
After many optimizations, the latest version performs on average 5-7ms faster than my old version.

## setup

- Install Python from [python.org](https://www.python.org/downloads/) _(pip is included with Python 3.4+)_
- Clone or download this repository
- Install dependencies:
```
pip install -r requirements.txt
```
- Run the visualizer:
```
python Astar-DEMO.py
```
- Or run the performance version:
```
python Astar.py
```

## how to use

firstly, in order to see how my algorithm searches for paths, ensure that you are running Astar-DEMO.py in order to see the visualization of the algorithm. The other file (Astar.py) does not have that feature as it will show instead how fast the algorithm has performed. 

Please note that can you change the maps. Here are the lists of maps corresponding to each number: 

1.
<img width="800" height="500" alt="Image" src="https://github.com/user-attachments/assets/242247c0-6f00-443a-b4a2-9ac0a83a2d31" />

2.
<img width="450" height="300" alt="Image" src="https://github.com/user-attachments/assets/c1254a43-b52b-4a74-bbcd-150bc3de16a1" />

3.
<img width="800" height="500" alt="Image" src="https://github.com/user-attachments/assets/4da70ddb-ee53-44d5-9dce-5d29cf44a62b" />

4. 
<img width="450" height="300" alt="Image" src="https://github.com/user-attachments/assets/7ca8c349-e055-433b-9b47-91e13aab86a4" />

5. 
<img width="800" height="500" alt="Image" src="https://github.com/user-attachments/assets/e861657a-2bdf-4388-a497-2a9e93bd7c80" />

6. 
<img width="800" height="500" alt="Image" src="https://github.com/user-attachments/assets/9f7e298e-fe9e-4b03-a4bf-a5267143f85b" />

7. 
<img width="800" height="500" alt="Image" src="https://github.com/user-attachments/assets/33112cc2-0d6e-44e8-b14f-49ad6b5da3ac" />

While the program is running, simply press the number corresponding to your map choice and press SPACE on your keyboard to watch the algorithm pathfind to its target.

Feel free to check out my code and let me know your thoughts.
