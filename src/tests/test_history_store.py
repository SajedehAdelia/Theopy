from src import history_store

USER_A = 100
USER_B = 101


def setup_function():
    """Ensure each test starts from a clean, empty history."""
    history_store.clear()


def test_record_infers_domain_from_tool_name():
    history_store.record(
        "fetch_all_invoices_list",
        {"customer_name": "Gare"},
        "Invoices List: ...",
        user_id=USER_A,
    )
    history_store.record(
        "fetch_planning_dashboard_customers",
        {},
        "Customer Dashboard Summary",
        user_id=USER_A,
    )
    history_store.record(
        "fetch_reminders_list", {}, "Reminders List: ...", user_id=USER_A
    )
    history_store.record(
        "trigger_start_session", {}, "Success: Session 999 started", user_id=USER_A
    )
    history_store.record(
        "unknown_diagnostic_tool", {}, "Mocked response", user_id=USER_A
    )

    grouped = history_store.get_grouped(USER_A)

    assert "Factures" in grouped
    assert "Plannings" in grouped
    assert "Relances" in grouped
    assert "Sessions" in grouped
    assert "Autre" in grouped


def test_get_grouped_returns_most_recent_first():
    history_store.record("fetch_all_invoices_list", {}, "first call", user_id=USER_A)
    history_store.record("fetch_all_invoices_list", {}, "second call", user_id=USER_A)

    grouped = history_store.get_grouped(USER_A)

    assert [entry["summary"] for entry in grouped["Factures"]] == [
        "second call",
        "first call",
    ]


def test_summary_is_truncated_to_160_chars():
    long_result = "x" * 500
    history_store.record("fetch_all_invoices_list", {}, long_result, user_id=USER_A)

    grouped = history_store.get_grouped(USER_A)

    assert len(grouped["Factures"][0]["summary"]) == 160


def test_empty_or_error_result_is_filed_under_autre_regardless_of_tool():
    history_store.record(
        "fetch_sessions_list",
        {},
        "No sessions found for this criteria.",
        user_id=USER_A,
    )
    history_store.record(
        "fetch_all_invoices_list", {}, "No data returned.", user_id=USER_A
    )
    history_store.record(
        "trigger_start_session", {}, "Error: Session not found.", user_id=USER_A
    )

    grouped = history_store.get_grouped(USER_A)

    assert "Sessions" not in grouped
    assert "Factures" not in grouped
    assert len(grouped["Autre"]) == 3


def test_record_stores_the_originating_question():
    history_store.record(
        "fetch_customer_company",
        {"customer_name": "Marcel Dumont"},
        "Customer: Pharmacie de la Gare | Holder: Marcel Dumont",
        question="which company does Marcel Dumont belong to?",
        user_id=USER_A,
    )

    grouped = history_store.get_grouped(USER_A)

    assert (
        grouped["Autre"][0]["question"] == "which company does Marcel Dumont belong to?"
    )


def test_record_without_question_defaults_to_none():
    """Backwards compatible: existing callers not passing question shouldn't break."""
    history_store.record(
        "fetch_all_invoices_list", {}, "Invoices List: ...", user_id=USER_A
    )

    grouped = history_store.get_grouped(USER_A)

    assert grouped["Factures"][0]["question"] is None


def test_entries_older_than_24h_are_pruned(monkeypatch):
    fake_now = [1_000_000.0]
    monkeypatch.setattr(history_store.time, "time", lambda: fake_now[0])

    history_store.record("fetch_all_invoices_list", {}, "old entry", user_id=USER_A)

    # Advance the clock by 24h and 1 second.
    fake_now[0] += history_store.RETENTION_SECONDS + 1
    history_store.record("fetch_reminders_list", {}, "fresh entry", user_id=USER_A)

    grouped = history_store.get_grouped(USER_A)

    assert "Factures" not in grouped
    assert grouped["Relances"][0]["summary"] == "fresh entry"


def test_get_grouped_only_returns_the_requesting_users_own_entries():
    history_store.record(
        "fetch_all_invoices_list", {}, "user A's invoice call", user_id=USER_A
    )
    history_store.record(
        "fetch_all_invoices_list", {}, "user B's invoice call", user_id=USER_B
    )

    grouped_a = history_store.get_grouped(USER_A)
    grouped_b = history_store.get_grouped(USER_B)

    assert [entry["summary"] for entry in grouped_a["Factures"]] == [
        "user A's invoice call"
    ]
    assert [entry["summary"] for entry in grouped_b["Factures"]] == [
        "user B's invoice call"
    ]


def test_get_grouped_excludes_entries_recorded_without_a_user_id():
    """Entries recorded before this migration (user_id=NULL) must not be shown
    to anyone - not attributed to the wrong person."""
    history_store.record(
        "fetch_all_invoices_list", {}, "pre-migration entry", user_id=None
    )

    grouped = history_store.get_grouped(USER_A)

    assert grouped == {}
