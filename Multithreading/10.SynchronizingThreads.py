import logging
import threading
import time

# Agregar el buffer finito (10 elementos)
# Agregar condición de parada del productor
# Agregar condición de consumo
# Agregar producción y el consumo (manipulación de buffer)
buffer = []
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s (%(threadName)-2s) %(message)s',
                    )


def consumer(mutex):
    global buffer

    """wait for the condition and use the resource"""
    logging.debug('Iniciando hilo consumidor')
    # t = threading.currentThread()
    while 1:
        with mutex:
            logging.debug('Esperando recurso')
            mutex.wait()
            print(buffer)
            buffer.remove("producto")
            logging.debug("removí un recurso")

        time.sleep(1)


def producer(mutex, maxProduccion):
    global buffer
    """set up the resource to be used by the consumer"""
    logging.debug('Iniciando el hilo productor')
    while 1:
        with maxProduccion:
            if len(buffer) < 10:
                maxProduccion.notify()
                logging.debug("empiecen a producir")
                with mutex:
                    logging.debug("produciendo")
                    buffer.append("producto")
                    logging.debug('Poniendo los recursos disponibles')
                    mutex.notifyAll()
            else:
                logging.debug("deteniendo producción")
                maxProduccion.wait()
        time.sleep(1)


mutex = threading.Condition()
conditionProduccionMax = threading.Condition()
c1 = threading.Thread(name='c1', target=consumer, args=(mutex,))
c2 = threading.Thread(name='c2', target=consumer, args=(mutex,))
p = threading.Thread(name='p', target=producer, args=(mutex, conditionProduccionMax))
p2 = threading.Thread(name='p2', target=producer, args=(mutex, conditionProduccionMax))
c1.start()
#time.sleep(2)
c2.start()
#time.sleep(2)
p.start()
p2.start()
