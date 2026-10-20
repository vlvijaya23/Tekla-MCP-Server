class ApprovalEngine:

    def evaluate(
        self,
        confidence
    ):

        if confidence >= 95:

            return (
                "AUTO APPROVED",
                "GREEN"
            )

        if confidence >= 70:

            return (
                "REVIEW",
                "ORANGE"
            )

        return (
            "CHECK REQUIRED",
            "RED"
        )