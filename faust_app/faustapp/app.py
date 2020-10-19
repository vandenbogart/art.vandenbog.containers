import os
import faust



app = faust.App(
    'user-service-app',
    version=1,
    autodiscover=True,
    origin='faustapp',
    broker=os.environ["KAFKA_BOOTSTRAP_SERVER"]
)

def main() -> None:
    app.main()
