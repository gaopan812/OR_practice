import cvxpy as cp
import time

K = 300
K = 200
W = 80
n = [46, 22, 43] 
w = [10, 11, 19]
n = list(range(20,30))
w = list(range(15,25))
y = cp.Variable(K, boolean=True)
x = cp.Variable((K,len(n)), integer=True)
obj = cp.Minimize(y.sum())
constraints = [cp.sum(x, axis=0) >= n, x >=0] # demand constraints
for k in range(K):
    constraints += [w@x[k] <= W*y[k]]
prob = cp.Problem(obj, constraints)
time_start = time.time()
prob.solve(solver=cp.GUROBI)
#prob.solve()
time_end = time.time()
print(prob.status)
print(prob.value)
print(f'{(time_end - time_start):.4f} seconds')
# print(x.value)
