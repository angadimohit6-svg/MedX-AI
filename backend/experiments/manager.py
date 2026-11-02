class ExperimentManager:
    def create(self, payload): raise NotImplementedError
    def list(self): raise NotImplementedError
    def compare(self, experiment_ids): raise NotImplementedError
