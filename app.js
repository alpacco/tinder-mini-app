// Подключение необходимых модулей
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

// Массив пользователей (для демонстрации)
let users = [
    { id: 1, name: 'John Doe', photo: 'https://example.com/photo1.jpg' },
    { id: 2, name: 'Jane Smith', photo: 'https://example.com/photo2.jpg' },
    { id: 3, name: 'Alice Johnson', photo: 'https://example.com/photo3.jpg' }
];

// Главная страница
app.get('/', (req, res) => {
    // Отправляем массив пользователей в шаблон index.ejs
    res.render('index', { users });
});

// Маршрут для обработки лайков
app.post('/like', bodyParser.json(), (req, res) => {
    const userId = req.body.userId;
    console.log(`User ${userId} liked`);
    
    // Удаляем первого пользователя из массива
    users = users.filter(user => user.id !== userId);

    // Отправляем ответ клиенту
    res.sendStatus(200);
});

// Маршрут для обработки дизлайков
app.post('/dislike', bodyParser.json(), (req, res) => {
    const userId = req.body.userId;
    console.log(`User ${userId} disliked`);
    
    // Удаляем первого пользователя из массива
    users = users.filter(user => user.id !== userId);

    // Отправляем ответ клиенту
    res.sendStatus(200);
});

// Запуск сервера на хосте 0.0.0.0 и указанном порте
app.listen(port, '0.0.0.0', () => {
    console.log(`Server running on http://0.0.0.0:${port}`);
});