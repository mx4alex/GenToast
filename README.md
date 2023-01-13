# GenToast
Проект по созданию телеграмм бота, генерирующего праздничные тосты, был выполнен студентом Русаковым А.В. в рамках курса ООП.
## Архитектура проекта
<img width="1508" alt="Снимок экрана 2023-01-11 190332" src="https://user-images.githubusercontent.com/90920531/212315251-4cf61871-4b7a-4987-b1fb-d74475f4c864.png">

Для создания телеграмм бота использовалась библиотека aiogram, поскольку она поддерживает написание асинхронных функций, позволяющих не ждать выполнение поступающих запросов и продолжать работу программы. Чтобы принимать от пользователя название праздника, была применена машина состояний, объектно-ориентированной реализацией которой является поведенческий паттерн проектирования State (состояние). Для хранения состояний пользователя была подключена база данных MongoDB, основным преимуществом которой является масштабируемость.

Для общения между телеграмм ботом и обученной модели использовался брокер сообщений RabbitMQ. Его преимуществом является удобный пользовательский интерфейс управления, поддержка асинхронного протокола AMQP, гибкая маршрутизация и хранение сообщения до тех пор, пока принимающее приложение не подключится и не получит его из очереди.

Также для удобства и практичности реализована передача сообщений в формате JSON через брокер сообщений.

Таким образом:
- [bot](./bot) - реализация Telegram Bot
- [generation](./generation) - реализация RuGPT-3 (генерация праздничного тоста)
- [train_model](./train_model) - подготовка датасета и дообучение модели

### Запуск проекта 
Для сборки и запуска использовался `docker-compose`, который позволяет одновременно запускать контейнеры микросервисов приложения и маршрутизировать потоки данных между ними. Для связывания контейнеров была использована сеть `docker_network` с сетевым драйвером `bridge` (так как необходимо было связать контейнеры на одном хосте Docker без изоляции друг от друга). Конечно, по умолчанию контейнеры и так были бы в единой сети с драйвером bridge, но определение собственной сети добавляет наглядность и возможность дальнейшего создания более сложной микросервисной архитектуры. Чтобы программа `gen_toast.py` получила доступ к дообученной модели, необходимо перед сборкой проекта положить модель в папку `generation`, из которой с помощью `Dockerfile` она скопируется в docker-хранилище. Также во избежание неприятностей при публичном доступе к токену телеграмм бота был создан файл `.env` с токеном бота. Таким образом, создав окружение, получаем полностью упакованный проект.

1. `docker-compose build` - сборка проекта
2. `docker-compose up` - запуск проекта

## Демонстрация работы
![ezgif com-gif-maker](https://user-images.githubusercontent.com/90920531/212316787-c2c86c87-a6ba-4eb1-88bf-d92d4e2130b1.gif)
 
