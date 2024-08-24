from gurobipy import *
import time
W = 80
demand = [46,22,43] 
demand_type = [10, 11, 19] 
demand = list(range(20,30))
demand_type = list(range(15,25))
time_start = time.time()
MP = Model("MP")
MP.setParam("OutputFlag", 0)
x = MP.addVars(len(demand), obj =1)
MP.addConstrs(x[i] * (W//demand_type[i]) >= demand[i] 
                for i in range(len(demand)))
MP.optimize()

y = MP.getAttr(GRB.Attr.Pi, MP.getConstrs())

SP = Model("SP")
SP.setParam("OutputFlag", 0)
a = SP.addVars(len(demand), lb = 0, vtype= GRB.INTEGER)
SP.setObjective(1-a.prod(y), GRB.MINIMIZE)
SP.addConstr(a.prod(demand_type) <= W)
SP.optimize()

iter = 0
while SP.objVal < -0.001:
    iter += 1
    print("iteration: ", iter)
    print(f"新列的检验数为{SP.objVal:.6f}")
    column_coeff = SP.getAttr('x', SP.getVars()) 
    column = Column(column_coeff, MP.getConstrs())
    MP.addVar(obj=1, lb =0, column=column)
    MP.optimize()
    y = MP.getAttr(GRB.Attr.Pi, MP.getConstrs())
    SP.setObjective(1-a.prod(y), GRB.MINIMIZE)
    SP.optimize()

for v in MP.getVars():
    v.setAttr('vtype', GRB.INTEGER)
MP.optimize()
time_end = time.time()
print(f"最少使用的木材数量为:{MP.objVal:.2f}。")
print(f"求解时间：{time_end-time_start:.2f}s")