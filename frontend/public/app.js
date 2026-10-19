document.addEventListener('DOMContentLoaded', () => {
  const getBackendUrl = () => {
    if (window.BACKEND_URL && window.BACKEND_URL.trim() !== '') {
      return window.BACKEND_URL.replace(/\/+$/, '');
    }
    return 'http://127.0.0.1:8000';
  };

  const fortuneBtn = document.getElementById('fortuneBtn');
  const dictBtn = document.getElementById('dictBtn');
  const resultCard = document.getElementById('resultCard');
  const resultContent = document.getElementById('resultContent');

  const showResult = (html) => {
    resultContent.innerHTML = html;
    resultCard.classList.remove('hidden');
  };

  const showError = (msg) => {
    showResult(`<p class="error-message">Error: ${msg}</p>`);
  };

  fortuneBtn.addEventListener('click', async () => {
    const backendUrl = getBackendUrl();
    try {
      showResult('<p>Loading fortune...</p>');
      const res = await fetch(`${backendUrl}/fortune/random`);
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      }
      const data = await res.json();
      showResult(`<p>${escapeHtml(data.fortune)}</p>`);
    } catch (err) {
      showError(err.message);
    }
  });

  dictBtn.addEventListener('click', async () => {
    const backendUrl = getBackendUrl();
    try {
      showResult('<p>Loading dictionary quote...</p>');
      const res = await fetch(`${backendUrl}/dict/random`);
      if (!res.ok) {
        throw new Error(`HTTP ${res.status}: ${res.statusText}`);
      }
      const data = await res.json();
      const content = `
        <div class="lemma-title">${escapeHtml(data.lemma || '')}</div>
        <p>${escapeHtml(data.definition || '')}</p>
      `;
      showResult(content);
    } catch (err) {
      showError(err.message);
    }
  });

  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
});
