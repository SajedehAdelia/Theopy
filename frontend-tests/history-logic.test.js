const test = require("node:test");
const assert = require("node:assert/strict");

const {
  matchesHistorySearch,
  selectHistoryEntries,
} = require("../src/static/js/history-logic.js");

// --- matchesHistorySearch -------------------------------------------------

test("matchesHistorySearch: matches when the query is in the question", () => {
  const entry = { question: "reminders for Pharmacie de la Gare?", summary: "Reminders List: ..." };
  assert.equal(matchesHistorySearch(entry, "gare"), true);
});

test("matchesHistorySearch: matches when the query is in the summary", () => {
  const entry = { question: "show invoices", summary: "Pharmacie de la Gare, 150.00 unpaid" };
  assert.equal(matchesHistorySearch(entry, "150.00"), true);
});

test("matchesHistorySearch: is case-insensitive", () => {
  const entry = { question: "Marcel Dumont's company?", summary: "Pharmacie de la Gare" };
  assert.equal(matchesHistorySearch(entry, "marcel dumont"), true);
});

test("matchesHistorySearch: returns false when nothing matches", () => {
  const entry = { question: "show sessions", summary: "Sessions List: ..." };
  assert.equal(matchesHistorySearch(entry, "invoice"), false);
});

test("matchesHistorySearch: tolerates a missing/null question (old entries)", () => {
  const entry = { question: null, summary: "No invoices found for this criteria." };
  assert.equal(matchesHistorySearch(entry, "invoices"), true);
  assert.equal(matchesHistorySearch(entry, "reminder"), false);
});

// --- selectHistoryEntries --------------------------------------------------

const SAMPLE_HISTORY = {
  Factures: [
    { id: 1, domain: "Factures", question: "invoices for Gare", summary: "Invoice 100", timestamp: 300 },
    { id: 2, domain: "Factures", question: "invoices for Soleil", summary: "Invoice 101", timestamp: 100 },
  ],
  Relances: [
    { id: 3, domain: "Relances", question: "reminders for Gare", summary: "Reminder 100", timestamp: 200 },
  ],
};

test("selectHistoryEntries: with no query, returns only the active domain's entries", () => {
  const result = selectHistoryEntries(SAMPLE_HISTORY, "Factures", "");
  assert.deepEqual(
    result.map((entry) => entry.id),
    [1, 2]
  );
});

test("selectHistoryEntries: with no query, an empty/unknown domain returns an empty array", () => {
  const result = selectHistoryEntries(SAMPLE_HISTORY, "Plannings", "");
  assert.deepEqual(result, []);
});

test("selectHistoryEntries: a whitespace-only query is treated as no query", () => {
  const result = selectHistoryEntries(SAMPLE_HISTORY, "Relances", "   ");
  assert.deepEqual(
    result.map((entry) => entry.id),
    [3]
  );
});

test("selectHistoryEntries: with a query, searches across every domain, not just the active one", () => {
  const result = selectHistoryEntries(SAMPLE_HISTORY, "Factures", "gare");
  assert.deepEqual(
    result.map((entry) => entry.id).sort(),
    [1, 3]
  );
});

test("selectHistoryEntries: with a query, results are sorted most-recent-first", () => {
  // Matches for "gare": id 1 (timestamp 300) and id 3 (timestamp 200).
  // Highest timestamp = most recent = should come first.
  const result = selectHistoryEntries(SAMPLE_HISTORY, "Factures", "gare");
  assert.deepEqual(
    result.map((entry) => entry.id),
    [1, 3]
  );
});

test("selectHistoryEntries: with a query that matches nothing, returns an empty array", () => {
  const result = selectHistoryEntries(SAMPLE_HISTORY, "Factures", "nonexistent");
  assert.deepEqual(result, []);
});
