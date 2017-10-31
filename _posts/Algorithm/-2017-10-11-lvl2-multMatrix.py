def productMatrix(A, B):
    if len(A[0]) == len(B):
        for i in range(len(A[0])):
            for j in range(len(A[0])):
                for k in range(len(B[0])):
                    print(i, k, k, j)
                    # print(A[i][k], B[k][j])



a = [[ 1, 2 ],
     [ 2, 3 ],
     [ 4, 5 ]]
b = [[ 3, 4, 5 ],
     [ 5, 6, 7 ]]

productMatrix(a, b)