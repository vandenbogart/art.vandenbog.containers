'''Faust application definition'''
import os
import faust


app = faust.App(
    'vandenbogart-faust',
    version=1,
    autodiscover=True,
    origin='faustapp',
    broker=os.environ["KAFKA_BOOTSTRAP_SERVER"],
    store='rocksdb://'
)

def main() -> None:
    "Wrapper for app.main"
    app.main()
