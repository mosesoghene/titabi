from drf_spectacular.openapi import AutoSchema


class AppNameTagAutoSchema(AutoSchema):
    def get_tags(self):
        # Default to app label for grouping (e.g. 'accounts', 'jobs')
        view = self.view
        try:
            return [view.__module__.split('.')[0].capitalize()]  # e.g. 'accounts.views' → 'Accounts'
        except Exception:
            return super().get_tags()