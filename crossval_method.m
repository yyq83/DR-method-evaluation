function crossval_method(method, Dataset, OutputFolder)
    % Add the necessary folder to the MATLAB path 
    addpath('./Datasets'); 

    % Create a folder path to save cross-validation results
    DatasetFolder = fullfile('../', OutputFolder, method, Dataset);
    addpath(DatasetFolder)

    %% 1. Load Datasets%%%%%%%%%%%%%%%%%%%%%%%%
    % Load the dataset specified in the input
    load(Dataset);
    
    % Extract matrices from loaded data
    Wrr = drug;
    Wdd = disease;
    Wdr = didr;
    Wrd = Wdr';
    A = Wrd;

    folds = 10;
    
    % Split the data into training and testing sets
    [positiveId, crossval_id] = train_test_split(A, folds, '1');

    for fold = 1:folds
        Wrd = A;
        PtestID = positiveId(crossval_id == fold);
        negativeID = find(Wrd == 0);
        num = numel(negativeID);
        Nidx = randperm(num);
        NtestID = negativeID(Nidx(1:length(PtestID)));
        Wrd(PtestID) = 0;
        Wdr = Wrd';
        [dn, dr] = size(Wdr);


        %%%%%%%% 2. Algorithm Code %%%%%%%%%%%%%%%%%%%%%%%%%%
        %% Algorithm Parameters
        maxiter = 300;
        alpha = 1;
        beta = 10;
        tol1 = 2 * 1e-3;
        tol2 = 1 * 1e-5;
        
        % Construct the combined matrix T
        T = [Wrr, Wdr'; Wdr, Wdd];
        [t1, t2] = size(T);
        
        % Create a binary mask for T
        trIndex = double(T ~= 0);
        
        % Apply the BNNR algorithm to recover missing values in T
        [WW, iter] = BNNR(alpha, beta, T, trIndex, tol1, tol2, maxiter, 0, 1);
        
        % Extract the recovered matrix corresponding to A
        M_recovery = WW((t1 - dn + 1) : t1, 1 : dr);
        Rt = M_recovery';

        % Prepare data for evaluation
        origin = [A(PtestID); A(NtestID)];
        pred = [Rt(PtestID); Rt(NtestID)];


        %%%%%%%%% 3. Save to CSV %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        % Define file names for saving results
        origFileName = fullfile(DatasetFolder, ['origin', num2str(fold), '.csv']);
        predFileName = fullfile(DatasetFolder, ['pre', num2str(fold), '.csv']);

        % Write the original and predicted data to CSV files
        writematrix(origin, origFileName);
        writematrix(pred, predFileName);
    end
end
