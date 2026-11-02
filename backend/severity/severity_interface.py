class SeverityProvider:
    def get_severity(self, result): raise NotImplementedError
    def get_severity_confidence(self, result): raise NotImplementedError
    def get_model_info(self): raise NotImplementedError
