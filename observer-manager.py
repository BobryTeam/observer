class ObserverManager:
    '''
    Класс, отвечающий за создание информации о тренде и ее передачу в Decision Module
    '''

    def __init__(kafka_config: KafkaConfig):
        '''
        Инициализация класса
        '''
        pass

    def get_event(self):
        '''
        Считывание сообщений с кафки
        '''
        pass

    def process_collect_metrics_response(self):
        '''
        (Вызывается внутри get_event()) Обработка ответа от Metrics Collector
        '''
        pass

    def process_analyse_trend_data_response(self):
        '''
        (Вызывается внутри get_event()) Обработка ответа от Analyse Module
        '''
        pass

    def send_request_to_collect_metrics(self):
        '''
        Отправление запроса на считывание метрик в Metrics Collector
        '''
        pass

    def send_requset_to_analyse_trend_data(self):
        '''
        Отправление запроса на анализ тренда в Analyse Module
        '''
        pass