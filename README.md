#VTS

Бот который читает сообщения в обсуждении группы VK и пересылает новые в Slack.

##Зависимости
1. VK API

`pip install vk`

2. Slack API

`pip install slacker`


##Настройки бота
1. Скопируйте файл **settings.example.py** и переименуте в **settings.py**.
2. Внесите необходимые изменения в файле **settings.py**.

**ВНИМАНИЕ!** не публикуйте этот файл, а также файл **vk_config.json**, примите меры для недоступности данного файла посторонним.

##Запуск бота как сервиса (Debian 6 stable и выше)
1. Скопируйте файл **vts.example.sh** в директорию **/etc/init.d/** с именем **vts.sh**.

`sudo cp vts.example.sh /etc/init.d/vts.sh`

2. В файле **vts.sh** строке `cd /path/to/vts` замените `/path/to/vts` на путь к файлу **vts.py**
3. Установите права на исполнение для скрипта **vts.sh**

`sudo chmod +x /etc/init.d/vts.sh`

4. Установите сервис

`sudo insserv -v -f /etc/init.d/vts.sh`

5. Запустите сервис

`sudo service vts.sh start`

Либо, запустите скрипт **install_service.sh**

##Удаление бота из автозагрузки (Debian 6 stable и выше)
1. Удалите сервис **vts.sh**

`sudo insserv -v -r /etc/init.d/vts.sh`

2. Удалите скрипт **vts.sh** из директории **/etc/init.d**

`sudo rm /etc/init.d/vts.sh`