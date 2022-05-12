function sol = seq_alignment(seq1,seq2)
seq = convertStringsToChars(seq1+reverse(seq2));
n= length(seq);
vars = optimvar("vars",[n,n],"LowerBound",0,"Type","integer","UpperBound",1);
sum = optimexpr;
for i=1:n
    for j=i:n
        sum = sum + vars(i,j);
    end
end
r=[];
c=[];
list1 = [];
for i=1:n
    for j=1:n
        if i>=j
            eqn = vars(i,j)==0;
            list1 = [list1;eqn];
        end
    end
end
rna_fold = optimproblem('ObjectiveSense','maximize');
list1 = [];
for i = 1:length(r)
    eqn = vars(r(i),c(i))==0;
    list1 = [list1;eqn];
end
rna_fold.Constraints.neccesary = list1;
rna_fold.Objective = sum;
eqnns1 = [];
for i=1:n
    for j=1:n
        if i<j
            if seq(i)~=seq(j)
                eqn = vars(i,j) == 0;
                eqnns1 = [eqnns1;eqn];
            end 
        end
    end
end
rna_fold.Constraints.set1 = eqnns1;
eqnns2 = [];
for i=1:n
    eqn = optimexpr;
    for j=1:n
        if i~=j
            if i<j
                eqn = eqn+vars(i,j);
            elseif i>j
                eqn = eqn+vars(j,i);
            end
        end
    end
    eqns = eqn<=1;
    eqnns2 = [eqnns2;eqns];
end
rna_fold.Constraints.set2 = eqnns2;
nums = nchoosek([1:length(seq)],4);
eqnns3 = [];
b = size(nums);
for i=progress(1:b(1))
    eqn = vars(nums(i,1),nums(i,3))+vars(nums(i,2),nums(i,4))<=1;
    eqnns3 = [eqnns3;eqn];
end
rna_fold.Constraints.set3 = eqnns3;
[sol,~] = solve(rna_fold);
begin = [];
end1 = [];
for i=1:n
    for j=1:n
        if sol.vars(i,j)==1
            begin = [begin,i];
            end1 = [end1,j];
        end
    end
end
dot_bracket = '';
for i=1:length(seq)
    if ismember(i,begin)
        dot_bracket = [dot_bracket,'('];
    elseif ismember(i,end1)
        dot_bracket = [dot_bracket,')'];
    else
        dot_bracket = [dot_bracket,'.'];
    end
end
rnaplot(dot_bracket,'Format','Diagram','Sequence',seq);
rnaplot(dot_bracket,'Format','Graph');
end