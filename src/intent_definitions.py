
INTENT_MAP = {
    "SESSION_QUERY": {
        "keywords": ["session", "intervention", "visite"],
        "route": "/api/theopy/sessions",
        "method": "GET",
        "description": "Used to fetch general session history."
    },
    "CUSTOMER_SESSION": {
        "keywords": ["pharmacie", "client", "gare"],
        "route": "/api/theopy/sessions/customer",
        "method": "GET",
        "description": "Used when a specific pharmacy name is mentioned."
    },
    "INVOICE_SUMMARY": {
        "keywords": ["facture", "argent", "compta", "unpaid"],
        "route": "/api/theopy/invoices/summary",
        "method": "GET",
        "description": "Used for financial status queries."
    }
}