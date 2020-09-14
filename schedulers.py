# -*- python -*-

from buildbot.plugins import (
    schedulers,
    util
)
from config import codebases_to_params

def scheduler_force_repo(name, builders, manifest_dfl, template_dfl, codebases_repo):
    return schedulers.ForceScheduler(
        name=name, buttonName="Repo build", label="Manual Repo build",
        reason=util.StringParameter(
            name="reason", label="Reason:", required=False, size=140
        ),
        builderNames=builders,
        codebases=codebases_to_params(codebases_repo),
        properties=[
            util.StringParameter(
                name="manifest", label="Manifest File:", default=manifest_dfl
            ),
            util.StringParameter(
                name="template", label="Configuration Template:",
                default=template_dfl
            )
        ])

def scheduler_force_custom(name, buttonName, builders, template_dfl, codebases_custom):
    return schedulers.ForceScheduler(
        name=name,
        buttonName=buttonName,
        label="Manual Custom build",
        reason=util.StringParameter(
            name="reason", label="Reason:", required=False, size=140
        ),
        builderNames=builders,
        codebases=codebases_to_params(codebases_custom),
        properties=[
            util.StringParameter(
                name="template", label="Configuration Template:",
                default=template_dfl
            )
        ])

def scheduler_force_stable(name, builders, template_dfl, codebases_stable):
    return schedulers.ForceScheduler(
        name=name,
        buttonName="Stable build",
        label="Trigger stable build",
        reason=util.StringParameter(
            name="reason", label="Reason:", required=False, size=140
        ),
        builderNames=builders,
        codebases=codebases_to_params(codebases_stable),
        properties=[
            util.StringParameter(
                name="template", label="Configuration Template:",
                default=template_dfl
            )
        ])

def scheduler_nightly(name, builders, template_dfl, codebases, hour, minute):
    return schedulers.Nightly(
        name=name,
        codebases=codebases,
        properties={
            'template': template_dfl
        },
        builderNames=builders,
        hour=hour,
        minute=minute,
        onlyIfChanged=True)

def scheduler_force_wintools(name, builders, codebases_wintools):
    return schedulers.ForceScheduler(
        name=name,
        buttonName="Wintools build",
        label="Manual Windows Tools build",
        reason=util.StringParameter(
            name="reason", label="Reason:", required=False, size=140
        ),
        builderNames=builders,
        codebases=codebases_to_params(codebases_wintools)
    )

def scheduler_nightly_wintools(name, builders, codebases, hour, minute):
    return schedulers.Nightly(
        name=name,
        codebases=codebases,
        builderNames=builders,
        hour=hour,
        minute=minute,
        onlyIfChanged=True)
