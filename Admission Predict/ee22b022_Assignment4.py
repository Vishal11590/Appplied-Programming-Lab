# Import numpy to get access to linalg.lstsq()
import numpy as np

# Extracting the data points from the csv file
# There are 5 lists x1,x2,x3,x4,x5 := x1 consits of data points which are given
# x2 consists of squares of the datapoints given, similarly up to 5th degree
# Also the list 'b' consists of chance of admit values
file = open('Admission_Predict_Ver1.1.csv','r')
x1,x2,x3,x4,x5,b = [],[],[],[],[],[]
for i in file:
    j = i.split(',')
    if j[0]!='Serial No.':
        x1.append([int(j[1]),int(j[2]),int(j[3]),float(j[4]),float(j[5]),float(j[6]),int(j[7]),1])
        x2.append([int(j[1])**2,int(j[2])**2,int(j[3])**2,float(j[4])**2,float(j[5])**2,float(j[6])**2,int(j[7]),1])
        x3.append([int(j[1])**3,int(j[2])**3,int(j[3])**3,float(j[4])**3,float(j[5])**3,float(j[6])**3,int(j[7]),1])
        x4.append([int(j[1])**4,int(j[2])**4,int(j[3])**4,float(j[4])**4,float(j[5])**4,float(j[6])**4,int(j[7]),1])
        x5.append([int(j[1])**5,int(j[2])**5,int(j[3])**5,float(j[4])**5,float(j[5])**5,float(j[6])**5,int(j[7]),1])
        b.append(float(j[8]))

# GRE Score, TOEFL Score, University Rating, SOP, LOR, CGPA, Research, Chance
# Finding the coefficients of the parameters for all different types of functions using linlag.lstsq()
params1,_,_,_ = np.linalg.lstsq(x1,b,rcond=None)
params2,_,_,_ = np.linalg.lstsq(x2,b,rcond=None)
params3,_,_,_ = np.linalg.lstsq(x3,b,rcond=None)
params4,_,_,_ = np.linalg.lstsq(x4,b,rcond=None)
params5,_,_,_ = np.linalg.lstsq(x5,b,rcond=None)

# p1,p2,p3,p4,p5 are the lists containing chance of admit values for 5 different functions used 
# s1,s2,s3,s4,s4 represents Total Square Error for 5 different functions
p1,p2,p3,p4,p5 = [],[],[],[],[]
s1,s2,s3,s4,s5 = 0,0,0,0,0
for i in range(len(b)):
    temp1,temp2,temp3,temp4,temp5 = 0,0,0,0,0
    for j in range(len(params1)):
        temp1 += (params1[j]*x1[i][j])
        temp2 += (params2[j]*(x1[i][j])**2)
        temp3 += (params3[j]*(x1[i][j]**3))
        temp4 += (params4[j]*(x1[i][j]**4))
        temp5 += (params5[j]*(x1[i][j]**5))
    p1.append(temp1)
    p2.append(temp2)
    p3.append(temp3)
    p4.append(temp4)
    p5.append(temp5)
    s1 += (b[i]-temp1)**2
    s2 += (b[i]-temp2)**2
    s3 += (b[i]-temp3)**2
    s4 += (b[i]-temp4)**2
    s5 += (b[i]-temp5)**2

# Printing of Root Mean Square Error for 5 different functions
print("Root Mean Square Error for different order polynomials")
print(f"Order(1) : {(s1/len(b))**0.5}\nOrder(2) : {(s2/len(b))**0.5}\nOrder(3) : {(s3/len(b))**0.5}\nOrder(4) : {(s4/len(b))**0.5}\nOrder(5) : {(s5/len(b))**0.5}")
print("-------------------------------------------------------------")

# The Error is least for linear regression model
print("It is observed that error is Least for Linear Regression Model")
print(f"Chance of Admit = {round(params1[0],4)}*GRE Score + {round(params1[1],4)}*TOEFL Score + {round(params1[2],4)}*Rating + {round(params1[3],4)}*SOP + {round(params1[4],4)}*LOR + {round(params1[5],4)}*CGPA + {round(params1[6],4)}*Research - {round(abs(params1[7]),4)}")

# Finding the mean of ratio of Estimated Chance of Admit to given Chance of Admit
m = 0
for i in range(len(b)):
    m += (b[i]/p1[i])
print("-------------------------------------------------------------")
print("Straight line is constructed with Estimated Chance of Admit and given Chance of Admit")
print(f"Approximate Slope : {m/len(b)}")
