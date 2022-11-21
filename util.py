"""
Utility file containing many helper functions for our driver code.
Most functions here are operations/displaying matrices and vectors.
"""

def print_matrix(m,s=''):
    # Function for printing individual matrix
    # s is an optional title parameter
    # if s is left default no title will be printed

    if s:
        print(s + ':')
    for row in m:
        print('[ ',end='')
        for cell in row:
            print(cell,end=' ')
        print(']')

def file_to_matrix(f):
    # Function for parsing a text file and returns multiple variables based on the file 'f'
    # f must be in the following format:
    # n is the number of processes, m is the number of resource types
    # FILE START
    # n m
    # max mat1
    # max mat2
    # max matn
    # available vector
    # FILE END
    # Returns 4 variables -> 1.n 2.m (ints), 3. max matrix (2d list), 4. available vec (list) 

    #opening and closing file and extracting info
    f = open(f, "r")
    file_str = f.read()
    f.close()

    #splitting all lines on new line (\n)
    lines = file_str.split('\n')

    #splitting first line on spaces to extract n and m 
    line_one = lines[0]
    n = int(line_one.split(' ')[0])
    m = int(line_one.split(' ')[1])

    #making list to store our max allocation matrix
    max = []

    for i in range(n):

        #we use i + 1 to avoid using the first line which is n and m
        line = lines[i+1]
        split_line = line.split(' ')
        max.append([int(c) for c in split_line])

    #splitting last line on spaces to get our available vector
    avail = [int(c) for c in lines[len(lines)-1].split(' ')]
    return [n,m,max,avail]

def copy_matrix(m : list, v=0):
    # Function for copying matrix m
    # If v is left as default value (0), the returned matrix will be have all entries be 0
    # If v is not 0 then the returned matrix will have identical values to matrix m
    # Returns copied matrix

    copy_m = []

    for row in m:
        if v == 0:
            copy_m.append([0 for i in range(len(row))])
        else:
            copy_m.append(row)

    return copy_m

def sub_matrix(m1,m2):
    # Function for subtracting matrix1 from matrix2
    # We are assuming matrix has identical dimensions
    # Returns a matrix which is equal to m1-m2

    #blank matrix to write to
    ret_mat = copy_matrix(m2)

    for i in range(len(m1)):
        #row
        for j in range(len(m1[i])):
            #cell
            ret_mat[i][j] = m1[i][j] - m2[i][j]

    return ret_mat

def copy_vec(v : list,val=0):
    # Function for copying a vector v
    # If val is left as default then vector entries are initialized to 0
    # If val is anything besides 0 it will copy values from v

    copy_vec = []
    for i in range(len(v)):
        if val == 0:
            copy_vec.append(0)
        else:
            copy_vec.append(v[i])
    return copy_vec

def le_vec(v1 : list,v2 : list):
    # Function that compares and returns boolean if v1 <= v2 (comparing individual entries)

    s_vec = sub_vec(v2,v1)
    for i in range(len(s_vec)):
        if s_vec[i] < 0:
            return False
    return True

def sub_vec(v1 : list,v2 : list):
    # Function for finding difference between v1 and v2
    # We are assuming vecs are identical dimensions
    # Returns resulting vector of differences

    v = []

    for i in range(len(v1)):
        v.append(v1[i]-v2[i])

    return v

def add_vec(v1 : list,v2 : list):
    # Function for adding two vectors v1 and v2
    # We are assuming vectors have identical dimensions
    # Returns resulting sum vector

    v = []
    for i in range(len(v1)):
        v.append(v1[i]+v2[i])
    return v

def true_vec(v : list):
    # Function for determing if all values in a vector are true
    # Returns true if all values in v are true and returns false otherwise

    for c in v:
        if not c:
            return False
    return True


def print_matrices(lm : list, spc=0):
    # Function for printing out multiple matrices
    # takes in list of matrices and prints them from left to right
    # lm = list of matrices
    # matrices can be different dimensions but they must be in descending order of.. 
    # ..(highest #rows, .., lowest #rows)
    # spc is an integer for how many spaces you want in between each matrix when printed

    # variable for storing the maximum amount of rows we will need to print later
    max_rows = 0

    # finding the max_rows
    for m in lm:
        if len(m) > max_rows:
            max_rows = len(m)

    spacer_str = ' ' * spc


    for i in range(max_rows):
        print("[",end='')
        mat_ind = 0
        for j in range(len(lm)):
            
            if i < len(lm[j]):
                for k in range(len(lm[j][i])):

                    if k == len(lm[j][i]) - 1:
                        print(f"{lm[j][i][k]}",end='')
                        if mat_ind != len(lm) - 1:
                            if i < len(lm[j+1]):
                                print(f"]{spacer_str}[",end='')
                    else:    
                        print(f"{lm[j][i][k]}, ",end='')
            mat_ind += 1

        print("]")

if __name__ == '__main__':
    print('This is a file of utility functions mostly pertaining to matrices and vectors.')