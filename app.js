const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = process.env.PORT || 3000;

// Поддержка статических файлов
app.use(express.static('public'));

// Настройка шаблонизатора EJS
app.set('view engine', 'ejs');

// Главная страница
app.get('/', (req, res) => {
    res.render('index', { users: [] }); // Передайте данные пользователей, если нужно
});

// Запуск сервера
app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});