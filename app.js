const express = require('express');
const bodyParser = require('body-parser');

// Создаем экземпляр Express-приложения
const app = express();

// Устанавливаем порт (берем из переменной окружения или используем 3000 по умолчанию)
const port = process.env.PORT || 3000;

// Поддержка статических файлов (например, CSS)
app.use(express.static('public'));

// Настройка шаблонизатора EJS
app.set('view engine', 'ejs');

// Массив пользователей с рандомными фотографиями
let users = [
    { id: 1, name: 'John Doe', photo: 'https://picsum.photos/id/1025/300/400' },
    { id: 2, name: 'Jane Smith', photo: 'https://picsum.photos/id/1026/300/400' },
    { id: 3, name: 'Alice Johnson', photo: 'https://picsum.photos/id/1027/300/400' }
];

// Главная страница
app.get('/', (req, res) => {
    if (users.length === 0) {
        // Если пользователи закончились, отправляем сообщение
        return res.send('<h1>No more users to show</h1>');
    }
    // Отправляем массив пользователей в шаблон index.ejs
    res.render('index', { users });
});

// Маршрут для получения данных пользователя из Telegram
app.post('/auth', bodyParser.json(), (req, res) => {
    const userData = req.body;
    console.log('User authenticated:', userData);

    // Здесь можно сохранить данные пользователя в базу данных или сессию
    res.sendStatus(200);
});

// Маршрут для лайка
app.post('/like', bodyParser.json(), (req, res) => {
    const userId = req.body.userId;
    console.log(`User ${userId} liked`);
    users.shift(); // Удаляем первого пользователя из массива
    res.sendStatus(200);
});

// Маршрут для дизлайка
app.post('/dislike', bodyParser.json(), (req, res) => {
    const userId = req.body.userId;
    console.log(`User ${userId} disliked`);
    users.shift(); // Удаляем первого пользователя из массива
    res.sendStatus(200);
});

// Запуск сервера на хосте 0.0.0.0 и указанном порте
app.listen(port, '0.0.0.0', () => {
    console.log(`Server running on http://0.0.0.0:${port}`);
});