from approximation import Approximation

class Segmentation:
    """ 
    There is already an impl out for basic algorithms from NickFoubert.
    """
    def __init__(self):
        self.approximation = Approximation()

    def merge_segment(self, T, pos, create_segment):
        return create_segment(self.approximation, T, pos)

    def sliding_window_segmentation(self, T, max_error, create_segment, compute_error):
        N = len(T)
        
        anchor = 0
        seq_TS = []
        while anchor != N - 1:
            i = 1
            while compute_error(self.approximation, T, (anchor, T[anchor], anchor + i, T[anchor + i - 1])) < max_error:
                i += 1
                if anchor + i >= N:
                    break
            segment = create_segment(self.approximation, T, (anchor,anchor + i - 1))
            seq_TS.append(segment)
 
            anchor = anchor + i - 1

        return seq_TS

    def bottom_up_segmentation(self, T, max_error, create_segment, compute_error):
        seq_TS = []
        merge_cost = []
        merged_segments = []

        for i in range(0, len(T)-1):
            #Create inition fine approximation
            seq_TS.append(create_segment(self.approximation, T, (i, i + 1)))
        for i in range(0, len(seq_TS)-1):
            merged_segments.append(create_segment(self.approximation, T, (seq_TS[i][0], seq_TS[i+1][2])))
        for segment in merged_segments:
            merge_cost.append(compute_error(self.approximation, T, segment))

        while min(merge_cost) < max_error:
            i = merge_cost.index(min(merge_cost))
            seq_TS[i] = self.merge_segment(T, (seq_TS[i][0], seq_TS[i+1][2]), create_segment)

            del seq_TS[i+1]

            if i > 0:
                merged_previous_segment = self.merge_segment(T, (seq_TS[i-1][0], seq_TS[i][2]), create_segment)
                merge_cost[i-1] = compute_error(self.approximation, T, merged_previous_segment) 
           
            if i + 1 < len(merge_cost):
                merged_next_segment = self.merge_segment(T, (seq_TS[i][0], seq_TS[i+1][2]), create_segment)
                merge_cost[i] = compute_error(self.approximation, T, merged_next_segment)

            del merge_cost[i]

        return seq_TS

   