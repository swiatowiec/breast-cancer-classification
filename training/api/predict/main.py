from fastapi import FastAPI
from api.predict import endpoints
from api.predict.config import get_predict_application_settings
from containers_config import PredictContainer

settings = get_predict_application_settings()

container = PredictContainer()
container.config.artifacts_dir_path.from_value(settings.artifacts_dir_path)
container.wire(modules=[endpoints])


app = FastAPI()
app.container = container
app.include_router(endpoints.router)