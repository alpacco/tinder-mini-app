function initMiniApp() {
    if (window.Telegram) {
        const tg = window.Telegram.WebApp;
        tg.ready();

        // Ваш код приложения
    } else {
        console.error('Telegram Mini App не обнаружен');
    }
}

document.addEventListener('DOMContentLoaded', initMiniApp);