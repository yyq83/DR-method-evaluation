function method_pre(method, Dataset, OutputFolder)
    % Add paths to necessary folders
    addpath('./Datasets'); % Add the folder where datasets are stored
    addpath(['../' OutputFolder]); % Add the output folder to the path

    %%%%% 1. Load Datasets %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    addpath('Functions');
    load(Dataset); % Load the dataset specified as input
    A_DR = didr;
    R = (drug_ChemS + drug_AtcS + drug_SideS + drug_DDIS + drug_TargetS) / 5;
    D = (disease_PhS + disease_DoS) / 2;
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %%%%% 2. Algorithm Code %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    alpha = 10;
    beta = 10;
    gamma = 0.1;
    threshold = 0.1;
    maxiter = 300;
    tol1 = 2 * 1e-3;
    tol2 = 1 * 1e-5;

    % 2.1 Bounded Matrix Completion
    trIndex = double(A_DR ~= 0);
    [A_bmc, iter] = fBMC(alpha, beta, A_DR, trIndex, tol1, tol2, maxiter, 0, 1);
    A_DR0 = A_bmc .* double(A_bmc > threshold);

    % 2.2 Gaussian Radial Basis function
    A_RR = fGRB(R, 0.5);
    A_DD = fGRB(D, 0.5);

    % 2.3 Heterogeneous Graph Inference
    A_recovery = fHGI(gamma, A_DD, A_RR, A_DR0);
    pre = A_recovery';
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

    %%%%%% 3. Save to CSV %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    outputFileName = fullfile(['../' OutputFolder], [method '_' Dataset '.csv']);
    dlmwrite(outputFileName, pre, 'precision', '%.4f');
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
end
