class UncertaintyEstimator:
    def estimate(self, inputs): raise NotImplementedError
    def evaluate(self, predictions, labels): raise NotImplementedError
    def get_uncertainty(self, result): raise NotImplementedError
