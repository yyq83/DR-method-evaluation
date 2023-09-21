clear all
addpath('Datasets');
addpath('Functions');
%% 1. Load Datesets
load iDrug_ms
A_DR = didr;
Wdr = A_DR;
Wrd = Wdr';
A = Wrd;
R = (drug_ChemS+drug_AtcS+drug_SideS+drug_DDIS+drug_TargetS)/5;
D = (disease_PhS+disease_DoS)/2;

folds = 10;
[positiveId, crossval_id] = train_test_split(A, folds, '1');
for fold=1:folds
	Wrd = A;
	PtestID = positiveId(crossval_id==fold);
	negativeID = find(Wrd==0);
	num = numel(negativeID);
	Nidx = randperm(num);
	NtestID = negativeID(Nidx(1:length(PtestID)));
	Wrd(PtestID) = 0;
	Wdr = Wrd';
        A_DR=Wdr;

	%% 2. HGIMC algorithm
	alpha = 10; 
	beta = 10; 
	gamma = 0.1; 
	threshold = 0.1;
	maxiter = 300; 
	tol1 = 2*1e-3;   
	tol2 = 1*1e-5;

	% 2.1 Bounded Matrix Completion
	trIndex = double(A_DR ~= 0);
	[A_bmc, iter] = fBMC(alpha, beta, A_DR, trIndex, tol1, tol2, maxiter, 0, 1);
	A_DR0 = A_bmc.*double(A_bmc > threshold);

	% 2.2 Gaussian Radial Basis function
	A_RR = fGRB(R, 0.5);
	A_DD = fGRB(D, 0.5);


	% 2.3 Heterogeneous Graph Inference 
	A_recovery = fHGI(gamma, A_DD, A_RR, A_DR0);
	Rt = A_recovery';


	origin = [A(PtestID); A(NtestID)];
	pred = [Rt(PtestID); Rt(NtestID)];

	writematrix(origin, ['origin',  num2str(fold), '.csv']);
	writematrix(pred, ['pre', num2str(fold), '.csv']);

end
