def evalTotalDistance(x, y):
    if x == y:
        return 0
    totalDistance = 0
    for i in range(len(x)):
        totalDistance += evalDistance(x[i], y[i])
    return totalDistance/len(x)
    
def evalDistance(x, y):

    if x == y:
        return 0
        
    I, J = len(x)+1, len(y)+1
    T = [[None] * J for i in range(I)]
    
    for i in range(I):
        T[i][0] = i
    for j in range(J):
        T[0][j] = j
    
    for i in range(1, I):
        for j in range(1, J):
            if x[i-1] == y[j-1]:
                T[i][j] = T[i-1][j-1]
            else:
                delete = T[i-1][j] + 1
                insert = T[i][j-1] + 1
                substi = T[i-1][j-1] + 1
                T[i][j] = min(delete, insert, substi)
    
    return 1.0 * T[I-1][J-1] / max(I-1, J-1)