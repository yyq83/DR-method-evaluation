function [positive_id, crossval_id] = train_test_split(data, nfolds, flag)

    if nargin < 3
        flag = '1';
    end

    if nargin < 2
        nfolds = 5;
    end

    if flag == '1'
        positive_id = find(data); %找出所有非0元素
        crossval_id = crossvalind('Kfold',positive_id(:),nfolds);
    end

    if flag == '2'
        [row, col] = size(data);
        split = crossvalind('Kfold',1:1:row,nfolds);
        positive_id = find(data);
        crossval_id = zeros(length(positive_id),1);

        for i = 1:length(positive_id)
            [r, ~] = ind2sub([row, col], positive_id(i)); 
            crossval_id(i) = split(r);
        end
    end

     if flag == '3'
        [row, col] = size(data);
        split = crossvalind('Kfold',1:1:col,nfolds);
        positive_id = find(data);
        crossval_id = zeros(length(positive_id),1);
		
        for i = 1:length(positive_id)
            [~, c] = ind2sub([row, col], positive_id(i)); 
            crossval_id(i) = split(c);
        end
     end

end
