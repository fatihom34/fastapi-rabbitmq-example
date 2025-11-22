# Event Sync Engine

RabbitMQ ile mesajlaşma yapan basit bir FastAPI uygulaması.

## Endpoints

### `GET /health`
Uygulama sağlık kontrolü.

### `POST /post-event`
RabbitMQ'ya mesaj gönderir.
- **Body:** `{ "message": "string", "event_type": "string", "timestamp": "datetime" }`
- **Queue:** `event_queue`

### `GET /events?max_messages=10`
Queue'daki mesajları okur ve okduktan sonra queue'dan siler.
- **Query Param:** `max_messages` (default: 10)

### `GET /queue-info`
Queue bilgilerini döner (mesaj sayısı, consumer sayısı).

## Kullanım

1. RabbitMQ'yu başlat: `docker-compose up -d rabbitmq-example`
2. Uygulamayı çalıştır: `uvicorn app.main:app --reload`
3. RabbitMQ Management UI: http://localhost:15672 (guest/guest)