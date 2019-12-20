from collections import defaultdict
import numpy as np

# This class shows a directed graph using adjacency matrix representation


class Graph:

    def __init__(selfdirect, graph):
        selfdirect.graph = graph  # This gives residual graph
        selfdirect.ROW = len(graph)

    '''Returns true if there is a path from source 's' to sink 't' in 
    residual graph. Also fills path_parent[] to store the path '''

    def BreadthFirstSearch(selfdirect, s, t, path_parent):

        # specify all the nodes as not visited
        visited = [False] * (selfdirect.ROW)

        # Create a queue for BreadthFirstSearch
        queue = []

        # specify the source node as visited and enqueue it
        queue.append(s)
        visited[s] = True

        # Standard BreadthFirstSearch Loop
        while queue:

            # Dequeue a vertex from queue and print the output
            u = queue.pop(0)

            # Get all adjacent vertices of the dequeued vertex u
            # If a adjacent has not been visited, then specify it
            # visited and enqueue it
            for ind, val in enumerate(selfdirect.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    path_parent[ind] = u

                    # If we reach sink in BreadthFirstSearch starting from source, then return
        # true, else false
        return True if visited[t] else False

    # Returns tne maximum flow from s to t in the given graph
    def FordFulkerson(selfdirect, source, sink):

        # This array is filled by BreadthFirstSearch and to store path
        path_parent = [-1] * (selfdirect.ROW)

        max_flow = 0  # There is no flow initially

        # Keep augmenting the flow while there is path from source to sink
        while selfdirect.BreadthFirstSearch(source, sink, path_parent):

            # Find the least residual capacity of the edges along the
            # path filled by BreadthFirstSearch. Or we can say find the maximum flow
            # through the path found.
            path_flow = float("Inf")
            s = sink
            while (s != source):
                path_flow = min(path_flow, selfdirect.graph[path_parent[s]][s])
                s = path_parent[s]

                # Add path flow to overall flow
            max_flow += path_flow

            # update residual capacities of the edges and reverse edges
            # along the path
            v = sink
            while (v != source):
                u = path_parent[v]
                selfdirect.graph[u][v] -= path_flow
                selfdirect.graph[v][u] += path_flow
                v = path_parent[v]

        return max_flow
def change_time_to_LAX(airport_code,time_of_depart_or_arrival): #All the other airports are coverted to the time zone of Los Angeles
    time_hrs = time_of_depart_or_arrival
    if (airport_code == "PHX") or (airport_code == "DEN"):
        if (int(time_hrs) - 1) >= 0:
            time_hrs = str(int(time_hrs) - 1)
        else:
            time_hrs = str(24 + int(time_hrs) - 1)
    elif (airport_code == "ATL") or (airport_code == "IAD") or (airport_code == "BOS") :
        if (int(time_hrs) - 3) >= 0:
            time_hrs= str(int(time_hrs) - 3)
        else:
            time_hrs = str(24 + int(time_hrs) - 3)
    elif airport_code =="ORD":
        if (int(time_hrs) - 2) >= 0:
            time_hrs = str(int(time_hrs) - 2)
        else:
            time_hrs = str(24 + int(time_hrs) - 2)
    else:
        time_hrs = time_of_depart_or_arrival
    return time_hrs

def main(input_text_file_path,temp_file_path):  # specify the airports and the respective flight capacities and compute the max flow per hour
    airports = {'LAX': '0', 'SFO': '1', 'PHX': '2', 'SEA': '3', 'DEN': '4', 'ATL': '5', 'ORD': '6', 'BOS': '7', 'IAD': '8',
                'JFK': '9'}
    aircraft_capacities = {'A220': '105', 'A319': '128', 'A320': '150', 'A321': '185', 'A321neo': '196', 'A330-200': '230',
                           'A330-300': '290', 'A330-900neo': '280', 'A350-900': '300', '717-200': '110', '737-700': '126',
                           '737-800': '165', '737-900': '180', '737-900ER': '180', '737-Max9': '180', '757-200': '180',
                           '757-300': '230', '767-300': '200', '767-300ER': '225', '767-400ER': '240', '777-200': '270',
                           '777-200ER': '270', '777-200LR': '280', '777-300': '300', '787-8': '235', '787-9': '280',
                           'Embraer170': '72', 'Embraer175(E75)': '78', 'Embraer190': '100',
                           'McDonnellDouglasMD-88': '150', 'McDonnellDouglasMD-90-30': '150', 'CRJ700': '75',
                           'CRJ900': '75'}

    input_text_file_obj = open(input_text_file_path,'r')

    temp_text_file_obj = open(temp_file_path,'w')

    input_text_data = input_text_file_obj.readlines()
    for line in input_text_data:
        splitting_line = line.split(';')
        #print(splitting_line)
        dep = splitting_line[2].split(':')
        arr = splitting_line[3].split(':')
        dep[0] = change_time_to_LAX(splitting_line[0], dep[0])
        arr[0] = change_time_to_LAX(splitting_line[1], arr[0])
        #print('before:'+str(dep))
        if int(dep[1]) > 30:
            if(int(dep[0])+1 == 24):
                dep[0] = '00'
            else:
                    dep[0] = str(int(dep[0]) + 1)
        dep[1] = '00'
        #print('after:'+str(dep))

        if int(arr[1]) > 30:
            if(int(arr[0])+1 == 24):
                arr[0] = '00'
            else:
                arr[0] = str(int(arr[0]) + 1)
        arr[1] = '00'
        newline = splitting_line[0] + ";" + splitting_line[1] + ";" + dep[0]+":"+dep[1] + ";" + arr[0]+":"+arr[1] + ";" + splitting_line[4];
        temp_text_file_obj.write(newline)
        #print(arr)
    temp_text_file_obj.close()
    input_text_file_obj.close()

    maxflow_hr = []
    temp_text_file_obj = open(temp_file_path,'r')
    temp_file_data = temp_text_file_obj.readlines()
    #print(temp_file_data)

    for i in range(0,24):
        graph = np.zeros([10, 10], dtype=int)
        for line in temp_file_data:
            splitted_line = line.split(';')
            dep_airport = splitted_line[0]
            arr_airport = splitted_line[1]
            dep_time = splitted_line[2]
            dep_time = dep_time.split(":")
            arr = splitted_line[3]
            aircraft_type = splitted_line[4]
            #print(dep_time.split(""))
            if( int(dep_time[0]) == i ):
                capacity = int(aircraft_capacities[aircraft_type.strip('\n')])
                from_id = int(airports[dep_airport])
                to_id = int(airports[arr_airport])
                graph[from_id][to_id] = graph[from_id][to_id] + capacity
        graph_for_this_hour = Graph(graph)
        #print(graph)
        maxflow_hr.append(graph_for_this_hour.FordFulkerson(0,9))

    return sum(maxflow_hr)

if __name__=='__main__':
    input_text_file_path='C:\\Users\\rauna\\PycharmProjects\\first\\Flight_Data.txt'
    temp_file_path = 'C:\\Users\\rauna\\PycharmProjects\\first\\temp1.txt'
    maxflow_day = main(input_text_file_path,temp_file_path)
    print(maxflow_day)