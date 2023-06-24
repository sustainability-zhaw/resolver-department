# Resolver Department

Publications and other sources do not always list all involved departments.
This resolver tries to complete the list of involved departments by adding the department of resolved authors to the list.

## Configuration

The following can be configured with environment variables or by providing a JSON file at `/etc/app/config.json`.
An additional JSON file is read from `/etc/app/secrets.json` that can be used for sensitive information.

*Note: Config files take precedence over environment variables.*

- `DB_HOST` - GraphQL host. Defaults to `localhost:8080`.
- `MQ_HOST` - RabbitMQ host. Defaults to `mq`.
- `MQ_EXCHANGE` - RabbitMQ exchange name. Defaults to `zhaw-km`.
- `MQ_QUEUE` - RabbitMQ queue name, Defaults to `classificationqueue`.
- `MQ_BINDKEYS` - RabbitMQ routing keys to use to bind the queue to the exchange. Defaults to `importer.person`. Multiple routing keys can be provided with comma separated string.
- `MQ_HEARTBEAT` - RabbitMQ heart beat in seconds. Defaults to `6000` (1.6h).
- `MQ_TIMEOUT` - RabbitMQ blocking timeout in seconds. Defaults to `3600` (1h).
- `LOG_LEVEL` - Log level for tracing and debugging. Defaults to `ERROR`.
