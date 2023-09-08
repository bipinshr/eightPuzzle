# Name: Bipin Shrestha
# UTA ID: 1001841216
import time
import sys
import queue
from copy import deepcopy
sys.setrecursionlimit(100000000)
# ---------------------------NODE ------
class Node:
    state = None
    parent = None
    depth = 0
    cost_of_move = 0    #g(x)
    pathcost = 0 
    action = None
    h_x = 0 
    f_n = 0
    def __init__(self, state, parent, depth, cost_of_move, pathcost, action,h_x,f_n):
        self.state = state
        self.parent = parent
        self.depth = depth 
        self.cost_of_move = cost_of_move
        self.pathcost = pathcost
        self.action = action
        self.h_x = h_x
        self.f_n = f_n


    def __str__(self):
        return f'{self.state}'


def find_zero(state):
    zero = 0
    for i in range(3):
        for j in range(3):
            if state[i][j] == zero:
                return i,j

def possible_move(x,y):
    return x >= 0 and x < 3 and y >= 0 and y < 3

def Expand(node,goal_test):
    i_positionZero = 0
    j_positionZero = 0
    action = ["Up", "Right","Down","Left"]
    row = [ 1, 0, -1, 0 ]
    col = [ 0, -1, 0, 1 ]
    successor = []

    #considering all the action: Here 4 action
    for i in range(4):
        positionZero = find_zero(node.state)
        i_positionZero = positionZero[0]
        j_positionZero = positionZero[1]
        new_tile = [i_positionZero + row[i], j_positionZero + col[i]]

        if possible_move(new_tile[0],new_tile[1]):
            #copy the state to another
            temp = deepcopy(node.state)
            #find the number that need to be swap. It is also the cost of being swap
            cost_of_move = node.state[new_tile[0]][new_tile[1]]
            #swap the position of number with zero
            temp[new_tile[0]][new_tile[1]] = 0
            #swap the position of number where it is zero with the cost or the number being swap
            temp[i_positionZero][j_positionZero] = cost_of_move
            g_n = node.pathcost + cost_of_move 
            h_dist = heuristic(temp,goal_test)
            f_n = g_n + h_dist
            new_node = Node(temp,node,node.depth+1,cost_of_move,g_n,action[i],h_dist,f_n)
            successor.append(new_node)
    return successor
#------------------------------------------------------------------------------------------------
def heuristic(start,final):
    start_position = {}
    final_position = {}
    for i in range(3):
        for j in range(3):
            start_position[start[i][j]] = (i,j)
            final_position[final[i][j]] = (i,j)
    
    # print(start_position)
    # print(final_position)
    distance = 0
    for i in range(9):
        #dis = abs|x1-x2| + abs|y1-y2|
        # print(i)
        distance += (abs(start_position[i][0]-final_position[i][0]) + abs(start_position[i][1]-final_position[i][1])) * i
    return distance



def treesearch(problem,goal_test,method,filename,dumpfile):
    fringe = []
    closed = []
    Nodes_Popped= 0
    Nodes_Expanded= 0
    Nodes_Generated= 0
    Max_Fringe_Size= 0
    fringe.append(Node(problem,None,0,0,0,None,0,heuristic(problem,goal_test)))
    Nodes_Generated = 1
    # if(method == "dfs"):
    #     fr = priorityQueue()
    #     fr.push(fringe[0])
    Max_Fringe_Size = 1
    def loop(Nodes_Popped,Nodes_Expanded,Nodes_Generated,Max_Fringe_Size):
       
        '''
        if method == "bfs":
            node = fringe.pop(0)
        elif method == "ucs":
            fringe.sort(key=lambda x : x.pathcost)
            node = fringe.pop(0)
        elif method == "greedy":
            fringe.sort(key=lambda x : x.h_x)
            node = fringe.pop(0)
        elif method == "a*" or method == "A*" or method == "astar":
            fringe.sort(key=lambda x : x.f_n)
            node = fringe.pop(0)
        # elif method == "dfs":
        #     node = fr.pop()
        else:
            fringe.sort(key=lambda x : x.f_n)
            node = fringe.pop(0)
        '''
        if(len(fringe)==0):
            Nodes_Generated -=1
            print("Solution not found")
            quit()

        node = fringe.pop(0)
        Nodes_Popped  += 1
        # print(f"The next pop with the pathcost is {node.pathcost}, h(x)= {node.h_x} and f(x) = {node.pathcost + node.h_x}")
        # print(node.state)

        if(node.state == goal_test):
            print("Nodes Popped:", Nodes_Popped)
            print("Nodes Expanded:", Nodes_Expanded)
            print("Nodes Generated:", Nodes_Generated)
            print("Max Fringe Size:", Max_Fringe_Size)
            depth_found = node.depth
            total_cost = node.pathcost
            print(f"Solution found at depth {depth_found} with cost {total_cost}.")
            print("step: ")
            step_path = []
            while(node.parent != None):
                step_path.append(node)
                node = node.parent
            
            while(len(step_path)!= 0):
                temp = step_path.pop()
                print(f"       move {temp.cost_of_move} {temp.action}")

            return 
        
        if(node.state not in closed):
            Nodes_Expanded+=1
            closed.append(node.state)
            succesor_generated = Expand(node,goal_test)
            num_of_succesor_generated =  len(succesor_generated)
            Nodes_Generated += num_of_succesor_generated

            while(len(succesor_generated)!=0):
                # if method ==  "dfs":
                #     fr.push(succesor_generated.pop())
                fringe.append(succesor_generated.pop())
                

            if(len(fringe)>=Max_Fringe_Size):
                Max_Fringe_Size = len(fringe)
            
            if method == "bfs":
                #Do nothing to findge
                # node = fringe.pop(0)
                pass
            elif method == "ucs":
                fringe.sort(key=lambda x : x.pathcost)
                # node = fringe.pop(0)
            elif method == "greedy":
                fringe.sort(key=lambda x : x.h_x)
                # node = fringe.pop(0)
            elif method == "a*" or method == "A*" or method == "astar":
                fringe.sort(key=lambda x : x.f_n)
                # node = fringe.pop(0)
            # elif method == "dfs":
            #     node = fr.pop()
            else:
                fringe.sort(key=lambda x : x.f_n)
                # node = fringe.pop(0)


            #------------------------------------------------------------------------------------------------
            if dumpfile==True:
                
                output = f"Generating successor to state = {node.state}, action = {node.cost_of_move} {node.action}, g(n) = {node.pathcost}, d(n) = {node.depth},f(n) = {node.f_n}, parent = {str(node.parent)}, \n"
                
                output += f"       {num_of_succesor_generated} successors generated \n"
                output += f"Closed: {closed}\n"
                output += f'Fridge:  [\n< '
                for i in range(len(fringe)):
                    output += f"state = "
                    output += f"{fringe[i].state} action = {fringe[i].cost_of_move} {fringe[i].action}, g(n) = {fringe[i].pathcost}, d(n) = {fringe[i].depth},f(n) = {fringe[i].f_n}, parent = {str(fringe[i].parent)} \n"
                with open (filename,'a+') as txt:
                    txt.write(output)
                    txt.close()

            loop(Nodes_Popped,Nodes_Expanded,Nodes_Generated,Max_Fringe_Size)
        else:
            if dumpfile == True:
                output = f"\n[[[ state = {node.state} action ={node.cost_of_move} {node.action}, g(n) = {node.pathcost}, d(n) = {node.depth},f(n) = {node.f_n}, parent = {str(node.parent)} NOTHING to add to Fridge\n"
                with open (filename,'a+') as txt:
                        txt.write(output)
                        txt.close()
            loop(Nodes_Popped,Nodes_Expanded,Nodes_Generated,Max_Fringe_Size)
    loop(Nodes_Popped,Nodes_Expanded,Nodes_Generated,Max_Fringe_Size)  





def search_dfs(problem,goal_test,method,filename,dumpfile):
    fringe = queue.LifoQueue()
    closed = []
    Nodes_Popped= 0
    Nodes_Expanded= 0
    Nodes_Generated= 0
    Max_Fringe_Size= 0
    fringe.put(Node(problem,None,0,0,0,None,0,heuristic(problem,goal_test)))
    Nodes_Generated = 1
    # if(method == "dfs"):
    #     fr = priorityQueue()
    #     fr.push(fringe[0])
    Max_Fringe_Size = 1
    def loop(Nodes_Popped,Nodes_Expanded,Nodes_Generated,Max_Fringe_Size):
        

        
        # print(f"The next pop with the pathcost is {node.pathcost}, h(x)= {node.h_x} and f(x) = {node.pathcost + node.h_x}")
        # print(node.state)
        if(fringe.qsize()==0):
            Nodes_Generated -=1
            print("Solution not found")
            quit()
        
        node = fringe.get()
        Nodes_Popped  += 1

        if(node.state == goal_test):
            print("Nodes Popped:", Nodes_Popped)
            print("Nodes Expanded:", Nodes_Expanded)
            print("Nodes Generated:", Nodes_Generated)
            print("Max Fringe Size:", Max_Fringe_Size)
            depth_found = node.depth
            total_cost = node.pathcost
            print(f"Solution found at depth {depth_found} with cost {total_cost}.")
            print("step: ")
            step_path = []
            while(node.parent != None):
                step_path.append(node)
                node = node.parent
            
            while(len(step_path)!= 0):
                temp = step_path.pop()
                print(f"       move {temp.cost_of_move} {temp.action}")

            return 
        
        if(node.state not in closed):
            Nodes_Expanded+=1
            closed.append(node.state)
            succesor_generated = Expand(node,goal_test)
            num_of_succesor_generated =  len(succesor_generated)
            Nodes_Generated += num_of_succesor_generated

            while(len(succesor_generated)!=0):
                # if method ==  "dfs":
                #     fr.push(succesor_generated.pop())
                fringe.put(succesor_generated.pop())
                

            if(fringe.qsize()>=Max_Fringe_Size):
                Max_Fringe_Size = fringe.qsize()
            
            '''
            if method == "bfs":
                #Do nothing to findge
                # node = fringe.pop(0)
                pass
            elif method == "ucs":
                fringe.sort(key=lambda x : x.pathcost)
                # node = fringe.pop(0)
            elif method == "greedy":
                fringe.sort(key=lambda x : x.h_x)
                # node = fringe.pop(0)
            elif method == "a*" or method == "A*" or method == "astar":
                fringe.sort(key=lambda x : x.f_n)
                # node = fringe.pop(0)
            # elif method == "dfs":
            #     node = fr.pop()
            else:
                fringe.sort(key=lambda x : x.f_n)
                # node = fringe.pop(0)
            '''

            #------------------------------------------------------------------------------------------------
            if dumpfile==True:
                
                output = f"Generating successor to state = {node.state}, action = {node.cost_of_move} {node.action}, g(n) = {node.pathcost}, d(n) = {node.depth},f(n) = {node.f_n}, parent = {str(node.parent)}, \n"
                
                output += f"       {num_of_succesor_generated} successors generated \n"
                output += f"Closed: {closed}\n"
                output += f'Fridge:  [\n< '
                # for i in range(fringe.qsize()):
                #     output += f"state = "
                #     output += f"{fringe[i].state} action = {fringe[i].cost_of_move} {fringe[i].action}, g(n) = {fringe[i].pathcost}, d(n) = {fringe[i].depth},f(n) = {fringe[i].f_n}, parent = {str(fringe.peek.parent)} \n"
                for item in list(fringe.queue):
                    output += f"state = "
                    output += f"{item.state} action = {item.cost_of_move} {item.action}, g(n) = {item.pathcost}, d(n) = {item.depth},f(n) = {item.f_n}, parent = {str(item.parent)} \n"

                with open (filename,'a+') as txt:
                    txt.write(output)
                    txt.close()

            loop(Nodes_Popped,Nodes_Expanded,Nodes_Generated,Max_Fringe_Size)
        else:
            if dumpfile==True:
                output = f"\n[[[ state = {node.state} action ={node.cost_of_move} {node.action}, g(n) = {node.pathcost}, d(n) = {node.depth},f(n) = {node.f_n}, parent = {str(node.parent)} NOTHING to add to Fridge\n"
                with open (filename,'a+') as txt:
                        txt.write(output)
                        txt.close()
            loop(Nodes_Popped,Nodes_Expanded,Nodes_Generated,Max_Fringe_Size)
    loop(Nodes_Popped,Nodes_Expanded,Nodes_Generated,Max_Fringe_Size) 

def depth_limited_search(problem,goal_test,method,filename,dumpfile,depth_limit):
    fringe = queue.LifoQueue()
    closed = []
    Nodes_Popped= 0
    Nodes_Expanded= 0
    Nodes_Generated= 0
    Max_Fringe_Size= 0
    fringe.put(Node(problem,None,0,0,0,None,0,heuristic(problem,goal_test)))
    Nodes_Generated = 1
    # if(method == "dfs"):
    #     fr = priorityQueue()
    #     fr.push(fringe[0])
    Max_Fringe_Size = 1


    while not fringe.empty():
        node = fringe.get()
        Nodes_Popped  += 1
        if(node.state == goal_test):
            print("Nodes Popped:", Nodes_Popped)
            print("Nodes Expanded:", Nodes_Expanded)
            print("Nodes Generated:", Nodes_Generated)
            print("Max Fringe Size:", Max_Fringe_Size)
            depth_found = node.depth
            total_cost = node.pathcost
            print(f"Solution found at depth {depth_found} with cost {total_cost}.")
            print("step: ")
            step_path = []
            while(node.parent != None):
                step_path.append(node)
                node = node.parent
            
            while(len(step_path)!= 0):
                temp = step_path.pop()
                print(f"       move {temp.cost_of_move} {temp.action}")

            return 
        elif(node.depth == depth_limit):
            while(node.depth != depth_limit):
                node = node.get()
        elif(node.state not in closed):
            if node.depth < depth_limit:
                Nodes_Expanded+=1
                closed.append(node.state)
                succesor_generated = Expand(node,goal_test)
                num_of_succesor_generated =  len(succesor_generated)
                Nodes_Generated += num_of_succesor_generated

                while(len(succesor_generated)!=0):
                    check = succesor_generated.pop()
                    if(check.state not in closed):
                        fringe.put(check)
                    

                if(fringe.qsize()>=Max_Fringe_Size):
                    Max_Fringe_Size = fringe.qsize()

                #------------------------------------------------------------------------------------------------
                if dumpfile==True:
                    
                    output = f"Generating successor to state = {node.state}, action = {node.cost_of_move} {node.action}, g(n) = {node.pathcost}, d(n) = {node.depth},f(n) = {node.f_n}, parent = {str(node.parent)}, \n"
                    
                    output += f"       {num_of_succesor_generated} successors generated \n"
                    output += f"Closed: {closed}\n"
                    output += f'Fridge:  [\n< '
                    # for i in range(fringe.qsize()):
                    #     output += f"state = "
                    #     output += f"{fringe[i].state} action = {fringe[i].cost_of_move} {fringe[i].action}, g(n) = {fringe[i].pathcost}, d(n) = {fringe[i].depth},f(n) = {fringe[i].f_n}, parent = {str(fringe.peek.parent)} \n"
                    for item in list(fringe.queue):
                        output += f"state = "
                        output += f"{item.state} action = {item.cost_of_move} {item.action}, g(n) = {item.pathcost}, d(n) = {item.depth},f(n) = {item.f_n}, parent = {str(item.parent)} \n"

                    with open (filename,'a+') as txt:
                        txt.write(output)
                        txt.close()
        else:
            if node.depth < depth_limit:
                if dumpfile==True:
                    output = f"\n[[[ state = {node.state} action ={node.cost_of_move} {node.action}, g(n) = {node.pathcost}, d(n) = {node.depth},f(n) = {node.f_n}, parent = {str(node.parent)} NOTHING to add to Fridge\n"
                    with open (filename,'a+') as txt:
                            txt.write(output)
                            txt.close()

    print("Solution not found")
    with open (filename,'a+') as txt:
        txt.write("Solution not found")
        txt.close()
    return 

if __name__ == "__main__":
    now = time.strftime("%Y%m%d-%H%M%S")
    startfile = sys.argv[1]
    goalfile = sys.argv[2]
    dumpfile = False
    if(len(sys.argv)==5):
        method_selected = sys.argv[3]
        dumpfile = sys.argv[4]
    elif(len(sys.argv)==4):
        method_selected = sys.argv[3]
        dumpfile = False
    else:
        method_selected = "a*"
        dumpfile = False

    if dumpfile == "true" or dumpfile == "TRUE" or dumpfile == "True":
        dumpfile = True
    if dumpfile == "false" or dumpfile == "FALSE" or dumpfile == "FALSE":
        dumpfile = False


    # print(startfile)
    # print("goal",goalfile)
    # print("method",method_selected)


    # -----------------------------INITIAL STATE---------------------------
    inital_state = []
    with open(startfile,'r') as f:
        for line in f.readlines():
            if line == "END OF FILE": break
            inital_state.append([int(l) for l in line.rstrip().split()])
    # print(inital_state)

    # -----------------------------GOAL STATE---------------------------
    goal_test = []
    with open(goalfile,'r') as f:
        for line in f.readlines():
            if line == "END OF FILE": break
            goal_test.append([int(l) for l in line.rstrip().split()])

    # print(goal_test)
    filename = ""

    # print("----------------------------")
    if dumpfile == True:
        opeingstatement = f"Command-line Argument: {sys.argv[1:]}\nMethod Selected: {method_selected} \n Running: {method_selected}"
        filename = f"trace-{now}.txt"
        with open (filename,'w') as txt:
                txt.write(opeingstatement)
                txt.close()
   
    
    if method_selected == "dfs":
        search_dfs(inital_state,goal_test,method_selected,filename,dumpfile)
    elif method_selected == "dls":
        depth_limit = input("\n Enter the depth limit l: ")
        depth_limit = int(depth_limit)
        depth_limited_search(inital_state,goal_test,method_selected,filename,dumpfile,depth_limit)
    else:
        treesearch(inital_state,goal_test,method_selected,filename,dumpfile)



 







