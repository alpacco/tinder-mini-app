const express = require('express');
const bodyParser = require('body-parser');

const app = express();
const port = process.env.PORT || 3000;
// В app.js добавьте массив данных
const users = [
    { id: 1, name: 'John', photo: 'https://example.com/photo1.jpg' },
    { id: 2, name: 'Jane', photo: 'https://example.com/photo2.jpg' },
    // ... добавьте больше пользователей
];

app.use(bodyParser.json());
app.use(express.static('public'));

app.set('view engine', 'ejs');

app.get('/', (req, res) => {
    res.render('index');
});

app.listen(port, () => {
    console.log(`Server running on port ${port}`);
});