# Importing necessary librarY
import numpy as np
# Defining GLobal Parameters for the components in the circuit
VSOURCE = "V"
ISOURCE = "I"
RESISTOR = "R"

# "conversion" function which converts the scientific form of a number to a float type and 
#  ignores the comments if present
def conversion(n):
    v=0
    for i in n:
        if i == '#':
            v+=n.index(i)
    if v == 0:
        s=len(n)
    else:
        s=v
    return float(n[:s])

# "evalSpice" function to solves for node_volatges and node_currents in a linear resistive circuit
def evalSpice(filename):
    # Defining the necessary lists and dictionaries to store all the data we need
    R = []
    V = []
    I = []
    nodes = {}
    node_voltage = {}
    nodes_current = {}
    
    # "try" checks whether the input file exists or not
    # Else it raise FileNotFoundError
    try:
        f = open(filename,"r")
      
        # ".circuit" indicates that the circuit is going to begin
        # ".end" indicates the circuit is going to finish
        # If a circuit file doesn't consist  any of the terminal points then it is a Malformed 
        # circuit file, so any of the nodes aren't stored in nodes dictionary. Hence len(nodes)==0
        inCkt = False
        for i in f:
            if ".circuit" in i:
                inCkt = True
            elif ".end" in i:
                inCkt = False
            # All the relevant data is getting stored into the lists which are declared in the 
            # beginning, it raises ValueError when it finds different components other than 
            # Resistors, Voltage and Current Sources
            elif inCkt:
                j = i.split()
                if len(j)!=0:
                    if j[0][0]==VSOURCE or j[0][0]==ISOURCE or j[0][0]==RESISTOR:
                        node1,node2 = j[1],j[2]
                        # All the nodes are getting updated into a dictionary "nodes"
                        if node1 in nodes:
                                nodes[node1] += 1
                        else:
                            nodes[node1] = 1

                        if node2 in nodes:
                                nodes[node2] += 1
                        else:
                            nodes[node2] = 1
                        # Checking whether the Ground Node is specified since there must be a
                        # reference node with node voltage as zero
                        if "GND" not in nodes:
                            raise ValueError("No Ground Node is specified")

                        # R,V,I are getting updated into the corresponding dictionaries
                        # 'C' : Name given to the component, 'N1' : Positive Node
                        # 'N2' : Negative Node, 'M' : Value
                        try:
                            if j[0][0] == RESISTOR:
                                if conversion(j[3])!=0:
                                    R.append({'C':j[0],'N1':node1,'N2':node2,'M':conversion(j[3])})
                            elif j[0][0] == VSOURCE:
                                if j[3]=='dc':
                                    V.append({'C':j[0],'N1':node1,'N2':node2,'M':conversion(j[4])})
                                else:
                                    raise ValueError("Only DC Sources are allowed")
                            elif j[0][0] == ISOURCE:
                                if j[3]=='dc':
                                    I.append({'C':j[0],'N1':node1,'N2':node2,'M':conversion(j[4])})
                                else:
                                    raise ValueError("Only DC Sources are allowed")
                        except ValueError:
                            raise ValueError("Only V, I, R elements are permitted")

                    elif j[0][0]!='#':
                        raise ValueError("Only V, I, R elements are permitted")
        f.close()
        # Checking for repeated component names
        C_count = []
        for i in (R+V+I):
            C_count.append(i['C'])
        if len(set(C_count))!=len(C_count):
            raise ValueError("Malformed circuit file")
            
        # len(nodes) is equal to zero if there are no terminal points('.circuit','.end')
        if len(nodes)==0:
            raise ValueError("Malformed circuit file")
            
        # List with all components, which is helpful to find series current sources
        MCOMP = R+V+I
        # Checking for Parallel Voltage Sources
        if len(V)!=1:
            for v1 in V:
                for v2 in V:
                    if (v1['N1']==v2['N1'] and v1['N2']==v2['N2']):
                            raise ValueError("Circuit error: no solution")
        # Checking for Series Current Sources
        z=0
        for i1 in I:
            for i2 in I:
                if i1['N2']==i2['N1']:
                    for j in MCOMP:
                        if j['N1']==i1['N2'] or j['N2']==i1['N2']:
                            z+=1
        if z==2:
            raise ValueError("Circuit error: no solution")
        
        # Defining two matrices of required length to solve the set of linear equations
        length = len(nodes)
        A = np.zeros((length+len(V),length+len(V)))
        B = np.zeros(length+len(V))
        nodenum = {}
        # Assigning the integer values to the nodes to make the problem simpler
        c = 0
        for node in nodes:
            if node == 'GND':
                if node not in nodenum:
                    nodenum[node] = c
                    c+=1
        for node in nodes:
            if node!='GND':
                if node not in nodenum:
                    nodenum[node] = c
                    c+=1
        # All the equations are formed using Kirchoff's Laws
        # Forming Resistor Equations
        for r in R:
            resistance = r['M']
            A[nodenum[r['N1']]][nodenum[r['N2']]]-=(1/resistance)
            A[nodenum[r['N2']]][nodenum[r['N1']]]-=(1/resistance)  
            A[nodenum[r['N1']]][nodenum[r['N1']]]+=(1/resistance)
            A[nodenum[r['N2']]][nodenum[r['N2']]]+=(1/resistance)
        # Forming Volatge Sources equations
        for v in V:
            i = V.index(v)
            A[length+i][nodenum[v['N1']]] = 1.0
            A[length+i][nodenum[v['N2']]] = -1.0
            B[length+i]=v['M']
            A[nodenum[v['N1']]][length+i] = 1.0
            A[nodenum[v['N2']]][length+i] = -1.0
        # Forming Current Source Equations
        for i in I:
            B[nodenum[i['N2']]]=-1*i['M']
            B[nodenum[i['N1']]]=i['M']
        # Since we have a reference node, so we don't need the first column and first row of the 
        # matrix A to solve the system of equations
        M = []
        for i in A:
            M.append(i[1:])
        # "numpy.linalg.solve()" solves for the unknown variables
        # First "length" in 'sol' are node voltages and the remaining of them are current through 
        # the voltage sources
        try:
            x = np.linalg.solve(M[1:],B[1:])
            sol = np.insert(x,0,0)
        # If linalg.solve do not able to solve the given set of matrices A,B then it shows an Error
        except np.linalg.LinAlgError:
            raise ValueError("Circuit error: no solution")
        # Node voltages are getting updated to the dictionary 'node_voltage' with their 
        # corresponding names.
        for i in nodenum:
            node_voltage[i] = sol[nodenum[i]]
            
        # Currents are getting updated to the dictionary with the proper direction
        # {'n1':{'n3':10,...},...} implies that the current 10A is flowing from 'n1' to 'n3' and
        # current from 'n1' to 'n2' is additive inverse of current from 'n2' to 'n1'
        for v in V:
            nodes_current[v['C']]=sol[length+V.index(v)]
       
        # Returning Node Voltages and Nodes between the currents
        return (node_voltage,nodes_current)
    # FileNotFoundError : If no valid SPICE file
    except FileNotFoundError:
        raise FileNotFoundError("Please give the name of a valid SPICE file as input")  
