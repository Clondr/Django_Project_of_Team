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
        // remove stray text nodes inside the button to avoid visible labels
        Array.from(btn.childNodes).forEach(n=>{ if(n.nodeType===3) n.textContent=''; });
        // toggle class; icons visibility handled by CSS (.theme-sun / .theme-moon)
        if(isDark) btn.classList.add('is-dark'); else btn.classList.remove('is-dark');
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
    // sanitize theme button text nodes first to avoid flicker
    try{
        if (btn) Array.from(btn.childNodes).forEach(n=>{ if(n.nodeType===3) n.textContent=''; });
    }catch(e){}
    applyTheme(getStoredTheme());

    if (btn) {
        btn.addEventListener('click', () => {
            const nextTheme = body.classList.contains('dark-theme') ? 'light' : 'dark';
            applyTheme(nextTheme);
        });
    }
    // mobile toggle inside collapse
    const mobileToggle = document.getElementById('theme-toggle-mobile');
    if (mobileToggle) {
        mobileToggle.addEventListener('click', (e) => {
            e.preventDefault();
            const nextTheme = body.classList.contains('dark-theme') ? 'light' : 'dark';
            applyTheme(nextTheme);
        });
    }
    // initialize bootstrap tooltips for icon-only nav
    try{
      const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
      tooltipTriggerList.map(function (el) { return new bootstrap.Tooltip(el); });
    }catch(e){console.warn('Tooltips init failed',e)}
});
// small helper: hide elements with data-allowed-roles attribute if current user role not allowed
document.addEventListener('DOMContentLoaded', ()=>{
    const role = document.body.getAttribute('data-user-role') || null;
    document.querySelectorAll('[data-allowed-roles]').forEach(el=>{
        try{
            const allowed = el.getAttribute('data-allowed-roles').split(',').map(s=>s.trim());
            if(!role || !allowed.includes(role)) el.style.display='none';
        }catch(e){}
    });
});

// Collapse long event lists inside calendar cells and add a "+N" toggler
document.addEventListener('DOMContentLoaded', ()=>{
    const maxVisible = 3;
    document.querySelectorAll('.events-list').forEach(list => {
        const events = Array.from(list.querySelectorAll('.gc-event'));
        if (events.length > maxVisible) {
            const hidden = events.slice(maxVisible);
            hidden.forEach(el => el.style.display = 'none');
            const moreBtn = document.createElement('a');
            moreBtn.href = '#';
            moreBtn.className = 'small fst-italic';
            moreBtn.textContent = `+${hidden.length} more`;
            moreBtn.style.display = 'inline-block';
            moreBtn.style.marginTop = '6px';
            moreBtn.addEventListener('click', (e) => {
                e.preventDefault();
                const currentlyHidden = hidden[0].style.display === 'none';
                hidden.forEach(el => el.style.display = currentlyHidden ? '' : 'none');
                moreBtn.textContent = currentlyHidden ? 'show less' : `+${hidden.length} more`;
            });
            list.appendChild(moreBtn);
        }
    });
});