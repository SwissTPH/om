# -*- coding: utf-8 -*-
#
# This file is part of the VecNet OpenMalaria Portal.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/om
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.generic import ListView

from website.apps.ts_om.models import Scenario as ScenarioModel


class ScenarioListView(ListView):
    template_name = 'ts_om/list.html'
    paginate_by = 10
    model = ScenarioModel

    # ensure_csrf_cookie is to send CSRF cookie with this view - to ensure that DeleteView is working properly
    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        return super(ScenarioListView, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        scenarios = ScenarioModel.objects.filter(user=self.request.user, deleted=False).order_by('-last_modified')
        return scenarios

    def get_context_data(self, **kwargs):
        context = super(ScenarioListView, self).get_context_data(**kwargs)

        return context
