import numpy as np

def xcorr(x, *args):
    """
%XCORR Cross-correlation function estimates.
%   C = XCORR(A,B), where A and B are length M vectors (M>1), returns
%   the length 2*M-1 cross-correlation sequence C. If A and B are of
%   different length, the shortest one is zero-padded.  C will be a
%   row vector if A is a row vector, and a column vector if A is a 
%   column vector.
%
%   XCORR produces an estimate of the correlation between two random
%   (jointly stationary) sequences:
%          C(m) = E[A(n+m)*conj(B(n))] = E[A(n)*conj(B(n-m))]
%   It is also the deterministic correlation between two deterministic
%   signals.
%
%   XCORR(A), when A is a vector, is the auto-correlation sequence.   
%   XCORR(A), when A is an M-by-N matrix, is a large matrix with
%   2*M-1 rows whose N^2 columns contain the cross-correlation
%   sequences for all combinations of the columns of A.
%   The zeroth lag of the output correlation is in the middle of the 
%   sequence, at element or row M.
%
%   XCORR(...,MAXLAG) computes the (auto/cross) correlation over the
%   range of lags:  -MAXLAG to MAXLAG, i.e., 2*MAXLAG+1 lags.
%   If missing, default is MAXLAG = M-1.
%
%   [C,LAGS] = XCORR(...)  returns a vector of lag indices (LAGS).
%
%   XCORR(...,SCALEOPT), normalizes the correlation according to SCALEOPT:
%     'biased'   - scales the raw cross-correlation by 1/M.
%     'unbiased' - scales the raw correlation by 1/(M-abs(lags)).
%     'coeff'    - normalizes the sequence so that the auto-correlations
%                  at zero lag are identically 1.0.
%     'none'     - no scaling (this is the default).
%
%   See also XCOV, CORRCOEF, CONV, COV and XCORR2.

%   Author(s): R. Losada
%   Copyright 1988-2000 The MathWorks, Inc.
%   $Revision: 1.13 $  $Date: 2000/09/11 19:29:20 $ 
%
%   References:
%     S.J. Orfanidis, "Optimum Signal Processing. An Introduction"
%     2nd Ed. Macmillan, 1988.
    """

    nargin = len(args) + 1
    
    if nargin < 1 or nargin > 4:
        raise ValueError("Wrong number of input arguments.")
    
    x, nshift = np.squeeze(np.atleast_1d(x)), np.ndim(x)
    
    xIsMatrix, autoFlag, maxlag, scaleType, msg = parseinput(x, *args)
    
    if xIsMatrix:
        c, M, N = matrixCorr(x, maxlag)
    else:
        c, M, N = vectorXcorr(x, autoFlag, maxlag, *args)
    
    c = forceRealCorr(c, x, autoFlag, *args)
    
    lags = np.arange(-maxlag, maxlag + 1)
    
    if maxlag >= M:
        c = np.concatenate((np.zeros((maxlag - M + 1, N**2)), c[-M+1:], c[:M], np.zeros((maxlag - M + 1, N**2))))
    else:
        c = np.concatenate((c[-maxlag:], c[:maxlag+1]))
    
    c, msg = scaleXcorr(c, xIsMatrix, scaleType, autoFlag, M, maxlag, lags, x, *args)
    
    c = np.rollaxis(c, -1, -nshift)
    
    return c, lags

def ofacorr(of):
    MAXLAG = 8
    NDIVS = 4
    actmp = np.correlate(of, of, mode='full')
    ind1 = (len(actmp) + 1) // 2
    ind2 = min(len(actmp), ind1 + MAXLAG * NDIVS)
    ac = np.zeros(MAXLAG * NDIVS + 1)
    ac[:ind2 - ind1 + 1] = actmp[ind1:ind2 + 1]
    if ac[0] > 0:
        ac /= ac[0]
    return ac[2::2]

def parseinput(x, *args):
    xIsMatrix = np.ndim(x) > 1
    autoFlag = 1
    maxlag = None
    scaleType = ""
    msg = ""

    errMsg = "Input argument is not recognized."

    if len(args) == 1:
        if isinstance(args[0], str):
            scaleType = args[0]
        elif isinstance(args[0], int):
            maxlag = args[0]
        else:
            msg = errMsg
            return xIsMatrix, autoFlag, maxlag, scaleType, msg
    elif len(args) == 2:
        if isinstance(args[1], str):
            scaleType = args[1]
        elif isinstance(args[1], int):
            maxlag = args[1]
        else:
            msg = errMsg
            return xIsMatrix, autoFlag, maxlag, scaleType, msg
    elif len(args) == 3:
        autoFlag = 0
        maxlag = args[1]
        scaleType = args[2]

    return xIsMatrix, autoFlag, maxlag, scaleType, msg

def matrixCorr(x, maxlag):
    M, N = x.shape
    X = np.fft.fft(x, 2**np.ceil(np.log2(2*M-1)).astype(int))
    Xc = np.conj(X)
    C = np.empty((0, N**2))
    for n in range(N):
        C = np.hstack((C, np.tile(X[:, n], (1, N)) * Xc))
    c = np.fft.ifft(C).real
    return c, M, N

def vectorXcorr(x, autoFlag, maxlag, *args):
    x = np.squeeze(x)
    M, N = len(x), 1
    if autoFlag:
        X = np.fft.fft(x, 2**np.ceil(np.log2(2*M-1)).astype(int))
        c = np.fft.ifft(np.abs(X)**2).real
    else:
        y = np.squeeze(args[0])
        L = len(y)
        Mcached = M
        M = max(Mcached, L)
        if L != Mcached and max(L / Mcached, Mcached / L) > 10:
            neg_c = np.conj(np.fft.fftfilt(np.flipud(y), np.conj(x)))
            pos_c = np.flipud(np.fft.fftfilt(np.flipud(x), np.conj(y)))
            lneg, lpos = len(neg_c), len(pos_c)
            neg_c = np.hstack((np.zeros((lpos - lneg,)), neg_c[:-1]))
            pos_c = np.hstack((pos_c, np.zeros((lneg - lpos,))))
            c = np.hstack((pos_c, neg_c))
        else:
            if L != Mcached:
                x = np.hstack((x, np.zeros(L - Mcached)))
                y = np.hstack((y, np.zeros(Mcached - L)))
            X = np.fft.fft(x, 2**np.ceil(np.log2(2*M-1)).astype(int))
            Y = np.fft.fft(y, 2**np.ceil(np.log2(2*M-1)).astype(int))
            c = np.fft.ifft(X * np.conj(Y)).real
    return c, M, N

def forceRealCorr(c, x, autoFlag, *args):
    forceReal = False
    if (np.isreal(x).all() and autoFlag) or (np.isreal(x).all() and np.isreal(args[0]).all()):
        forceReal = True
    if forceReal:
        c = np.real(c)
    return c

def scaleXcorr(c, xIsMatrix, scaleType, autoFlag, M, maxlag, lags, x, *args):
    if scaleType == "none":
        return c, ""
    elif scaleType == "biased":
        c /= M
    elif scaleType == "unbiased":
        scale = np.maximum(M - np.abs(lags), 1)
        if xIsMatrix:
            scale = np.tile(scale, (len(c), 1))
        c /= scale
    elif scaleType == "coeff":
        if autoFlag:
            c /= c[maxlag]
        else:
            if not xIsMatrix:
                c /= np.linalg.norm(x) * np.linalg.norm(args[0])
            else:
                jkl = np.diag_indices_from(c.reshape(np.sqrt(c.shape[0]), np.sqrt(c.shape[0])))
                tmp = np.sqrt(c[maxlag, jkl])
                tmp = np.tile(tmp, (len(jkl[0]), 1)).T * np.tile(tmp, (len(jkl[0]), 1))
                c /= tmp
    return c, ""


# function [c,lags] = xcorr(x,varargin)

# error(nargchk(1,4,nargin));

# [x,nshift] = shiftdim(x);
# [xIsMatrix,autoFlag,maxlag,scaleType,msg] = parseinput(x,varargin{:});
# error(msg);

# if xIsMatrix,
# 	[c,M,N] = matrixCorr(x,maxlag);
# else
# 	[c,M,N] = vectorXcorr(x,autoFlag,maxlag,varargin{:});
# end

# % Force correlation to be real when inputs are real
# c = forceRealCorr(c,x,autoFlag,varargin{:});


# lags = [-maxlag:maxlag];


# % Keep only the lags we want and move negative lags before positive lags
# if maxlag >= M,
# 	c = [zeros(maxlag-M+1,N^2);c(end-M+2:end,:);c(1:M,:);zeros(maxlag-M+1,N^2)];
# else
# 	c = [c(end-maxlag+1:end,:);c(1:maxlag+1,:)];
# end

# % Scale as specified
# [c,msg] = scaleXcorr(c,xIsMatrix,scaleType,autoFlag,M,maxlag,lags,x,varargin{:});
# error(msg);

# % If first vector is a row, return a row
# c = shiftdim(c,-nshift);

# %----------------------------------------------------------------
# function [c,M,N] = matrixCorr(x,maxlag)
# % Compute all possible auto- and cross-correlations for a matrix input

# [M,N] = size(x);

# X = fft(x,2^nextpow2(2*M-1));

# Xc = conj(X);

# C = [];
# for n =1:N,
# 	C = [C,repmat(X(:,n),1,N).*Xc];
# end
# c = ifft(C);

# %----------------------------------------------------------------
# function [c,M,N] = vectorXcorr(x,autoFlag,maxlag,varargin)
# % Compute auto- or cross-correlation for vector inputs

# x = x(:);

# [M,N] = size(x);

# if autoFlag,
# 	% Autocorrelation
# 	% Compute correlation via FFT
# 	X = fft(x,2^nextpow2(2*M-1));
# 	c = ifft(abs(X).^2);
	
# else,
# 	% xcorrelation
# 	y = varargin{1};
# 	y = y(:);
# 	L = length(y);
	
# 	% Cache the length(x)
# 	Mcached = M;
	
# 	% Recompute length(x) in case length(y) > length(x)
# 	M = max(Mcached,L);
	
#     if (L ~= Mcached) & any([L./Mcached, Mcached./L] > 10),

# 		% Vector sizes differ by a factor greater than 10,
# 		% fftfilt is faster
# 		neg_c = conj(fftfilt(conj(x),flipud(y))); % negative lags
# 		pos_c = flipud(fftfilt(conj(y),flipud(x))); % positive lags
		
# 		% Make them of almost equal length (remove zero-th lag from neg)
# 		lneg = length(neg_c); lpos = length(pos_c);
# 		neg_c = [zeros(lpos-lneg,1);neg_c(1:end-1)];
# 		pos_c = [pos_c;zeros(lneg-lpos,1)];
		
# 		c = [pos_c;neg_c];
		
# 	else
# 		if L ~= Mcached,
# 			% Force equal lengths
# 			if L > Mcached
# 				x = [x;zeros(L-Mcached,1)];
				
# 			else,
# 				y = [y;zeros(Mcached-L,1)];
# 			end									
# 		end
		
# 		% Transform both vectors
# 		X = fft(x,2^nextpow2(2*M-1));
# 		Y = fft(y,2^nextpow2(2*M-1));
		
# 		% Compute cross-correlation
# 		c = ifft(X.*conj(Y));
# 	end
# end
	
# %----------------------------------------------------------------
# function [c,msg] = scaleXcorr(c,xIsMatrix,scaleType,autoFlag,...
# 	M,maxlag,lags,x,varargin)
# % Scale correlation as specified

# msg = '';

# switch scaleType,
# case 'none',
# 	return
# case 'biased', 
# 	% Scales the raw cross-correlation by 1/M.
# 	c = c./M;
# case 'unbiased', 
# 	% Scales the raw correlation by 1/(M-abs(lags)).
# 	scale = (M-abs(lags)).';
# 	scale(scale<=0)=1; % avoid divide by zero, when correlation is zero
	
# 	if xIsMatrix,
# 		scale = repmat(scale,1,size(c,2));
# 	end
# 	c = c./scale;
# case 'coeff',
# 	% Normalizes the sequence so that the auto-correlations
# 	% at zero lag are identically 1.0.
# 	if ~autoFlag,
# 		% xcorr(x,y)
# 		% Compute autocorrelations at zero lag
# 		cxx0 = sum(abs(x).^2);
# 		cyy0 = sum(abs(varargin{1}).^2);
# 		scale = sqrt(cxx0*cyy0);
# 		c = c./scale;
# 	else,
# 		if ~xIsMatrix,
# 			% Autocorrelation case, simply normalize by c[0]
# 			c = c./c(maxlag+1);
# 		else,
# 			% Compute the indices corresponding to the columns for which
# 			% we have autocorrelations (e.g. if c = n by 9, the autocorrelations
# 			% are at columns [1,5,9] the other columns are cross-correlations).
# 			[mc,nc] = size(c);
# 			jkl = reshape(1:nc,sqrt(nc),sqrt(nc))';
# 			tmp = sqrt(c(maxlag+1,diag(jkl)));
# 			tmp = tmp(:)*tmp; 
# 			cdiv = repmat(tmp(:).',mc,1);
# 			c = c ./ cdiv; % The autocorrelations at zero-lag are normalized to
# 			% one
# 		end
# 	end
# end	

# %----------------------------------------------------------------
# function [xIsMatrix,autoFlag,maxlag,scaleType,msg] = parseinput(x,varargin)
# %    Parse the input and determine optional parameters:
# %
# %    Outputs:
# %       xIsMatrix - flag indicating if x is a matrix
# %       AUTOFLAG  - 1 if autocorrelation, 0 if xcorrelation
# %       maxlag    - Number or lags to compute
# %       scaleType - String with the type of scaling wanted
# %       msg       - possible error message

# % Set some defaults
# msg = '';
# scaleType = '';
# autoFlag = 1; % Assume autocorrelation until proven otherwise
# maxlag = []; 

# errMsg = 'Input argument is not recognized.';

# switch nargin,
# case 2,
# 	% Can be (x,y), (x,maxlag), or (x,scaleType)
# 	if ischar(varargin{1}),
# 		% Second arg is scaleType
# 		scaleType = varargin{1};
		
# 	elseif isnumeric(varargin{1}),
# 		% Can be y or maxlag
# 		if length(varargin{1}) == 1,
# 			maxlag = varargin{1};
# 		else
# 			autoFlag = 0;
# 			y = varargin{1};
# 		end
# 	else
# 		% Not recognized
# 		msg = errMsg;
# 		return
# 	end
# case 3,
# 	% Can be (x,y,maxlag), (x,maxlag,scaleType) or (x,y,scaleType)
# 	maxlagflag = 0; % By default, assume 3rd arg is not maxlag
# 	if ischar(varargin{2}),
# 		% Must be scaletype
# 		scaleType = varargin{2};
		
# 	elseif isnumeric(varargin{2}),
# 		% Must be maxlag
# 		maxlagflag = 1;
# 		maxlag = varargin{2};
		
# 	else
# 		% Not recognized
# 		msg = errMsg;
# 		return
# 	end
	
# 	if isnumeric(varargin{1}),
# 		if maxlagflag,
# 			autoFlag = 0;
# 			y = varargin{1};
# 		else
# 			% Can be y or maxlag
# 			if length(varargin{1}) == 1,
# 				maxlag = varargin{1};
# 			else
# 				autoFlag = 0;
# 				y = varargin{1};
# 			end
# 		end
# 	else
# 		% Not recognized
# 		msg = errMsg;
# 		return
# 	end
	
# case 4,
# 	% Must be (x,y,maxlag,scaleType)
# 	autoFlag = 0;
# 	y = varargin{1};
	
# 	maxlag = varargin{2};
	
# 	scaleType = varargin{3};
# end

# % Determine if x is a matrix or a vector
# [xIsMatrix,m] = parse_x(x);



# if ~autoFlag,
# 	% Test y for correctness
# 	[maxlag,msg] = parse_y(y,m,xIsMatrix,maxlag);
# 	if ~isempty(msg),
# 		return
# 	end
# end

# [maxlag,msg] = parse_maxlag(maxlag,m);
# if ~isempty(msg),
# 	return
# end


# % Test the scaleType validity
# [scaleType,msg] = parse_scaleType(scaleType,errMsg,autoFlag,m,varargin{:});
# if ~isempty(msg),
# 	return
# end

	
# %-------------------------------------------------------------------
# function [xIsMatrix,m] = parse_x(x)


# xIsMatrix = (size(x,2) > 1);

# m = size(x,1);


# %-------------------------------------------------------------------
# function [maxlag,msg] = parse_y(y,m,xIsMatrix,maxlag)
# msg = '';
# [my,ny] = size(y);
# if ~any([my,ny] == 1),
# 	% Second arg is a matrix, error
# 	msg = 'B must be a vector (min(size(B))==1).';
# 	return
# end

# if xIsMatrix,
# 	% Can't do xcorr(matrix,vector)
# 	msg = 'When B is a vector, A must be a vector.';
# 	return
# end
# if (length(y) > m) & isempty(maxlag),
# 	% Compute the default maxlag based on the length of y
# 	maxlag = length(y) - 1;
# end

# %-------------------------------------------------------------------
# function [maxlag,msg] = parse_maxlag(maxlag,m)
# msg = '';
# if isempty(maxlag),
# 	% Defaul hasn't been assigned yet, do so
# 	maxlag = m-1;
# else	
# 	% Test maxlag for correctness	
# 	if  length(maxlag)>1
# 		msg = 'Maximum lag must be a scalar.';
# 		return
# 	end	
# 	if maxlag < 0,
# 		maxlag = abs(maxlag);
# 	end
# 	if maxlag ~= round(maxlag),
# 		msg = 'Maximum lag must be an integer.';
# 	end
# end

# %--------------------------------------------------------------------
# function c = forceRealCorr(c,x,autoFlag,varargin)
# % Force correlation to be real when inputs are real

# forceReal = 0; % Flag to determine whether we should force real corr

# if (isreal(x) & autoFlag) | (isreal(x) & isreal(varargin{1})),
# 	forceReal = 1;
# end


# if forceReal,
# 	c = real(c);
# end

# %--------------------------------------------------------------------
# function [scaleType,msg] = parse_scaleType(scaleType,errMsg,autoFlag,m,varargin)
# msg = '';
# if isempty(scaleType),
# 	scaleType = 'none';
# else
# 	scaleOpts = {'biased','unbiased','coeff','none'};
# 	indx = strmatch(lower(scaleType),scaleOpts);
	
# 	if isempty(indx),
# 		msg = errMsg;
# 		return
# 	else
# 		scaleType = scaleOpts{indx};
# 	end
	
# 	if ~autoFlag & ~strcmpi(scaleType,'none') &(m ~= length(varargin{1})),
# 		msg = 'Scale option must be ''none'' for different length vectors A and B.';
# 		return
# 	end
# end

# % EOF
