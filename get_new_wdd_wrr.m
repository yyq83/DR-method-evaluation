function [newWrr, newWdd] = get_new_wdd_wrr(Wrd)

[row, column] = size(Wrd);
newWrr = zeros(row);
newWdd = zeros(column);

% 生成newWrr
for i=1:row
    index1 = find(Wrd(i,:)==1);
    for j=1:row
        count = 0;
        if i==j
            newWrr(i,j) = length(find(Wrd(i,:)==1));
        else
            index2 = find(Wrd(j,:)==1);
            for n=1:length(index1)
                if ismember(index1(n), index2)
                    count=count+1;
                end
            end
            newWrr(i,j) =count;
        end
    end
end

% 生成newWdd
for i=1:column
    index1 = find(Wrd(:,i)==1);
    for j=1:column
        count = 0;
        if i==j
            newWdd(i,j) = length(find(Wrd(:,i)==1));
        else
            index2 = find(Wrd(:,j)==1);
            for n=1:length(index1)
                if ismember(index1(n), index2)
                    count=count+1;
                end
            end
            newWdd(i,j) =count;
        end
    end
end

end