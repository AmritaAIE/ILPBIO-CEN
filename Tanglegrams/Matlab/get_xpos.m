function xpositions = get_xpos(i,j)
    global T1 T2 x1 x2 xx1 xx2 N nums_2 ist jst nums_1
    
    su = zeros(N,1);
    p1 = find(nums_1==ist);
    su(p1) = 1;
    p2 = find(nums_1==jst);
    su(p2) = 1;
    su = logical(su);

    % finding the subtree with the root as lowest common ancestor of i,j in
    % first tree
    t1 = subtree(T1,su);
    

    su1 = zeros(N,1);
    p1 = find(nums_2==ist);
    su1(p1) = 1;
    p2 = find(nums_2==jst);
    su1(p2) = 1;
    su1 = logical(su1);

    % finding the subtree with the root as lowest common ancestor of i,j in
    % second tree
    t2 = subtree(T2,su1);
    
    % in the following lines of code we will be determining the position of
    % the variable in X1,X2 representing the subtree exchange about the
    % LCA(i,j)

    % check if the subtree has already been encountered
    pos1 = find_node(xx1,t1);
    pos2 = find_node(xx2,t2);

    if pos1 == -1
        % if not encountered return the position of the subtree
        x1 = x1 + 1;
        xx1 = [xx1 t1];
        xpos = x1;
        
    else
        % if encountered return the position of the tree in the array of
        % subtrees
        xpos = pos1;
    end
    
    % similar operation on X2
    if pos2 == -1
        x2 = x2 + 1;
        xx2 = [xx2 t2];
        xpos2 = x2;
        
    
    else
        xpos2 = pos2;
    end
    
    xpositions = [xpos xpos2];
    
end