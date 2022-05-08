function [P] = productmatrix(G,M)
p=struct();
p.nodes = combvec( G.nodes,M.nodes);
n_nodes = size(p.nodes); n_nodes = n_nodes(2);
N = combvec(p.nodes,p.nodes);
s=size(N);
edges = [];
for I=1:s(2)
    i=N(2,I);
    j=N(1,I);
    a=N(4,I);
    b=N(3,I);
   
    if j==b
        entry = 0;
    elseif i==a
            entry = 0;
    else 
        entry = ( M.A(i,a)&&G.A(j,b) )  || (  (~M.A(i,a)) && (~G.A(j,b) ) );
    
    end

    
    edges = [edges , entry ];
       
       
   
end

p.A = reshape(edges,n_nodes,n_nodes);
P = p;
end
