"""
Mia Abbott
November 21st, 2022
CS2040
Algorithms Assignment Five - String Matching
"""
from util import * # Importing all functions from our helper file util.py
import sys         # Importing sys so we can take command line arguments

file_path = '' 

def safety(n : int,m : int,avail : list, max_m : list, alloc : list) -> bool:
    # Function for determining if the system is in a safe state based on passed in tables and values
    # Returns true if system is in a safe state, returns false if system in an unsafe state
    # n     = number of processes
    # m     = number of resource types
    # avail = vector of available resources
    # max_m = matrix of maximum number of resources each process can request 
    # alloc = matrix of allocated resources for each process

    # Getting our need matrix
    need = get_need(max_m, alloc)

    # Initializing finish vector with list comprehension
    finish = [False for i in range(n)]

    # List to store safe sequence of processes
    safe = []

    # Init work vector as a copy of available vector
    work = copy_vec(avail,1)

    count = 0

    while count < n:

        found = False
        for i in range(n):

            if not finish[i]:

                #seeing if all requirements of process i are met
                proc_finished = True
                for j in range(m):
                    if need[i][j] > work[j]:
                        proc_finished = False
                        break
                
                if proc_finished:
                    
                    for j in range(m):
                        work[j] = work[j] + alloc[i][j]

                    safe.append(i) #adding safe proc to sequence
                    count += 1     # this is num of processes that are in safe seq

                    finish[i] = True
                    found = True

        # If not a safe state we get caught here and exit function
        if not found:
            return False


    # Prints out a sequence of processes that the safe state leads to
    print('Sequence ',end='')
    for s in range(len(safe)):
        end_str = '->'
        if s == len(safe)-1: end_str = ' satisfies safety requirement.\n'
        print(f"P{safe[s]}",end=end_str)
    return True

def get_need(max_m : list, alloc  : int):
    # Function for setting the 'NEED' matrix in the safe state procedure (safety())

    # Initializing blank matrix to write to 
    ret_mat = copy_matrix(max_m,0)

    for i in range(len(max_m)): #looping through processes (rows)
        for j in range(len(max_m[0])): #looping through resource types (cols)
            ret_mat[i][j] = max_m[i][j] - alloc[i][j]
    return ret_mat

def valid_proc(p,n):
    # Function for checking if process (p) selected is valid
    # p has to be an integer, between 0 - (n-1) inclusively
    if p == None or p > (n-1) or p < 0:
        return False
    else:
        return True
    
def dump_mem(max_m, alloc, need, avail):
    # Function for displaying relevant memory in the banker's algorithm
    # Glorified driver function to use print_matrices util function
    titles = "MAX_M      ALLOC      NEED        AVAIL"
    print("==DUMP=MEMORY==")
    print(titles)
    print_matrices([max_m, alloc, need, [avail]],2)
    print('\n')

if __name__ == '__main__':

    # Number of arguments. We subtract 1 because sys.argv[0] is just the file name
    num_args = len(sys.argv) - 1

    if num_args < 1:
        print(f'{num_args} arguments passed. 1 required')
        exit()
    else:
        file_path = sys.argv[1]
        print('==BANKERS ALGORITHM==')
        print(f'Opening file {file_path}\n')

# Making sure file passed is able to be opened.
try:
    file_out = file_to_matrix(file_path)
except:
    print(f'Unable to open file at {file_path}. Terminating program')
    exit()

#############################################################
# Initializing values before we start main driver loop code #
#############################################################


# Getting variables from file to execute bankers algorithm
n, m, max_m, avail = file_out[0],file_out[1],file_out[2],file_out[3]

finish = [False for i in range(n)]
need = copy_matrix(max_m,1)

alloc = copy_matrix(max_m,0)

# First memory dump to file was correctly parsed
dump_mem(max_m, alloc, need, avail)

# p is used to store input from user when selecting which process to send request to
p = -2

# Main driver loop for taking requests
while True:

    ##############
    # INPUT CODE #
    ##############

    while not valid_proc(p, n):
        p = int(input(f'Which Process(0-{n-1}) would you like to send a request to?: '))
        print()
        if p == -1: # If user ends program
            break
    
    #if user ends program by inputting -1
    if p == -1:
        break
        
    req = [] # Request vector
    for i in range(m):
        new_entry = True # Using a boolean value to simulate a do while loop since python does not have them
        entry = -1
        while entry < 0:
            if new_entry:
                new_entry = False
            else:
                # If request is unacceptable we dump memory

                print(f"{entry} entered. Request is unacceptable. Values must be greater than or equal to 0")
                dump_mem(max_m, alloc, need, avail)

            entry = int(input(f"How much of resource {i} is Process {p} requesting?: "))
        
        req.append(entry)
    
    print(f"Checking request {req}")

    # Booleans used for storing whether or not request is acceptable.
    valid_req = True # if this becomes false then programs dumps and quits
    avail_resources = True
    err = "" #error string to print out if request is invalid later

    # If we get caught in here that means request is invalid.
    if not le_vec(req,need[p]):
        valid_req = False
        err = f"Unacceptable request. Process {p} has exceeded its maximum claim.\n"

    # Catch invalid requests
    if not valid_req:
        print(err)
        dump_mem(max_m, alloc, need, avail)
        p = -2
        continue

    # See if resources are free for request (comparing with avail)
    if not le_vec(req,avail):
        # User must make new request if resources aren't available for request currently
        avail_resources = False
        print(f"Unacceptable request. process {p} requested more resources than are available.")
        dump_mem(max_m, alloc, need, avail)
        p = -2
        continue

    # Making temporary variables so we can check state
    t_alloc = copy_matrix(alloc,1)
    t_need  = copy_matrix(need,1)

    t_avail = sub_vec(avail,req)
    t_alloc[p] = add_vec(alloc[p],req)
    t_need[p] = sub_vec(need[p],req)



    # Checking if our temp variables lead to a safe state
    print(f"Checking state after request -> {req}")

    if safety(n,m,t_avail,max_m,t_alloc):
        print(f"Acceptable request. Request {req} leads to safe state.")

        #make changes to actual matrices and vecs not copies
        avail    = sub_vec(avail,req)
        alloc[p] = add_vec(alloc[p],req)
        need[p]  = sub_vec(need[p],req)
        dump_mem(max_m, alloc, need, avail)
    else:
        print(f"Request {req} leads to an unsafe state. request denied.")
        dump_mem(max_m, alloc, need, avail)
    
    p = -2 # Resetting p so we can ask for new process in input code

# When we terminate program we dump memory

print("\nProcess terminating dumping memory...")
dump_mem(max_m, alloc, need, avail)








