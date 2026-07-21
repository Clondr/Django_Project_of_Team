const btn = document.getElementById('theme-toggle');
const body = document.body;
const root = document.documentElement;

function applyTheme(theme) {
    const isDark = theme === 'dark';

    body.classList.remove('light-theme', 'dark-theme');
    body.classList.add(isDark ? 'dark-theme' : 'light-theme');
    root.setAttribute('data-bs-theme', isDark ? 'dark' : 'light');
    root.style.colorScheme = isDark ? 'dark' : 'light';
    localStorage.setItem('theme', theme);

    if (btn) {
        btn.textContent = isDark ? 'Увімкнути світлу тему' : 'Увімкнути темну тему';
    }
}

function getStoredTheme() {
    const storedTheme = localStorage.getItem('theme');

    if (storedTheme === 'dark' || storedTheme === 'light') {
        return storedTheme;
    }

    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
}

document.addEventListener('DOMContentLoaded', () => {
    applyTheme(getStoredTheme());

    if (btn) {
        btn.addEventListener('click', () => {
            const nextTheme = body.classList.contains('dark-theme') ? 'light' : 'dark';
            applyTheme(nextTheme);
        });
    }
});