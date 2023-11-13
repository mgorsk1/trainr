import threading
import time

import uvicorn
from fastapi import FastAPI

from trainr.api.v1 import v1
from trainr.api.v1.model.health import HealthApiModel


# class BackgroundTasks(threading.Thread):
#     def run(self, *args, **kwargs):
#         val = 5
#         while True:
#             val = val + 5
#             requests.post('localhost:1337/api/v1/hr/', params=dict(value=val + 5))
#
#             # Set fan
#
#             requests.post('localhost:1337/api/v1/light')
#
#             # Set light
#
#
#             time.sleep(5)
#

app = FastAPI()

app.include_router(v1, prefix='/api')


@app.get('/', response_model=HealthApiModel)
async def root():
    return HealthApiModel(healthy=True)


# if __name__ == '__main__':
#     t = BackgroundTasks()
#     t.start()
#     uvicorn.run(app)
