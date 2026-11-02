class Explainer:
    def explain(self, image, prediction, method="Grad-CAM", layer=None): raise NotImplementedError
    def evaluate(self, artifact, ground_truth=None): raise NotImplementedError
    def get_artifact(self, explanation_id): raise NotImplementedError
