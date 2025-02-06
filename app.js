const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = process.env.PORT || 3000; // Используйте PORT из окружения или 3000 по умолчанию

// Поддержка статических файлов
app.use(express.static('public'));

// Настройка шаблонизатора EJS
app.set('view engine', 'ejs');

// Массив пользователей
const users = [
    { id: 1, name: 'John Doe', photo: 'https://example.com/photo1.jpg' },
    { id: 2, name: 'Jane Smith', photo: 'https://example.com/photo2.jpg' },
    { id: 3, name: 'Alice Johnson', photo: 'https://example.com/photo3.jpg' }
];

// Главная страница
app.get('/', (req, res) => {
    res.render('index', { users: [] }); // Передайте данные пользователей, если нужно
});

// Запуск сервера
app.listen(port, '0.0.0.0', () => { // Укажите явно хост '0.0.0.0'
    console.log(`Server running on http://0.0.0.0:${port}`);
});