
    async function shorten() {
      const longUrl = document.getElementById('longUrl').value.trim();
      if (!longUrl) {
        alert("Please enter a URL first!");
        return;
      }

      const response = await fetch("/shorten", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ long_url: longUrl })
      });

      const data = await response.json();
      const result = document.getElementById("result");

      if (response.ok) {
        result.innerHTML = `
          <span class="text-green-600 animate-pulse">✅ Shortened:</span><br>
          <a href="${data.short_url}" target="_blank" 
             class="text-blue-600 underline hover:text-blue-800 transition">
             ${data.short_url}
          </a>
        `;
      } else {
        result.innerHTML = `
          <span class="text-red-600 animate-bounce">❌ Error:</span> ${data.detail}
        `;
      }
    }

    // 🌗 Dark mode toggle logic
    const toggle = document.getElementById('darkModeToggle');
    const body = document.body;

    // Load saved theme
    if (localStorage.getItem('theme') === 'dark') {
      body.classList.add('dark-mode');
      toggle.textContent = '☀️ Light Mode';
      toggle.classList.replace('bg-blue-600', 'bg-yellow-400');
      toggle.classList.replace('hover:bg-blue-700', 'hover:bg-yellow-500');
    }

    toggle.addEventListener('click', () => {
      body.classList.toggle('dark-mode');
      const isDark = body.classList.contains('dark-mode');
      toggle.textContent = isDark ? '☀️ Light Mode' : '🌙 Dark Mode';

      if (isDark) {
        toggle.classList.replace('bg-blue-600', 'bg-yellow-400');
        toggle.classList.replace('hover:bg-blue-700', 'hover:bg-yellow-500');
      } else {
        toggle.classList.replace('bg-yellow-400', 'bg-blue-600');
        toggle.classList.replace('hover:bg-yellow-500', 'hover:bg-blue-700');
      }

      localStorage.setItem('theme', isDark ? 'dark' : 'light');
    });

    document.addEventListener("DOMContentLoaded", () => {
      document.querySelectorAll(".fade-up").forEach((el, i) => {
        el.style.opacity = 0;
        el.style.animationDelay = `${0.3 + i * 0.2}s`;
      });
    });
 