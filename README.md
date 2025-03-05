# Telegramm Bot API Kinopoisk
Телеграмм-бот для работы с API кинопоиска <https://kinopoisk.dev/>

***

## Установка (Windows)

1. Клонирование репозитория  
```console 
  git clone https://github.com/danil-baybakov/TelegrammBotApiKinopoisk.git
```
2. Создание виртуального окружения и установка зависимостей:  
    * перейти в папку проекта  
    ```console
        cd ./TelegrammBotApiKinopoisk
    ``` 
    * создание виртуального окружения  
    ```console
        python -m venv .venv
    ``` 
    * активация виртуального окружения  
    ```console
        .\.venv\Scripts\activate.bat
    ``` 
    * установка зависимостей 
    ```console
        pip install -r requirements.txt
    ``` 
3. Зарегистрировать Телеграмм-бота через BotFather:
    * зарегистрировать Телеграмм-бота и получить токен в соответствии с инструкцией  
      <https://botcreators.ru/blog/botfather-instrukciya/?ysclid=m7vodl5ii4294938908>
    * в файл настроек окружения проекта `.env` в переменную окружения `TG_API_TOKEN` записать  
      значение полученного токена
4. Получить токен авторизации для работы с API <https://kinopoisk.dev/>:
    * получить токен в соответствии с инструкцией  
      <https://api.kinopoisk.dev/documentation>
    * в файл настроек окружения проекта `.env` в переменную окружения `SITE_API_KEY` записать  
      значение полученного токена
5. Запустить приложение:
    * перейти в папку проекта  
    ```console
        cd ./TelegrammBotApiKinopoisk
    ``` 
    * запуск приложения 
    ```console
        python ./main.py
    ``` 
   

   
   
