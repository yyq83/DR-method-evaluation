function method_pre(method, Dataset, OutputFolder)
    % Add paths to necessary folders
    addpath('./Datasets'); % Add the folder where datasets are stored
    addpath(['../' OutputFolder]); % Add the output folder to the path

    %%%%% 1. Load Datasets %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    load(Dataset); % Load the dataset specified as input
    Wrr = drug;
    Wdd = disease;
    Wdr = didr;
    Wrd = Wdr';
    [dn, dr] = size(Wdr);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %%%%% 2. Algorithm Code %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    maxiter = 300;
    alpha = 1;
    beta = 10;
    tol1 = 2 * 1e-3;
    tol2 = 1 * 1e-5;
    T = [Wrr, Wdr'; Wdr, Wdd];
    [t1, t2] = size(T);
    trIndex = double(T ~= 0);
    [WW, iter] = BNNR(alpha, beta, T, trIndex, tol1, tol2, maxiter, 0, 1);
    pre = WW((t1 - dn + 1) : t1, 1 : dr);
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


    %%%%%% 3. Save to CSV %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    outputFileName = fullfile(['../' OutputFolder], [method '_' Dataset '.csv']);
    dlmwrite(outputFileName, pre, 'precision', '%.4f');
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
end
