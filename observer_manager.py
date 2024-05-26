from typing import Dict

from threading import Thread
from threading import Timer

from events.event import *
from events.kafka_event import *

from trend_data.trend_data import TrendData
from scale_data.scale_data import ScaleData

from microservice.microservice import Microservice

class ObserverManager(Microservice):
    '''
    Класс отвечающий за представление Observer manager
    Его задача -- отправлять запрос на проведение анализа, пересылать полученные данные Desicion module, отправлять запрос на сбор метрик
    '''
    TIMER_SEND_METRIC_COLLECT_EVENT = 300.0
    TIMER_SEND_ANALYSE_TREND_EVENT = 60.0

    def __init__(self, event_queue: Queue, writers: Dict[str, KafkaEventWriter]):
        '''
        Инициализация класса:
         - `self.timer1 - таймер для отправки ивента на сбор метрик`
         - `self.timer2 - таймер для отправки ивента на проведение анализа`
        '''
        self.timer1 = None
        self.timer2 = None
        return super().__init__(event_queue, writers)


    def start_timer(self):
        '''
        Запуск таймера для отправки ивентов
        '''
        self.timer1 = Timer(self.TIMER_SEND_METRIC_COLLECT_EVENT, self.send_get_metrics_event)
        self.timer1.start()
        
    def send_get_metrics_event(self):
        '''
        Отправка ивента на сбор метрик
        '''
        self.writers['mtrc'].send_event(Event(EventType.GetMetrics))
        self.timer1 = None
        self.timer2 = Timer(self.TIMER_SEND_ANALYSE_TREND_EVENT, self.send_analyse_trend_event)
        self.timer2.start()

    def send_analyse_trend_event(self):
        '''
        Отправка ивента на проведение анализа
        '''
        self.writers['trda'].send_event(Event(EventType.AnalyseTrend))
        self.timer2=None
        self.start_timer

    def handle_event(self, event: Event):
        '''
        Обработка ивентов
        '''
        target_function = None

        match event.type:
            case EventType.TrendData:
                target_function = self.handle_event_trend_data
            case _:
                pass

        if target_function is not None:
            Thread(target=target_function, args=(event.data,)).start()

    def handle_event_trend_data(self, scale_data: ScaleData):
        # send trend data to DM Manager
        self.writers['dmm'].send_event(Event(EventType.TrendData, scale_data))
