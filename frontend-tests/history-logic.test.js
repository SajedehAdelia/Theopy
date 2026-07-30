const test = require("node:test");
const assert = require("node:assert/strict");

const {
  matchesHistorySearch,
  selectHistoryEntries,
  formatToolResultAsMarkdownTable,
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

// --- formatToolResultAsMarkdownTable ---------------------------------------

test("formatToolResultAsMarkdownTable: multi-row invoice list with a title line", () => {
  const raw =
    "Invoices List:\n" +
    "Invoice ID: 100 | Pharmacy: Pharmacie de la Gare | Date: 2019-02-01 | Total: 276.00€ | Status: Paid\n" +
    "Invoice ID: 105 | Pharmacy: Pharmacie de la Gare | Date: 2019-03-01 | Total: 312.00€ | Status: Unpaid";

  const table = formatToolResultAsMarkdownTable(raw);

  assert.equal(
    table,
    "| Invoice ID | Pharmacy | Date | Total | Status |\n" +
      "| --- | --- | --- | --- | --- |\n" +
      "| 100 | Pharmacie de la Gare | 2019-02-01 | 276.00€ | Paid |\n" +
      "| 105 | Pharmacie de la Gare | 2019-03-01 | 312.00€ | Unpaid |"
  );
});

test("formatToolResultAsMarkdownTable: a title glued onto the first field on the same line (reminders)", () => {
  const raw =
    "Reminders List: ID: 101 | Customer: Pharmacie de la Gare | Date: 2019-03-02 | " +
    "Author: Mathieu Onésime | Status: Pending | Comment: à se souvenir une nouvelle fois";

  const table = formatToolResultAsMarkdownTable(raw);

  assert.equal(
    table,
    "| ID | Customer | Date | Author | Status | Comment |\n" +
      "| --- | --- | --- | --- | --- | --- |\n" +
      "| 101 | Pharmacie de la Gare | 2019-03-02 | Mathieu Onésime | Pending | à se souvenir une nouvelle fois |"
  );
});

test("formatToolResultAsMarkdownTable: a title with a parenthetical glued onto the first field (planning)", () => {
  const raw =
    "Customer Dashboard Summary (5/2019): Customer: Pharmacie de la Gare | Freq: | " +
    "Planned: 44h00 | Done: 11:40:23 | Charged: 16:00:00";

  const table = formatToolResultAsMarkdownTable(raw);

  assert.equal(
    table,
    "| Customer | Freq | Planned | Done | Charged |\n" +
      "| --- | --- | --- | --- | --- |\n" +
      "| Pharmacie de la Gare | — | 44h00 | 11:40:23 | 16:00:00 |"
  );
});

test("formatToolResultAsMarkdownTable: drops a trailing row truncated to fewer columns, keeps the complete one", () => {
  const raw =
    "Invoices List:\n" +
    "Invoice ID: 100 | Pharmacy: Pharmacie de la Gare | Date: 2019-02-01 | Total: 276.00€ | Status: Paid\n" +
    "Invoice ID: 105 | Pharmacy: Pharmacie de la G";

  const table = formatToolResultAsMarkdownTable(raw);

  assert.equal(
    table,
    "| Invoice ID | Pharmacy | Date | Total | Status |\n" +
      "| --- | --- | --- | --- | --- |\n" +
      "| 100 | Pharmacie de la Gare | 2019-02-01 | 276.00€ | Paid |"
  );
});

test("formatToolResultAsMarkdownTable: a plain non-tabular message returns null (no pipes at all)", () => {
  assert.equal(
    formatToolResultAsMarkdownTable("Success: Invoice 101 has been marked as Paid."),
    null
  );
  assert.equal(
    formatToolResultAsMarkdownTable("No sessions found for this criteria."),
    null
  );
});

test("formatToolResultAsMarkdownTable: null/empty input returns null", () => {
  assert.equal(formatToolResultAsMarkdownTable(null), null);
  assert.equal(formatToolResultAsMarkdownTable(""), null);
});
