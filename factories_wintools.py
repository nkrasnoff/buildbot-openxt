import os

from buildbot.plugins import *
from buildbot.process.results import SUCCESS

# General notes:

step_timeout = 1200

# Base environment:
# The autobuilder tree should look like:
# | workdir_base/openxt
# | workdir_base/openxt/windows/
# | workdir_base/openxt/windows/winbuild-prepare.ps1
# | workdir_base/openxt/windows/winbuild-all.ps1
# | workdir_base/openxt/windows/xc-windows
# | workdir_base/openxt/windows/xc-windows/dobuild.bat
# | workdir_base/openxt/windows/xc-windows/xc-vusb

# NOTE: This is not subtle at all and tied up in a lot of technical debt.
# It is quite convoluted how things tie up together, but it is technically
# possible to build each component then each driver separately.
# Given the past EOL status of most of xc-windows.git, efforts would better be
# invested in upgrading xc-vusb.git and using the upstream provided Xen PV
# drivers for Windows. 9.0 even builds in the EWDK, which makes everything a
# lot more simple.

# Layout of the codebases for the different repositories to the build scripts.
codebase_layout = {
    'openxt': r'\openxt',
    'xc-windows': r'\openxt\windows\xc-windows',
    'xc-vusb': r'\openxt\windows\xc-windows\xc-vusb',
}

def factory_wintools(workdir_base, deploydir, codebases_wintools):
    f = util.BuildFactory()
    f.addStep(steps.ShellSequence(
        hideStepIf=lambda results, s: results==SUCCESS,
        name='Initialize environment',
        haltOnFailure=True,
        commands=[
            util.ShellArg(command=[
                'if', 'not', 'exist' , workdir_base, 'mkdir', workdir_base ],
                haltOnFailure=True, logfile='stdio')
        ]))
    for codebase, _ in codebases_wintools.items():
        destdir = codebase_layout.get(codebase, '/unknown/' + codebase)
        f.addStep(steps.Git(
            haltOnFailure=True,
            workdir=util.Interpolate(workdir_base + destdir),
            repourl=util.Interpolate('%(src:' + codebase + ':repository)s'),
            branch=util.Interpolate('%(src:' + codebase + ':branch)s'),
            codebase=codebase,
            mode='full', method='fresh', clobberOnFailure=True
        ))
    f.addStep(steps.ShellCommand(
        workdir=workdir_base + r'\openxt\windows',
        name='Configure the build environment',
        haltOnFailure=True,
        command=[ 'powershell', r'.\winbuild-prepare.ps1',
            'config=config.xml',
            util.Interpolate("build=%(prop:buildnumber)s"),
            'certname=developer',
            'branch=master']
    ))
    f.addStep(steps.ShellCommand(
        workdir=workdir_base + r'\openxt\windows',
        name='Build all',
        haltOnFailure=True,
        command=['powershell', r'.\winbuild-all.ps1']
    ))
    f.addStep(steps.FileUpload(
        workersrc=workdir_base + r'\openxt\windows\output\xc-wintools.iso',
        masterdest=util.Interpolate(
            deploydir + r'/openxt-wintools-%(prop:buildnumber)s.iso'),
        url=None
    ))
    return f
