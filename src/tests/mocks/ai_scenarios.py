class MCPSimulator:
    """
    A deterministic state machine simulating the Teepy MCP Server.
    All data returned perfectly mirrors the backend dev_data.sql state.
    """

    def __init__(self):
        # Internal state to simulate database mutations
        self.active_session_id = None
        self.lines_added = 0
        self.treated_reminders = set()
        self.paid_invoices = set()

    def execute_tool(self, tool_name: str, arguments: dict) -> str:
        """Routes the tool call to the correct mock response based on arguments."""

        # ---------------------------------------------------------------------
        # DOMAIN: INVOICES
        # ---------------------------------------------------------------------
        if tool_name == "fetch_all_invoices_list":
            customer = arguments.get("customer_name", "").lower()
            if "gare" in customer:
                return (
                    "Invoices List:\n"
                    "Invoice ID: 101 | Pharmacy: Pharmacie de la Gare | "
                    "Date: 2019-02-01 | Total: 150.0€ | Status: Unpaid\n"
                    "Invoice ID: 106 | Pharmacy: Pharmacie de la Gare | "
                    "Date: 2021-02-01 | Total: 150.0€ | Status: Unpaid"
                )
            elif "soleil" in customer:
                return (
                    "Invoices List:\n"
                    "Invoice ID: 102 | Pharmacy: Pharmacie du Soleil | "
                    "Date: 2020-01-01 | Total: 150.0€ | Status: Unpaid\n"
                    "Invoice ID: 107 | Pharmacy: Pharmacie du Soleil | "
                    "Date: 2021-02-01 | Total: 150.0€ | Status: Unpaid"
                )
            # Simulate an empty response
            elif customer:
                return "No invoices found for this criteria."

            return "Invoices List:\n(15 invoices total across all customers)"

        elif tool_name == "fetch_mark_invoice_status":
            inv_id = arguments.get("invoice_id")
            if arguments.get("is_paid"):
                self.paid_invoices.add(inv_id)
                return f"Success: Invoice {inv_id} has been marked as Paid."
            return f"Success: Invoice {inv_id} has been marked as Unpaid."

        # ---------------------------------------------------------------------
        # DOMAIN: PLANNING & DASHBOARDS
        # ---------------------------------------------------------------------
        elif tool_name == "fetch_planning_dashboard_customers":
            customer = arguments.get("customer_name", "").lower()
            if "groupement" in customer or "méchant" in customer:
                # Testing the complex groupement architecture
                return (
                    "Customer Dashboard Summary:\n"
                    "Customer: Méchant Groupement | Freq: monthly | "
                    "Planned: 10h00 | Done: 8h30 | Charged: 8h00\n"
                    "Customer: Méchante Pharmacie | Freq: weekly | "
                    "Planned: 2h00 | Done: 1h30 | Charged: 1h30"
                )
            return (
                "Customer Dashboard Summary (5/2019):\n"
                "Customer: Pharmacie de la Gare | Freq: monthly | "
                "Planned: 2h00 | Done: 1h30 | Charged: 1h30"
            )

        elif tool_name == "fetch_planning_dashboard_operators":
            return (
                "Operator Dashboard Summary (Year: 2019, Week: 21):\n"
                "Operator: Mathieu Onésime | Planned: 5h00 | Done: 4h30 | Charged: 4h30\n"
                "Operator: Christelle Beauchamp | Planned: 2h30 | Done: 2h30 | Charged: 2h00"
            )

        # ---------------------------------------------------------------------
        # DOMAIN: SESSIONS
        # ---------------------------------------------------------------------
        elif tool_name == "fetch_sessions_list":
            start = arguments.get("start")
            if start == "2019-05-20":
                return (
                    "Sessions List:\n"
                    "Session ID: 100 | Customer: Prestataire | "
                    "Start: 2019-05-21 09:32:18 | End: 2019-05-21 12:32:17\n"
                    "Session ID: 101 | Customer: Prestataire | "
                    "Start: 2019-05-22 09:32:18 | End: 2019-05-22 12:12:44"
                )
            return "No sessions found for this criteria."

        # --- MULTI-STEP SESSION FLOW ---
        elif tool_name == "trigger_start_session":
            self.active_session_id = 999
            self.lines_added = 0
            return f"Success: Session {self.active_session_id} started successfully."

        elif tool_name == "trigger_add_session_line":
            if not self.active_session_id:
                return "Error: Session not found."
            self.lines_added += 1
            return f"Success: Line {self.lines_added} added to session {self.active_session_id}."

        elif tool_name == "trigger_close_session":
            if not self.active_session_id:
                return "Error: Session not found or already closed."
            closed_id = self.active_session_id
            self.active_session_id = None
            return f"Success: Session {closed_id} successfully closed with {self.lines_added} lines."

        # ---------------------------------------------------------------------
        # DOMAIN: REMINDERS
        # ---------------------------------------------------------------------
        elif tool_name == "fetch_reminders_list":
            if arguments.get("pending_only"):
                # If reminder 100 was treated, only show 101
                if 100 in self.treated_reminders:
                    return (
                        "Reminders List:\nID: 101 | Customer: Prestataire | "
                        "Date: 2019-03-02 | Author: Mathieu Onésime | Status: Pending | "
                        "Comment: à se souvenir une nouvelle fois"
                    )

                return (
                    "Reminders List:\n"
                    "ID: 100 | Customer: Prestataire | Date: 2019-03-02 | "
                    "Author: Christelle Beauchamp | Status: Pending | Comment: à se souvenir\n"
                    "ID: 101 | Customer: Prestataire | Date: 2019-03-02 | "
                    "Author: Mathieu Onésime | Status: Pending | Comment: à se souvenir une nouvelle fois"
                )
            return "Reminders List:\n(All historic reminders displayed)"

        elif tool_name == "trigger_treat_reminder":
            rem_id = arguments.get("reminder_id")
            if arguments.get("treat"):
                self.treated_reminders.add(rem_id)
                return f"Success: Reminder {rem_id} marked as Treated."

            self.treated_reminders.discard(rem_id)
            return f"Success: Reminder {rem_id} marked as Pending."

        # ---------------------------------------------------------------------
        # FALLBACK
        # ---------------------------------------------------------------------
        return f"Mocked response for tool: {tool_name}"


# Global instance to be shared across a single test run
mcp_simulator = MCPSimulator()


def mock_call_tool(tool_name: str, arguments: dict) -> str:
    """The function injected into the MCP Client via Pytest monkeypatch."""
    return mcp_simulator.execute_tool(tool_name, arguments)
