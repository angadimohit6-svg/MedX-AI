class Calibrator:
    def fit(self, predictions, labels): raise NotImplementedError
    def calibrate(self, predictions): raise NotImplementedError
    def evaluate(self, predictions, labels): raise NotImplementedError
    def get_reliability_data(self): raise NotImplementedError
