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

  return Object.values(historyByDomain)
    .flat()
    .filter((entry) => matchesHistorySearch(entry, query))
    .sort((a, b) => b.timestamp - a.timestamp);
}

// Recalling an old history entry (recorded before full_answer existed, or
// any entry where attaching the LLM's Markdown answer failed) 
function extractKeyValuePairs(line) {
  const segments = line.split("|");
  const pairs = [];

  segments.forEach((segment, index) => {
    if (index === 0) {

      const parts = segment.split(":");
      if (parts.length >= 3) {
        pairs.push({
          key: parts[parts.length - 2].trim(),
          value: parts[parts.length - 1].trim(),
        });
      } else if (parts.length === 2) {
        pairs.push({ key: parts[0].trim(), value: parts[1].trim() });
      }
      return;
    }

    const colonIndex = segment.indexOf(":");
    if (colonIndex === -1) return;
    pairs.push({
      key: segment.slice(0, colonIndex).trim(),
      value: segment.slice(colonIndex + 1).trim(),
    });
  });

  return pairs;
}

function formatToolResultAsMarkdownTable(rawText) {
  if (!rawText) return null;

  const lines = rawText
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);

  const rows = lines
    .filter((line) => line.includes("|"))
    .map(extractKeyValuePairs)
    .filter((pairs) => pairs.length > 0);

  if (rows.length === 0) return null;

  const columnCount = rows[0].length;
  if (columnCount < 2) return null;

  const completeRows = rows.filter((row) => row.length === columnCount);
  if (completeRows.length === 0) return null;

  const headers = completeRows[0].map((cell) => cell.key);
  const headerRow = "| " + headers.join(" | ") + " |";
  const separatorRow = "| " + headers.map(() => "---").join(" | ") + " |";
  const bodyRows = completeRows.map(
    (row) => "| " + row.map((cell) => cell.value || "—").join(" | ") + " |"
  );

  return [headerRow, separatorRow, ...bodyRows].join("\n");
}

if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    matchesHistorySearch,
    selectHistoryEntries,
    formatToolResultAsMarkdownTable,
  };
}
