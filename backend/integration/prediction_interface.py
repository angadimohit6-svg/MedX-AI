class PredictionProvider:
    """Adapter contract for a researcher-owned inference pipeline."""

    def predict(self, image_path):
        raise NotImplementedError
