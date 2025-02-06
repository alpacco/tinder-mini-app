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

// Массив для хранения зарегистрированных пользователей
let registeredUsers = [];

// Главная страница
app.get('/', (req, res) => {
    if (users.length === 0) {
        return res.send('<h1>No more users to show</h1>');
    }
    res.render('index', { users });
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

// Маршрут для регистрации пользователя
app.post('/register', bodyParser.json(), (req, res) => {
    const { telegramId, name, gender } = req.body;
    console.log(`User registered: ${name}, Gender: ${gender}`);

    // Добавляем пользователя в массив
    registeredUsers.push({ telegramId, name, gender });

    // Отправляем успешный ответ
    res.sendStatus(200);
});

// Запуск сервера на хосте 0.0.0.0 и указанном порте
app.listen(port, '0.0.0.0', () => {
    console.log(`Server running on http://0.0.0.0:${port}`);
});