const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = process.env.PORT || 3000;

// Middleware для установки заголовков
app.use((req, res, next) => {
    res.setHeader('Content-Type', 'text/html; charset=UTF-8');
    res.setHeader('Cache-Control', 'no-store, no-cache, must-revalidate, proxy-revalidate');
    res.setHeader('Pragma', 'no-cache');
    res.setHeader('Expires', '0');
    next();
});

app.use(bodyParser.json());
app.use(express.static('public'));

app.set('view engine', 'ejs');


// Данные о пользователях
const users = [
    { id: 1, name: 'John', photo: 'https://randomuser.me/api/portraits/men/1.jpg' },
    { id: 2, name: 'Jane', photo: 'https://randomuser.me/api/portraits/women/1.jpg' },
    { id: 3, name: 'Alex', photo: 'https://randomuser.me/api/portraits/men/2.jpg' },
    { id: 4, name: 'Anna', photo: 'https://randomuser.me/api/portraits/women/2.jpg' },
];

let currentIndex = 0; // Текущий индекс пользователя

// Главная страница
app.get('/', (req, res) => {
    if (currentIndex < users.length) {
        res.render('index', { user: users[currentIndex] });
    } else {
        res.render('index', { user: null }); // Если пользователи закончились
    }
});

// API для получения следующего пользователя
app.post('/next-user', (req, res) => {
    currentIndex++;
    if (currentIndex < users.length) {
        res.json(users[currentIndex]);
    } else {
        res.json(null); // Если пользователи закончились
    }
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});