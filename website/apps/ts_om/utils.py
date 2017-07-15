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
import datetime
from django.contrib.auth.models import User
from django.core.files.base import ContentFile

from data_services.models import Simulation
from website.apps.email.utils.send_html_email import send_html_email
from website.apps.ts_om.models import Simulation as SimulationNew, Scenario


def migrate_simulations():
    # This function is for use in data migration. Should be removed after data on the server has been migrated
    for simulation in Simulation.objects.all():
        print simulation.id
        simulation_new = SimulationNew()
        input_file = simulation.input_files.filter(name="scenario.xml").first()
        if input_file:
            print input_file
            simulation_new.input_file.save(
                "scenario_%s.xml" % simulation_new.id,
                ContentFile(input_file.get_contents())
            )
        output_file = simulation.simulationoutputfile_set.filter(name="output.txt").first()
        if output_file:
            print output_file
            simulation_new.output_file.save(
                "output_%s.txt" % simulation_new.id,
                ContentFile(output_file.get_contents())
            )

        ctsout_file = simulation.simulationoutputfile_set.filter(name="ctsout.txt").first()
        if ctsout_file:
            print ctsout_file
            simulation_new.ctsout_file.save(
                "ctsout_%s.txt" % simulation_new.id,
                ContentFile(ctsout_file.get_contents())
            )

        stdout = simulation.simulationoutputfile_set.filter(name="stdout.txt").first()
        if stdout:
            print stdout
            simulation_new.model_stdout.save(
                "stdout_%s.txt" % simulation_new.id,
                ContentFile(stdout.get_contents())
            )

        if simulation.status == "done":
            simulation_new.status = SimulationNew.COMPLETE
        elif simulation.status == "error":
            simulation_new.status = SimulationNew.FAILED
        elif simulation.status == "ready":
            simulation_new.status = SimulationNew.NEW

        simulation_new.save()
        scenario = simulation.scenario_set.all().first()
        if scenario:
            scenario.new_simulation = simulation_new
            scenario.save()


def get_number_at_the_end_of_string(string):
    """ Return number at the end of the string (or None)
    Examples:
    "Scenario 23" -> 23
    "Scenario -23" -> 23
    "Scenario" -> None
    "123" -> 123
    :param string:
    :return:
    """
    n = -1
    number = ""
    try:
        while True:
            ch = string[n]
            if ch.isdigit():
                number += ch
                n -= 1
            else:
                raise IndexError
    except IndexError:
        pass
    if number:
        # Reverse string
        return int(number[::-1])
    else:
        return None

def scenario_name_with_next_number(name):
    """ Generate new scenario name when coping scenario
    "Kenya"     -> "Kenya - 2"
    "Kenya - 4" -> "Kenya - 5"
    :param name: Current scenario name
    :return: New scenario name, with number at the end increased by 1
    """
    name = name.strip()
    number = get_number_at_the_end_of_string(name)
    if number is None:
        return name + " - 2"
    else:
        return name[0:-len(str(number))] + str(number + 1)


def get_users_created_yesterday():
    return User.objects.filter(date_joined__date=(datetime.datetime.today() - datetime.timedelta(days=1)))


def get_scenarios_updated_yesterday():
    return Scenario.objects.filter(last_modified__date=(datetime.datetime.today() - datetime.timedelta(days=1)))

def get_simulations_in_progress():
    return SimulationNew.objects.filter(status=SimulationNew.RUNNING)

def send_daily_report(emails):
    users_created_yesterday = get_users_created_yesterday()
    send_html_email(
        recipients=emails,
        subject="OpenMalaria Portal report (%s scenarios updated)" % get_scenarios_updated_yesterday().count(),
        text="New portal users report",
        template_path="ts_om/emails/new_users_report.html",
        users=users_created_yesterday,
        scenarios=get_scenarios_updated_yesterday(),
        simulation_in_progress=get_simulations_in_progress(),
    )
