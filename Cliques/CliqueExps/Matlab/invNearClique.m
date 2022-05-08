function [x,edges] = invNearClique(A,k,d,xp,sharing,varargin)
for i = 1:2:length(varargin) 
    if ischar(varargin{i}) 
        params.(varargin{i}) = varargin{i+1};
        
    end
end

S = size(A);
N = S(1);
A_ = tril(A,-1)+triu(ones(N,1)*ones(1,N));
[r,c]= find(A_==0);

inverse_near_clique = optimproblem('ObjectiveSense',"minimize");

C = optimvar('C',N,'Type','integer','LowerBound',0,'UpperBound',1);
V = optimvar('V',length(r),'Type','integer','LowerBound',0,'UpperBound',1);
W = optimvar('W',1,'Type','integer',"LowerBound",0);
inverse_near_clique.Constraints.maxreq = sum(C)>=k+d;
inverse_near_clique.Constraints.minedge = sum(V)<=W;
inverse_near_clique.Constraints.edgeConstraint = C(r)+C(c)-V(1:length(r))<=1 ; 

inverse_near_clique.Objective = W;

if nargin>=5
    if strcmp(sharing,"none")
        inverse_near_clique.Constraints.excempt = sum(C(xp==1))==0;
    end
    if strcmp(sharing,"allow")
         inverse_near_clique.Constraints.excempt = sum(C(xp==0))>= 1;
    end 
    
     if length(varargin)>=2
         
        if strcmp('Gurobi',params.solver)
            
            options = optimoptions ('intlinprog');
        end
    end
   

end

sol = solve(inverse_near_clique);
x = sol;
eds = [r,c];
edges = eds(sol.V==1,:);

end