def size(T=0, G=0, M=0, K=0, B=0):
    return (T * (2 ** 40) + G * (2 ** 30) 
        + M * (2 ** 20) + K * (2 ** 10) + B)