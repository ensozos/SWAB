from numpy import arange, array, ones, vstack
from numpy.linalg import lstsq

class Approximation:
    def linear_interpolation(self, subsequence, subseq_range):
        return (subseq_range[0], subsequence[subseq_range[0]], subseq_range[1], subsequence[subseq_range[1]])

    def linear_regression(self, subsequence, subseq_range):
        p, error = self.leastsquareslinefit(subsequence, subseq_range)

        # compute y = mx + c
        y0 = p[0]*subseq_range[0] + p[1]
        y1 = p[0]*subseq_range[1] + p[1]
        return (subseq_range[0], y0, subseq_range[1], y1)

    def leastsquareslinefit(self, subsequence, subseq_range):
        x = arange(subseq_range[0], subseq_range[1] + 1)
        y = array(subsequence[subseq_range[0]:subseq_range[1]+ 1])

        A = vstack([x, ones(len(x))]).T
        (p,residuals,rank,s) = lstsq(A,y, -1) #rcond=-1 for futurewarning
        try:
            error = residuals[0]
        except IndexError:
            error = 0.0
        return (p,error)

    def sumsquerred_error(self, subsequence, segment):
        x0, y0, x1, y1 = segment

        error = self.leastsquareslinefit(subsequence, (x0, x1))[1]
        
        return error
