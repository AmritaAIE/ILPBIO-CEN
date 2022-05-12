function pos = find_node(t,n)
    len = length(t);
    % default - element not found
    pos = -1;

    for i=1:len
        
        % after traversing if element is found return the position
        if isequal(t(i),n)
            pos = i;
            break;
        end
    end

end