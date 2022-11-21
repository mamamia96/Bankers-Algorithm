Mia Abbott
November 21st, 2022
CS2040
Algorithms Assignment Five - Bankers Algorithm

**OVERVIEW:**\n
    This program takes in a text file of integers. It is used to simulate a resource allocation matrix in the context of 
    operating systems and processes. It uses the Banker's Algorithm the program takes in requests in the form of vectors
    then checks these vectors for possible safe or unsafe states.

**TO RUN PROGRAM:**\n
    Navigate to the appropriate directory and use command -> 'python main.py "file_path" '
    file_path must be a text file in the format:
        n is the number of processes, m is the number of resource types
        FILE START
        n m
        max mat1
        max mat2
        max matn
        available vector
        FILE END

**INPUT:**\n
    The program will prompt the user for requests. First it will ask the user which process they desire to send to a request to. Then it
    will ask the user the specify #'s of resource types to request for the given process.

PROGRAM END:
    The program will run forever until the user enters '-1' for the process number when prompted.
