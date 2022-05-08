function [x] = findNearClique(A,k,xp,sharing)

S = size(A);
N = S(1);
A_ = tril(A,-1)+triu(ones(N,1)*ones(1,N));
[r,c]= find(A_==0);
maximum_clique = optimproblem('ObjectiveSense','maximize');
C = optimvar('C',N,'Type','integer','LowerBound',0,'UpperBound',1);
V = optimvar('V',length(r),'Type','integer','LowerBound',0,'UpperBound',1);
maximum_clique.Constraints.edgeConstraint = C(r)+C(c)-V(1:length(r))<=1 ; 
maximum_clique.Constraints.maxAddableEdges = sum(V)<=k;
if nargin==4
    if strcmp(sharing,"none")
        maximum_clique.Constraints.excempt = sum(C(xp==1))==0;
    end
    if strcmp(sharing,"allow")
         maximum_clique.Constraints.excempt = sum(C(xp==0))>= 1;
    end 

end
maximum_clique.Objective = sum(C);
show(maximum_clique)
sol = solve(maximum_clique);
x = sol;

end