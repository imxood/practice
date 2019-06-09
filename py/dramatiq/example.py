import dramatiq
import requests
import sys
from dramatiq.brokers.redis import RedisBroker

broker = RedisBroker()

dramatiq.set_broker(broker)

@dramatiq.actor
def count_words(url):
    response = requests.get(url)
    count = len(response.text.split(' '))
    print("There are {} words at {}.".format(count, url))

if __name__ == '__main__':
    count_words.send(sys.argv[1])
