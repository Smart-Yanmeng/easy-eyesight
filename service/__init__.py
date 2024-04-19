import insightface

from settings.settings import DeployConfig

config = DeployConfig()
model = insightface.app.FaceAnalysis()
model.prepare(ctx_id=config.gpu_id)
