Для локального тестирования функционала проекта необходимо выполнить команду: 
git clone https://git.miem.hse.ru/400/production/people_video_count.git 
а затем запустить приложение в контейнере:
docker build -t people_count .
docker run -d -p 5000:5000 people_count

templates - папка с html шаблонами страниц
static - содержит стиль интерфейса, а также директории для сохранения видео и результатов работы модели
app.py - конфигурация web приложения
main.py - файл с эндпоинтами для корректного работы web сервиса
utils.py - вспомогательные функции и функции для инференса модели
![Uploading demonstration.gif…]()
