import insightface

from settings.settings import DeployConfig


class FaceModel:
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:
            config = DeployConfig()
            cls._model = insightface.app.FaceAnalysis()
            cls._model.prepare(ctx_id=config.gpu_id)

        return cls._model
