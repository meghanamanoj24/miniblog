from django.contrib.sites.shortcuts import get_current_site

class SEOMetaMixin:
    def get_meta_description(self):
        return getattr(self, 'meta_description', None)

    def get_meta_keywords(self):
        return getattr(self, 'meta_keywords', None)

    def get_meta_title(self):
        return getattr(self, 'meta_title', None)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['meta_description'] = self.get_meta_description()
        context['meta_keywords'] = self.get_meta_keywords()
        context['meta_title'] = self.get_meta_title()
        context['canonical_url'] = self.request.build_absolute_uri()
        return context 