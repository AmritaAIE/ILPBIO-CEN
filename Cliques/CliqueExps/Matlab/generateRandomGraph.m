function A = generateRandomGraph(N,p)
adj = zeros(N,N);
for i =1:N
    for j=i:N
        
        if i~=j
             a = rand(1);
            if a>p
                adj(i,j)=1;
                adj(j,i)=1;
            end
        
        end
       
        
    end
    
end
A = adj;
end