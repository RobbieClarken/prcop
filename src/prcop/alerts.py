class ReviewOverdueAlert:
    def __init__(self, pr):
        self.pr = pr

    def __str__(self):
        hours_since_updated = int(self.pr.business_hours_since_updated.total_seconds() / 3600)
        reviews_str = "review" if self.pr.reviews_remaining == 1 else "reviews"
        return (
            f'Pull request "{self.pr.title}" '
            f"(last updated {hours_since_updated} business hours ago) "
            f"needs {self.pr.reviews_remaining} more {reviews_str}:\n"
            f"{self.pr.url}"
        )
