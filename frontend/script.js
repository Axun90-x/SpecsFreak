const form = document.getElementById("recommend-form");
const promptInput = document.getElementById("prompt");
const statusBox = document.getElementById("status");
const resultsBox = document.getElementById("results");
const submitBtn = document.getElementById("submit-btn");

function safeText(value) {
  if (value === null || value === undefined) return "";
  return String(value);
}

function renderResults(recommendations) {
  if (!recommendations || recommendations.length === 0) {
    resultsBox.innerHTML = "<p>No recommendations found.</p>";
    return;
  }

  resultsBox.innerHTML = recommendations
    .map((item) => {
      const title = safeText(item.game_name);
      const gameReview = item.game_review ?? item.user_score ?? "N/A";
      const metaScore = item.meta_score ?? "N/A";
      const userScore = item.user_score ?? "N/A";
      const genre = safeText(item.genre);
      const platform = safeText(item.platform);
      const type = safeText(item.type);
      const rating = safeText(item.rating);
      const url = safeText(item.url);

      return `
        <article class="result-card">
          <div class="result-top">
            <h3 class="result-title">${item.rank}. ${title}</h3>
            <span class="result-score">Game review: ${gameReview}</span>
          </div>
          <div class="meta">
            <div><strong>Genre:</strong> ${genre}</div>
            <div><strong>Platform:</strong> ${platform}</div>
            <div><strong>Type:</strong> ${type} | <strong>Rating:</strong> ${rating}</div>
            <div><strong>Meta/User:</strong> ${metaScore} / ${userScore}</div>
          </div>
          ${
            url
              ? `<a class="link" href="${url}" target="_blank" rel="noreferrer">Open game page</a>`
              : ""
          }
        </article>
      `;
    })
    .join("");
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const prompt = promptInput.value.trim();
  if (!prompt) {
    statusBox.textContent = "Please describe what kind of game you want.";
    return;
  }

  submitBtn.disabled = true;
  statusBox.textContent = "Analyzing your prompt and finding matches...";
  resultsBox.innerHTML = "";

  try {
    const response = await fetch("/api/recommend", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt, top_n: 30 }),
    });

    const data = await response.json();
    if (!response.ok) {
      throw new Error(data.error || "Failed to get recommendations.");
    }

    if (data.message) {
      statusBox.textContent = data.message;
    } else {
      statusBox.textContent = `Showing ${data.count} recommendations for "${data.prompt}".`;
    }
    renderResults(data.recommendations);
  } catch (error) {
    statusBox.textContent = error.message || "Something went wrong.";
  } finally {
    submitBtn.disabled = false;
  }
});
