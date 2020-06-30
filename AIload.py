import numpy as np

# def nonlin(x,deriv=False):
#     if(deriv==True):
#         return x*(1-x)
#     return 1/(1+np.exp(-x))

# syn = np.load('syn.npz')
# syn0 = syn['syn0']
# syn1 = syn['syn1']

# l0 = [[1,0,0]]
# l1 = nonlin(np.dot(l0,syn0))
# l2 = nonlin(np.dot(l1,syn1))

# print(l2)
width = 5
height = 15
pole = np.zeros((3))
px = []
py =[]
pole[1] = 1
for i in range(len(pole)):
    print(pole[i])