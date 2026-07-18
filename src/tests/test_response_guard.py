from src.response_guard import CLARIFICATION_FALLBACK, sanitize_final_answer


def test_leaked_tool_call_with_parameters_is_replaced():
    leaked = '{"name": "fetch_inventory", "parameters": {"customer_name": "Gare"}}'
    assert sanitize_final_answer(leaked) == CLARIFICATION_FALLBACK


def test_leaked_tool_call_with_arguments_is_replaced():
    leaked = '{"name": "fetch_inventory", "arguments": {}}'
    assert sanitize_final_answer(leaked) == CLARIFICATION_FALLBACK


def test_normal_markdown_answer_is_untouched():
    answer = "Here is the table you requested:\n\n| ID | Total |\n|----|-------|\n| 101 | 150€ |"
    assert sanitize_final_answer(answer) == answer


def test_plain_text_answer_is_untouched():
    answer = "No invoices found for this criteria."
    assert sanitize_final_answer(answer) == answer


def test_json_looking_text_without_name_key_is_untouched():
    # Starts with '{' but isn't a tool-call shape - should pass through.
    answer = '{"status": "ok"}'
    assert sanitize_final_answer(answer) == answer


def test_narrated_tool_name_in_a_sentence_is_replaced():
    # Real regression: the model narrates an intended call instead of executing it
    # or answering directly, leaking the raw tool identifier into the chat.
    leaked = (
        "Since there are no session with the customer name Marcel Dumont, let me "
        "try to fetch customer details directly. Let me call fetch_customer_details tool."
    )
    assert sanitize_final_answer(leaked) == CLARIFICATION_FALLBACK


def test_trigger_prefixed_tool_name_is_also_caught():
    leaked = "I'll go ahead and trigger_start_session for you now."
    assert sanitize_final_answer(leaked) == CLARIFICATION_FALLBACK
