document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('predictionForm');
  const searchInput = document.getElementById('symptomSearch');

  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      const value = e.target.value.toLowerCase();
      document.querySelectorAll('.symptom-item').forEach((item) => {
        item.style.display = item.textContent.toLowerCase().includes(value) ? '' : 'none';
      });
    });
  }

  if (form) {
    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      const symptoms = {};
      form.querySelectorAll('input[type="checkbox"]').forEach((box) => { symptoms[box.name] = box.checked ? 1 : 0; });

      const response = await fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ symptoms }),
      });

      if (!response.ok) {
        alert('Prediction failed. Please retry.');
        return;
      }

      const result = await response.json();
      window.location.href = `/result/${result.record_id}`;
    });
  }
});
