import pygame
from pygame import Vector2 as vec
import heapq
from itertools import count
from math import sqrt
import numpy as np
from time import sleep,perf_counter
pygame.init()

HEIGHT = 830
WIDTH = 1400

screen = pygame.display.set_mode((WIDTH,HEIGHT))


class move_rect:
    def __init__(self,rect):
        self.rect = rect  
        self.reset() #initialises the variables
    def int_vec(self,vec):
        return pygame.Vector2(round(vec.x),round(vec.y))   #rounds pos/arguement to the nearest whole num 
    def move_rect(self,pos_x,pos_y,speed):
        self.end = (pos_x,pos_y)
        self.end_vec = pygame.math.Vector2(self.end) 
        self.rect.x,self.rect.y = self.pos.x,self.pos.y #updates the self.pos varible linked to the rect
        if self.move:
            self.delta = self.end_vec - self.start_vec #difference between start and end
            if self.delta.length_squared() != 0: #avoids an error for when the rect gets to the end
                self.direction = self.delta.normalize() #creates a unit vector 
                self.pos += (self.direction * speed) 
            if self.int_vec(self.pos) == self.int_vec(self.end_vec): #if the rect reaches the end
                self.move = False
        else: #pos reaches the end
            self.pos = self.end_vec #snaps the rect into end position when it's near
            # revert start variables
            self.start_vec = self.end_vec
            self.start = self.end 
            self.reset()
            return True #signals that the rect has completed its movement
    def reset(self):
        self.start = (self.rect.x,self.rect.y)
        self.start_vec = pygame.math.Vector2(self.start)
        self.pos = self.start_vec.copy()
        self.move = True
        
class Astar():
    class path_node():
        def __init__(self,pos,direction,target_rect,curr_g,x,y):
            self.rect = pygame.Rect(x,y,50,50)
            self.pos = pos # location on the tilemap
            self.direction = vec(direction) 
            self.parent = self.neg_tuple(direction)
            self.gcost = curr_g + 50 # ground cost from moving to each node
            self.hcost = sqrt((target_rect.x - x)**2 + (target_rect.y - y)**2) # calculates the heuristic (distance between two points)
            self.fcost = self.gcost + self.hcost # sums them together

        def neg_tuple(self,tpl):
            return tuple(-x for x in tpl)
        
        def Render(self,color): #this method is used for debugging
            self.text = font.render(str(self.parent),True,color)
            screen.blit(self.text,(self.rect.x,self.rect.y))
        def __repr__(self):
            return str(self.parent)
    
    def __init__(self,tilemap,pos:tuple,rect):
        self.rect = rect
        self.tilemap = tilemap
        self.pos = pos #stores (row,col) of the chaser
        self.loop = False       
        self.set_time = True
        self.directions = {(0,-1), #UP
                          (0,1), #DOWN
                          (1,0), #RIGHT
                          (-1,0)} #LEFT
        
        # keys represent vector directions 
        # I store them as tuples because vectors are unhashable 
        
   
    def add_tuples(self,a, b):
        return tuple(int(x + y) for x, y in zip(a, b))
    
   
    def pathfind(self,target:tuple,target_rect): #recursion boolean allows the method to repeat itself within itself
        if self.loop == False:
            if self.set_time == True:
                self.start_time = perf_counter()
                self.set_time = False
            self.curr_g = 0
            self.open = [] #these will store tuples (row,col) where the algorithm considers the next path to take
            self.closed = set() 
            self.sol = []
            self.count = count() # this acts as a tie break for the heapq so that if two nodes have the same fcost then it will choose the one that was added first
            self.start = self.pos
 
            while not self.pos == target: 
                self.found = False
                self.neighbors = []
                
                
                #calculates each path around the chaser 
                for direction in self.directions: 
                    self.is_barrier = self.add_tuples(self.pos,direction[::-1]) 
                    # since direction represent vector directions which will be stored in self.sol
                    # it must be reversed so that when i add it to self.pos it works according to the tilemap
                    
                    if self.tilemap[self.is_barrier[0],self.is_barrier[1]] !=  1 and not self.is_barrier in self.closed:
                        offset = (self.rect.x + direction[0]*60,self.rect.y + direction[1]*60)
                        self.neighbors.append(self.path_node(self.is_barrier,direction, target_rect, self.curr_g,offset[0],offset[1]))

                       
                                
                for neighbor in self.neighbors:                    
                    self.found = False
                    for element in self.open:
                        if neighbor.pos == element[-1].pos: #there is a neighbor in the open list
                            self.found = True
                            if element[-1].gcost > neighbor.gcost:  #compares gcost and if there is a better path then updates it           
                                element[-1].fcost = neighbor.gcost + element[-1].hcost
                                element[-1].parent = neighbor.direction    
                    if self.found == False:  #neighbor was not in the open list   
                        
                        heapq.heappush(self.open, (neighbor.fcost,next(self.count), neighbor))


                             
                self.lowest = heapq.heappop(self.open) #returns the tuple with the lowest fcost and removes it from the heapq

                
                self.curr_g = self.lowest[2].gcost #obtains the object gcost from the tuple in the heapq
                self.sol.append(self.lowest[2]) #adds the object to the solution list
                self.closed.add(self.pos)
                self.pos = self.lowest[2].pos # moves pos to the node with the lowest heuristic

                self.rect = self.lowest[2].rect.copy()
                
                               
                
            self.loop = True
            self.set_time = True
            return self.recontruct_path(self.sol[:]) #passes in a shallow copy of self.sol as an argument
        else:
            return self.sol
            
    def recontruct_path(self,sol):
        self.sol = [sol[-1].direction] #adds the last object.direction
        self.pos = self.add_tuples(self.pos,sol[-1].parent[::-1]) 

        while not self.pos == self.start:
            self.index = next((obj for obj in sol if obj.pos == self.pos), None)# gives object in sol where it intersects with self.pos
            if self.index == None:
                break
            self.sol.insert(0,self.index.direction)
            self.pos = self.add_tuples(self.pos,self.index.parent[::-1])
            self.time_taken = (perf_counter()-self.start_time)*1000
            self.render_time = font_50.render(f"Time taken to pathfind: {self.time_taken:.2f}ms",True,(255,255,255))
                    
            
        return self.sol


def convert_array(map_design):
    arr = []
    rects = []
    x,y = 50,50
    for row in map_design:
        Row = []
        for col in row:
            if col == '#':
                Row.append(1)
                rects.append(pygame.Rect(x,y,50,50))
            elif col == 'T':
                target_rect = pygame.Rect(x,y,50,50)

                Row.append(3)
            elif col == 'x':
                bot_x,bot_y = x,y
                Row.append(2)           
            
            else:
                Row.append(0)
                
            x += 60
        arr.append(Row)
        
        x = 50
        y += 60
        
    return np.array(arr),rects,bot_x,bot_y,target_rect


       
                

    

class chaser():
    def __init__(self,x,y,h,w,tilemap,pos):
        self.rect = pygame.Rect(x,y,h,w)
        self.pos = vec(x,y)
        self.Move = move_rect(self.rect)
        self.moving = False
        self.shadow = Astar(tilemap,pos,self.rect.copy()) #in order to pathfind again i must redefine this
        self.count = 0
        self.time_taken = 0
        self.speed = 5
       
    def move(self,target,target_rect):
        self.sol = self.shadow.pathfind(target,target_rect) #gives a list containing vectors that pathfind to the target
        
        if self.moving == False: #prevents accidental incrementation during movement
            self.pos += self.sol[self.count] *60
        if self.Move.move_rect(self.pos.x,self.pos.y,self.speed) == True:
            #movement is complete
            
            self.count += 1
            self.moving = False
        else:
            self.moving = True
        
        if self.count >= len(self.sol): 
            self.render_time = self.shadow.render_time           
            return True
        else:
            return False

    def draw(self,surface):
        pygame.draw.rect(surface,((0,0,255)),self.rect)




model1 = ['####################',
'#.....#..x..#......#',
'###.#.#.###.#.######',
'#...#.#...#.#......#',
'#.###.###.#.######.#',
'#.#.....#.#.#....#.#',
'#.#.###.#.#.#.##.#.#',
'#.#.#...#.....#..#.#',
'#...#.#######.#.##.#',
'###.#.........#....#',
'#...###########.####',
'#.###............T##',
'####################',]
model2 = ['#####################',
'#x....#T........#...#',
'#.#######.#####.#.###',
'#.......#.....#.#...#',
'#####.#.#####.#.###.#',
'#.....#.......#.....#',
'#.#########.#.#######',
'#...........#......-#',
'#####################']
model3 = ['#####################',
'#x....#.............#',
'#.##.#.###########.##',
'#.#..#.#.........#..#',
'#.#.##.#.#######.##.#',
'#.#....#.#.....#....#',
'#.######.#.###T######',
'#........#..........#',
'#..########.#.#######',
'#...........#.......#',
'#####################']
model4 = ['#####################',
'#x........#........T#',
'#.........#.........#',
'#....######.........#',
'#.........######....#',
'#.........#.........#',
'#....######.........#',
'#...................#',
'#...................#',
'#####################']
model5 = [
'############',
'#x.....#...#',
'#......#...#',
'#......#...#',  
'#------#---#',
'#......#...#',
'#..#####.-.#',
'#----------#',
'#.........T#',
'############']
model6 = [
'##################',
"#-----#----------#",
"#-----#------#---#",
"#-----#T---#####-#",
"#-----######---#-#",
"#----------#---#-#",
"#----------#---#-#",
"#----------#---#-#",
"#----------------#",
"#-x--------------#",
'##################'

]
model7 = ['##########',
          '#--------#',
          '#--#T----#',
          '#--#####-#',
          '#--------#',
          '#------x-#',
          '##########']


selection = {pygame.K_1:model1,
             pygame.K_2:model2,
             pygame.K_3:model3,
             pygame.K_4:model4,
             pygame.K_5:model5,
             pygame.K_6:model6,
             pygame.K_7:model7,
                }

font_50 = pygame.font.Font(None,50)


cooldown = False
select_map = True
greeting = font_50.render('Press a number on your keyboard to select a map',True,(255,255,255))
run = True
font = pygame.font.Font(None,15)
clock = pygame.time.Clock()
start = False
pause = False
show_text = True



while run == True:
    while select_map == True:
        screen.fill((0,0,0))
        screen.blit(greeting,(0,0))
        
        key = pygame.key.get_pressed()
        
        pygame.display.flip()
        for i,k in enumerate(selection,start = 0):
            if key[k] == True:
                design = selection[k]
                txt = font_50.render(f'You have chosen map no. {i+1}',True,(255,255,255))
                txt2 = font_50.render("press the SPACE BAR to start",True,(255,255,255))
                screen.fill((0,0,0))
                screen.blit(txt,(WIDTH//2 - 300,HEIGHT//2))
                
                pygame.display.flip()
                
                tilemap_array,tilemap_rects,bot_x,bot_y,target_rect = convert_array(design)
                # gets coords on tilemap for bot
                x,y = np.where(tilemap_array == 2)
                pos = (x[0],y[0])

                bot = chaser(bot_x,bot_y,50,50,tilemap_array,pos)

                # gets coords on tilemap for target
                x,y = np.where(tilemap_array == 3)
                target_pos = (x[0],y[0])
                sleep(1)
                select_map = False
        # if exit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                select_map = False
    if run == False:
        pygame.quit()
    else:

        # algorithm begins
        clock.tick(144)
        
        if cooldown == False:
            if key[pygame.K_SPACE] == True: 
                start = True
                
                show_text = False
        
        if start == True:
            txt2.fill((0,0,0))
            screen.blit(txt2,(WIDTH//2 - 300,0))
            if bot.move(target_pos,target_rect) == True:               
                pause = True
                
                # map has been solved
                # choose another map
                select_map = True
                start = False
                cooldown = False
                show_text = True
                
            else:
                cooldown = True
       
        
        screen.fill((0,0,0))
       
        
        screen.blit(txt2,(WIDTH//2 - 300,0))
            
        key = pygame.key.get_pressed()
        
        pygame.draw.rect(screen,((0,255,0)),target_rect)
        
        for rect in tilemap_rects:
            pygame.draw.rect(screen,(255,0,0),rect)

        bot.draw(screen)
        if pause == True:
            screen.blit(bot.render_time,((WIDTH//2 - 300,0)))
                        
        pygame.display.flip()
        
        if pause == True:
            sleep(2)
            pause = False

        
         # if exit during the algorithm
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        

pygame.quit()

