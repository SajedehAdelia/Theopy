from src import history_store


def setup_function():
    """Ensure each test starts from a clean, empty history."""
    history_store.clear()


def test_record_infers_domain_from_tool_name():
    history_store.record(
        "fetch_all_invoices_list", {"customer_name": "Gare"}, "Invoices List: ..."
    )
    history_store.record(
        "fetch_planning_dashboard_customers", {}, "Customer Dashboard Summary"
    )
    history_store.record("fetch_reminders_list", {}, "Reminders List: ...")
    history_store.record("trigger_start_session", {}, "Success: Session 999 started")
    history_store.record("unknown_diagnostic_tool", {}, "Mocked response")

    grouped = history_store.get_grouped()

    assert "Factures" in grouped
    assert "Plannings" in grouped
    assert "Relances" in grouped
    assert "Sessions" in grouped
    assert "Autre" in grouped


def test_get_grouped_returns_most_recent_first():
    history_store.record("fetch_all_invoices_list", {}, "first call")
    history_store.record("fetch_all_invoices_list", {}, "second call")

    grouped = history_store.get_grouped()

    assert [entry["summary"] for entry in grouped["Factures"]] == [
        "second call",
        "first call",
    ]


def test_summary_is_truncated_to_160_chars():
    long_result = "x" * 500
    history_store.record("fetch_all_invoices_list", {}, long_result)

    grouped = history_store.get_grouped()

    assert len(grouped["Factures"][0]["summary"]) == 160


def test_empty_or_error_result_is_filed_under_autre_regardless_of_tool():
    history_store.record(
        "fetch_sessions_list", {}, "No sessions found for this criteria."
    )
    history_store.record("fetch_all_invoices_list", {}, "No data returned.")
    history_store.record("trigger_start_session", {}, "Error: Session not found.")

    grouped = history_store.get_grouped()

    assert "Sessions" not in grouped
    assert "Factures" not in grouped
    assert len(grouped["Autre"]) == 3


def test_record_stores_the_originating_question():
    history_store.record(
        "fetch_customer_company",
        {"customer_name": "Marcel Dumont"},
        "Customer: Pharmacie de la Gare | Holder: Marcel Dumont",
        question="which company does Marcel Dumont belong to?",
    )

    grouped = history_store.get_grouped()

    assert (
        grouped["Autre"][0]["question"] == "which company does Marcel Dumont belong to?"
    )


def test_record_without_question_defaults_to_none():
    """Backwards compatible: existing callers not passing question shouldn't break."""
    history_store.record("fetch_all_invoices_list", {}, "Invoices List: ...")

    grouped = history_store.get_grouped()

    assert grouped["Factures"][0]["question"] is None


def test_entries_older_than_24h_are_pruned(monkeypatch):
    fake_now = [1_000_000.0]
    monkeypatch.setattr(history_store.time, "time", lambda: fake_now[0])

    history_store.record("fetch_all_invoices_list", {}, "old entry")

    # Advance the clock by 24h and 1 second.
    fake_now[0] += history_store.RETENTION_SECONDS + 1
    history_store.record("fetch_reminders_list", {}, "fresh entry")

    grouped = history_store.get_grouped()

    assert "Factures" not in grouped
    assert grouped["Relances"][0]["summary"] == "fresh entry"
