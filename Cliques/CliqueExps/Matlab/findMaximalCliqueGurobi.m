function [x] = findMaximalCliqueGurobi(Adj)

n_nodes = size(Adj); n_nodes = n_nodes(1);
A_ = tril(Adj,-1)+triu(ones(n_nodes,1)*ones(1,n_nodes));
[r,c]= find(A_==0);
n_constraints = length(r);
constraints = zeros(n_constraints,n_nodes);
for i=1:n_constraints
    constraints(i,r(i))=1;
    constraints(i,c(i))=1;
end

obj = ones(1,n_nodes);
rhs = ones(1, n_constraints);


model.A = sparse(constraints);
model.obj = obj;
model.rhs = rhs;
model.sense = '<';
model.vtype = 'B';
model.modelsense = 'max';

params.outputflag = 0;

result = gurobi(model, params);
x = result.x;
end

