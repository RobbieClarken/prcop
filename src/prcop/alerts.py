class ReviewOverdueAlert:
    def __init__(self, pr):
        self.pr = pr

    def __str__(self):
        opened = int(self.pr.business_hours_since_opened.total_seconds() / 3600)
        reviews_str = "review" if self.pr.reviews_remaining == 1 else "reviews"
        return (
            f'Pull request "{self.pr.title}" (opened {opened} business hours ago) '
            f"needs {self.pr.reviews_remaining} more {reviews_str}:\n"
            f"{self.pr.url}"
        )
