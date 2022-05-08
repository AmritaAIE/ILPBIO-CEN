function [x]  = findnextMaximalClique(A,xp)
S = size(A);
N = S(1);
A_ = tril(A,-1)+triu(ones(N,1)*ones(1,N));
[r,c]= find(A_==0);
maximum_clique = optimproblem('ObjectiveSense','maximize');
C = optimvar('C',N,'Type','integer','LowerBound',0,'UpperBound',1);
maximum_clique.Constraints.maxclique = C(r)+C(c)<=1; 
maximum_clique.Constraints.avoids = sum(C(xp==1))== 0 ;
maximum_clique.Objective = ones(1,N)*C;
sol = solve(maximum_clique);
x = sol.C;
end