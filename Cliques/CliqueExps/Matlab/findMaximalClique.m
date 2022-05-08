function [x]  = findMaximalClique(A,xp,sharing)
S = size(A);
N = S(1);
A_ = tril(A,-1)+triu(ones(N,1)*ones(1,N));
[r,c]= find(A_==0);
maximum_clique = optimproblem('ObjectiveSense','maximize');
C = optimvar('C',N,'Type','integer','LowerBound',0,'UpperBound',1);
maximum_clique.Constraints.maxclique = C(r)+C(c)<=1;
if nargin==3
    if strcmp(sharing,"none") %none-> none of the nodes in xp is shared 
        maximum_clique.Constraints.excempt = sum(C(xp==1))==0;
        
    end
    
    if strcmp(sharing,"allow") %allow nodes to be shared
        "allow"
        maximum_clique.Constraints.excempt = sum(C(xp==0))>=1;
    end
        
        

end
maximum_clique.Objective = ones(1,N)*C;
sol = solve(maximum_clique);
x = sol.C;
end