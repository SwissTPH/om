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

import json
from xml.etree.ElementTree import ParseError

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import JsonResponse
from django.views.generic.base import TemplateView
from vecnet.openmalaria.monitoring import get_survey_times
from vecnet.openmalaria.scenario import Scenario

from website.apps.ts_om import submit
from website.apps.ts_om.forms import ScenarioSummaryForm
from website.apps.ts_om.models import Scenario as ScenarioModel
from website.middleware import HttpRedirectException
from website.notification import set_notification


class ScenarioSummaryView(TemplateView):
    template_name = "ts_om/summary.html"
    form_class = ScenarioSummaryForm
    model_scenario = None
    scenario = None

    def post(self, *args, **kwargs):
        scenario_id = self.kwargs["scenario_id"]
        scenario = ScenarioModel.objects.get(id=scenario_id)
        if self.request.user != scenario.user:
            raise PermissionDenied
        scenario.name = self.request.POST.get('name', scenario.name)
        scenario.description = self.request.POST.get('desc', scenario.description)

        if not self.request.is_ajax() or "save" in self.request.POST and json.loads(self.request.POST["save"]):
            scenario.save()

        if self.request.is_ajax():
            return JsonResponse({"success": True, "xml": scenario.xml})

        if 'submit_type' in self.request.POST and self.request.POST["submit_type"] == "run":
            # Clicked "Save and Run" button
            # Will submit a scenario to Simulation Manager here
            simulation = submit.submit_new(scenario)
            if simulation is None:
                set_notification(self.request, "Can't submit simulation", "alert-danger")
            else:
                # scenario.simulation = simulation
                # scenario.save()
                set_notification(self.request, "Successfully started simulation", "alert-success")
        raise HttpRedirectException(reverse('ts_om.list'))

    def get_context_data(self, **kwargs):
        context = super(ScenarioSummaryView, self).get_context_data(**kwargs)
        scenario_id = self.kwargs["scenario_id"]
        self.model_scenario = ScenarioModel.objects.get(id=scenario_id)

        if self.request.user != self.model_scenario.user:
            raise PermissionDenied
        try:
            self.scenario = Scenario(self.model_scenario.xml)
        except ParseError:
            self.scenario = None

        vectors = []

        for v in self.scenario.entomology.vectors:
            vectors.append(v)

        if self.scenario:
            context["scenario"] = self.model_scenario
            context["scenario_id"] = self.model_scenario.id
            context["name"] = self.model_scenario.name
            context["desc"] = self.model_scenario.description if self.model_scenario.description else ""
            context["deleted"] = self.model_scenario.deleted
            context["version"] = self.scenario.schemaVersion

            if self.model_scenario.new_simulation:
                context['sim_id'] = self.model_scenario.new_simulation.id

            context["xml"] = self.scenario.xml

            monitor_info = get_survey_times(self.scenario.monitoring, self.model_scenario.start_date)

            context["monitor_type"] = monitor_info["type"]
            context["monitor_yrs"] = monitor_info["yrs"]
            context["monitor_mos"] = monitor_info["mos"]
            context["timesteps"] = monitor_info["timesteps"]

            context["demography"] = self.scenario.demography.name
            context["pop_size"] = self.scenario.demography.popSize

            context["first_line_drug"] = self.scenario.healthSystem.ImmediateOutcomes.firstLine
            context["vectors"] = vectors
            if hasattr(self.scenario.entomology, 'scaledAnnualEIR'):
                context["annual_eir"] = self.scenario.entomology.scaledAnnualEIR
            else:
                context["annual_eir"] = None

            interventions = []
            for component in self.scenario.interventions.human:
                interventions.append(component.id)
            for vectorPop in self.scenario.interventions.vectorPop:
                interventions.append(vectorPop.name)

            context["interventions"] = interventions

        return context
