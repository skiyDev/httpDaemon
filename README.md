Простой демон-сервис основанный на aiohttp и python-daemon. 
Для запуска демона, следует использовать права суперпользователя.
<br>
По умолчанию сервис использует порт: 8081.
<br>
Для рабты с сервисом доступно следующие API:
<ol>
<li>upload - post метод с параметром name для загрузки на сервер файла по его полному имени, возвращает json с параметром FileHash</li>
<li>download(hash) - get метод с параметром hash для получения с сервера файла по его хэш-коду</li>
<li>remove - post метод с параметром hash для удаления файла с сервера</li>
</ol>
Сервис сохраняте файлы в папку /store/, а также там же ведет лог исключений.
