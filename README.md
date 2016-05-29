collect_articles.py - создание корпуса статей. Принимает на вход массив с url страниц авторов. Создает папку для каждого автора, в которую сохраняет статьи этого автора.

tweets_downloader.py - создание корпуса твитов. Принимает на вход имя пользователся твиттера, создает csv-файл, в который записывает ID твита, время написания и текст (отсеивает ретвиты и реплаи, включает ограничение на количество твитов).

collect_data.py - сбор признаков из новостных статей. Принимает на вход директории с файлами, возвращает два csv-файла - один со значениями признаков обучающих текстов, другой - тестовых.

SVM.py - классификация методом SVM. Принимает на вход два csv-файла (с данными обучающих и тестовых текстов). Строит модель SVM, считает долю правильно расклассифицированных объектов.
