clear all
edgs = readlines("data\Spoke_TAP_format.txt")
edgs = edgs(1:end-1);
n_edges = length(edgs)

nodes = [];

for i=1:n_edges-1
    [n1,n2] = split(edgs(i),"	");
    
    if ~any(strcmp(nodes,n1(1)))
       
        nodes = [nodes; n1(1)];
        
    end
    
    if ~any(strcmp(nodes,n1(2)))
        nodes = [nodes; n1(2)];
        
    end
    
end

n_nodes = length(nodes);


Adj = zeros(n_nodes,n_nodes) + eye(n_nodes);

for i=1:n_edges-1
    [n1,n2] = split(edgs(i),"	");
    n1_idx = find(nodes==n1(1));
    n2_idx = find(nodes==n1(2));
    
    Adj(n1_idx,n2_idx)=1;
    Adj(n2_idx,n1_idx)=1;
    
    
end
sol = invNearClique(Adj,4,3)