from observer_manager import ObserverManager

from events.kafka_event import *
from events.event import *

import os

# put the value in a k8s manifest
kafka_bootstrap_server: str | None = os.environ.get('KAFKA_BOOTSTRAP_SERVER')

if kafka_bootstrap_server is None:
    print(f'Environment variable KAFKA_BOOTSTRAP_SERVER is not set')
    exit(1)

event_queue = Queue()

# share the queue with a reader
reader = KafkaEventReader(
    KafkaConsumer(
        'om',
        bootstrap_servers=kafka_bootstrap_server,
        auto_offset_reset='latest',
    ),
    event_queue
)

# writers to other microservices
writers = {
    'mc': KafkaEventWriter(
        KafkaProducer(
            bootstrap_servers=kafka_bootstrap_server
        ),
        'mc'
    ),
    'ta': KafkaEventWriter(
        KafkaProducer(
            bootstrap_servers=kafka_bootstrap_server
        ),
        'ta'
    ),
    'dmm': KafkaEventWriter(
        KafkaProducer(
            bootstrap_servers=kafka_bootstrap_server
        ),
        'dmm'
    ),
}

# init the microservice
observer_manager = ObserverManager(
    event_queue, writers
)

observer_manager.main_thread.join()