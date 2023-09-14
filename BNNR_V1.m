clear all
addpath('Datasets');
%% 1. Load Datesets
load TLHGBI
Wrr = drug;
Wdd = disease;
Wdr = didr;
Wrd = Wdr';
A = Wrd;


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
	[dn,dr] = size(Wdr);
	%% 2. BNNR algorithm
	maxiter = 300;
	alpha = 1;
	beta = 10;
	tol1 = 2*1e-3;
	tol2 = 1*1e-5;
    %[Wrr,Wdd]=get_new_wdd_wrr(Wrd);
	T = [Wrr, Wdr'; Wdr, Wdd];
	[t1, t2] = size(T);
	trIndex = double(T ~= 0);
	[WW,iter] = BNNR(alpha, beta, T, trIndex, tol1, tol2, maxiter, 0, 1);
	M_recovery = WW((t1-dn+1) : t1, 1 : dr);
	Rt = M_recovery';

	origin = [A(PtestID); A(NtestID)];
	pred = [Rt(PtestID); Rt(NtestID)];

	writematrix(origin, ['origin',  num2str(fold), '.csv']);
	writematrix(pred, ['pre', num2str(fold), '.csv']);

end

%% 3. save with .txt
%%dlmwrite('results.txt',M_recovery,'delimiter','\t','precision',4)
%%dlmwrite('results.csv',M_recovery,'precision','%.4f');
