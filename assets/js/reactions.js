/**
 * Article reactions — GitHub Pages compatible
 *
 * Without backend (default):
 *   Saves your vote in localStorage (per browser). No global counts.
 *
 * With Supabase (optional global counts):
 *   Copy reactions-config.example.js → reactions-config.js
 *   Fill in URL + anon key. See internal/README for setup.
 */
(() => {
  const STORAGE_KEY = "techblog:reactions";

  const loadConfig = () => {
    if (window.REACTIONS_CONFIG?.enabled) return window.REACTIONS_CONFIG;
    return null;
  };

  const readLocal = () => {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    } catch {
      return {};
    }
  };

  const writeLocal = (data) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  };

  const formatCounts = (counts) => {
    const like = counts.like || 0;
    const dislike = counts.dislike || 0;
    const love = counts.love || 0;
    return { like, dislike, love };
  };

  async function fetchSupabaseCounts(config, articleId) {
    const url = `${config.url}/rest/v1/article_reactions?article_id=eq.${encodeURIComponent(articleId)}&select=like_count,dislike_count,love_count`;
    const res = await fetch(url, {
      headers: {
        apikey: config.anonKey,
        Authorization: `Bearer ${config.anonKey}`,
      },
    });
    if (!res.ok) return null;
    const rows = await res.json();
    if (!rows.length) return { like: 0, dislike: 0, love: 0 };
    return formatCounts({
      like: rows[0].like_count,
      dislike: rows[0].dislike_count,
      love: rows[0].love_count,
    });
  }

  async function submitSupabase(config, articleId, reaction) {
    const res = await fetch(`${config.url}/rest/v1/rpc/vote_article`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        apikey: config.anonKey,
        Authorization: `Bearer ${config.anonKey}`,
      },
      body: JSON.stringify({ p_article_id: articleId, p_reaction: reaction }),
    });
    return res.ok;
  }

  function updateUI(bar, counts, userVote) {
    bar.querySelectorAll("[data-reaction]").forEach((btn) => {
      const type = btn.dataset.reaction;
      const countEl = btn.querySelector(".reaction-count");
      if (countEl && counts) countEl.textContent = counts[type] ?? 0;
      btn.classList.toggle("is-active", userVote === type);
      btn.setAttribute("aria-pressed", userVote === type ? "true" : "false");
    });

    const note = bar.querySelector(".reactions-note");
    if (note) {
      if (userVote) {
        note.textContent = loadConfig()
          ? "Thanks — your vote is counted."
          : "Thanks — saved on this device.";
      } else {
        note.textContent = loadConfig()
          ? "Was this helpful?"
          : "Was this helpful? (saved locally on this device)";
      }
    }
  }

  async function initBar(bar) {
    const articleId = bar.dataset.articleId;
    if (!articleId) return;

    const config = loadConfig();
    const local = readLocal();
    const userVote = local[articleId] || null;

    let counts = { like: 0, dislike: 0, love: 0 };
    if (config) {
      const remote = await fetchSupabaseCounts(config, articleId);
      if (remote) counts = remote;
    }

    updateUI(bar, counts, userVote);

    bar.addEventListener("click", async (e) => {
      const btn = e.target.closest("[data-reaction]");
      if (!btn || btn.disabled) return;

      const reaction = btn.dataset.reaction;
      if (!["like", "dislike", "love"].includes(reaction)) return;

      const prev = local[articleId];
      if (prev === reaction) return;

      local[articleId] = reaction;
      writeLocal(local);

      if (config) {
        bar.classList.add("is-loading");
        const ok = await submitSupabase(config, articleId, reaction);
        bar.classList.remove("is-loading");
        if (ok) {
          const remote = await fetchSupabaseCounts(config, articleId);
          if (remote) counts = remote;
        }
      } else {
        // Local-only optimistic bump (visible only to this user)
        if (prev && counts[prev] > 0) counts[prev] -= 1;
        counts[reaction] = (counts[reaction] || 0) + 1;
      }

      updateUI(bar, counts, reaction);
    });
  }

  document.querySelectorAll("[data-reactions]").forEach(initBar);
})();
