## Создайте онлайн-сервис для генерации CSV-файлов с поддельными (фиктивными) данными с помощью Python и Django:

- Любой пользователь может войти в систему под своим именем пользователя и паролем.
- Вы можете использовать общие представления, предоставляемые Django для реализации этих возможностей. Достаточно зарегистрировать новых пользователей через интерфейс администратора.  Обратите внимание, что вам не нужно реализовывать интерфейс пользовательского профиля для поддержки смены пароля. 
- Любой зарегистрированный пользователь может создать любое количество схем данных для создания наборов данных с поддельными данными.
- Каждая такая схема данных имеет имя и список столбцов с именами и указанными типами данных.
- Необходимо реализовать различные типы данных (как минимум 5 различных типов):
- - Полное имя (комбинация имени и фамилии).
- - Работа
- - Email
- - Доменное имя
- - Номер телефона
- - Название компании
- - Текст (с заданным диапазоном для ряда предложений)
- - Целое (с заданным диапазоном)
- - Адрес
- - Дата
- Пользователи могут построить схему данных с любым количеством столбцов любого типа, описанного выше.  Некоторые типы поддерживают дополнительные аргументы (например, диапазон), другие нет.
- Каждый столбец также имеет свое собственное имя (которое будет заголовком столбца в CSV-файле) и порядок (просто номер для управления порядком столбцов).
- После создания схемы пользователь должен иметь возможность ввести количество записей, которые ему необходимо сгенерировать, и нажать кнопку "Сгенерировать данные".
- После нажатия кнопки система должна использовать Сельдерей, чтобы сгенерировать CSV-файл заданной структуры, соответствующие фальшивые данные и сохранить результат в файле где-нибудь в каталоге "носитель".
- Интерфейс должен показывать цветную метку состояния генерации для каждого набора данных (обработка/готовность).
- Добавьте кнопку "Download" для доступных для скачивания наборов данных.
- Завершенное приложение должно быть развернуто в Heroku и доступно в режиме онлайн (должен поддерживаться HTTPS).  Пожалуйста, создайте тестового пользователя и предоставьте нам учетные данные.
- Исходный код должен быть зафиксирован в репозитории на GitHub, Bitbucket или GitLab.

Запуск Celery на windows `celery -A Planeks worker --pool=solo -l info`