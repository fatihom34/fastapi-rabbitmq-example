from fastapi import FastAPI, Body
from app.core.config import settings
from pydantic import BaseModel
import pika
import json
from datetime import datetime

app = FastAPI(title=settings.APP_NAME)

class EventMessage(BaseModel):
    message: str
    event_type: str = "default"
    timestamp: datetime = datetime.now()

@app.get("/health")
def health():
    return {
        "status": "ok",
        "environment": settings.ENVIRONMENT
    }

def get_connection():
    return pika.BlockingConnection(pika.ConnectionParameters(host=settings.RABBITMQ_HOST))

@app.post("/post-event")
def post_event(event: EventMessage):
    """
    RabbitMQ'ya mesaj gönder
    """
    connection = get_connection()
    channel = connection.channel()
    
    # Queue'yu oluştur (yoksa)
    channel.queue_declare(queue='event_queue', durable=True)
    
    # Mesajı JSON formatında hazırla
    message_body = json.dumps({
        "message": event.message,
        "event_type": event.event_type,
        "timestamp": event.timestamp.isoformat()
    })
    
    # Mesajı publish et
    channel.basic_publish(
        exchange='',
        routing_key='event_queue',
        body=message_body,
        properties=pika.BasicProperties(
            delivery_mode=2,  # Mesajı persistent yap
        )
    )
    
    connection.close()
    
    return {
        "status": "success",
        "message": "Event published to RabbitMQ",
        "data": {
            "message": event.message,
            "event_type": event.event_type
        }
    }

@app.get("/events")
def get_queued_events(max_messages: int = 10):
    """
    Queue'daki mesajları getir (consume etmeden)
    """
    connection = get_connection()
    channel = connection.channel()
    
    # Queue'yu oluştur (yoksa)
    channel.queue_declare(queue='event_queue', durable=True)
    
    messages = []
    
    # Queue'dan mesajları al
    for _ in range(max_messages):
        method_frame, header_frame, body = channel.basic_get(queue='event_queue', auto_ack=False)
        
        if method_frame:
            try:
                message_data = json.loads(body.decode('utf-8'))
            except:
                message_data = body.decode('utf-8')
            
            messages.append({
                "delivery_tag": method_frame.delivery_tag,
                "message": message_data
            })
            
            # Mesajı acknowledge et (queue'dan sil)
            channel.basic_ack(delivery_tag=method_frame.delivery_tag)
        else:
            # Queue boş
            break
    
    connection.close()
    
    return {
        "status": "success",
        "message_count": len(messages),
        "messages": messages
    }

@app.get("/queue-info")
def get_queue_info():
    """
    Queue bilgilerini getir (mesaj sayısı, consumer sayısı vs.)
    """
    connection = get_connection()
    channel = connection.channel()
    
    # Queue'yu passive mode'da declare et (sadece bilgi al, oluşturma)
    queue = channel.queue_declare(queue='event_queue', durable=True, passive=False)
    
    connection.close()
    
    return {
        "status": "success",
        "queue_name": "event_queue",
        "message_count": queue.method.message_count,
        "consumer_count": queue.method.consumer_count
    }