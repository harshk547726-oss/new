(() => {
  const toggle = document.getElementById('themeToggle');
  const root = document.documentElement;
  if (toggle) {
    const applyTheme = (theme) => {
      root.setAttribute('data-bs-theme', theme);
      localStorage.setItem('theme', theme);
      toggle.textContent = theme === 'dark' ? '☀️' : '🌙';
    };
    applyTheme(localStorage.getItem('theme') || 'light');
    toggle.addEventListener('click', () => applyTheme(root.getAttribute('data-bs-theme') === 'dark' ? 'light' : 'dark'));
  }

  window.renderTrendChart = (labels, values) => {
    const ctx = document.getElementById('trendChart');
    if (!ctx) return;
    new Chart(ctx, {
      type: 'bar',
      data: { labels, datasets: [{ label: 'Predictions', data: values, borderWidth: 1 }] },
      options: { responsive: true, plugins: { legend: { display: false } } }
    });
  };
})();
