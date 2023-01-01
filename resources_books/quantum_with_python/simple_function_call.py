import scipy.linalg.lapack as la 
import numpy as np 

A=np.array([[1,2,3],[2,4,5],[3,5,6]])

# using something aclled la.dsyev
eigenvalues, eigenvectors, info= la.dsyev(A)

print("Eigenvalues of symmetric matrix")
print(eigenvalues)

print("Eigenvectors of symmetric matrix")
print(eigenvectors)

U, sigma, VT, info = la.dgesvd(A)

print("The singular values")
print(sigma)
