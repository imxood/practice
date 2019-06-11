import dramatiq
import requests
import sys
from dramatiq.brokers.redis import RedisBroker

broker = RedisBroker()

dramatiq.set_broker(broker)

@dramatiq.actor
def count_words(url):
    pass

if __name__ == '__main__':
    count_words.send(sys.argv[1])
