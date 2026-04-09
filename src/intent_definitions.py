INTENT_MAP = {
    "SESSION_QUERY": {
        "keywords": ["session", "intervention", "visite", "travail", "historique", "log"],
        "route": "/api/theopy/sessions",
        "method": "GET",
        "description": "General list of all recent interventions."
    },
    "CUSTOMER_SESSION": {
        "keywords": ["client", "pharmacie", "gare", "soleil", "nuit", "détails", "ouvrir"],
        "route": "/api/theopy/sessions/customer",
        "method": "GET",
        "description": "Specific intervention history for a named pharmacy. Useful for 'Open the page for X'."
    },
    "INVOICE_SUMMARY": {
        "keywords": ["facture", "argent", "compta", "unpaid", "impayés", "bilan", "chiffre", "paiement"],
        "route": "/api/theopy/invoices/summary",
        "method": "GET",
        "description": "Financial summary including totals, taxes, and creditor bank info."
    }
}

TOOLS = [
    {
        "name": "get_customer_sessions",
        "description": "Fetches detailed intervention sessions. Use this when the user wants to see specific work logs or IDs for a pharmacy.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "customer_name": {"type": "STRING", "description": "The exact name of the pharmacy from the request."}
            },
            "required": ["customer_name"]
        }
    },
    {
        "name": "get_invoice_summary",
        "description": "Fetches the financial dashboard. Use this for questions about money, unpaid invoices, or accounting totals.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "customer_name": {"type": "STRING", "description": "The name of the pharmacy"}
            },
            "required": ["customer_name"]
        }
    },
    {
        "name": "open_session_page",
        "description": "Triggers a UI navigation to the specific workspace of a pharmacy.",
        "parameters": {
            "type": "OBJECT",
            "properties": {
                "customer_name": {"type": "STRING"}
            },
            "required": ["customer_name"]
        }
    }
]