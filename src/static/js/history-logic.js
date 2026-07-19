// Pure, DOM-free logic for the 24h history sidebar (tabs + search bar).
// Kept separate from the inline <script> in theopy-chat.html.jinja2 so it can
// be loaded in the browser (as a plain <script> tag) AND required directly in
// Node for automated tests (see /frontend-tests) - no DOM dependency, no
// framework, no build step needed either way.

function matchesHistorySearch(entry, query) {
  const haystack = ((entry.question || "") + " " + (entry.summary || "")).toLowerCase();
  return haystack.includes(query);
}

function selectHistoryEntries(historyByDomain, activeDomain, searchQuery) {
  const query = (searchQuery || "").trim().toLowerCase();

  if (!query) {
    return historyByDomain[activeDomain] || [];
  }

  // Searching spans every domain at once - you usually don't remember which
  // tab a past search landed under.
  return Object.values(historyByDomain)
    .flat()
    .filter((entry) => matchesHistorySearch(entry, query))
    .sort((a, b) => b.timestamp - a.timestamp);
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = { matchesHistorySearch, selectHistoryEntries };
}
