#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.2.4),
    on Tue Apr 29 10:04:01 2025
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
prefs.hardware['audioLib'] = 'ptb'
prefs.hardware['audioLatencyMode'] = '3'
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2024.2.4'
expName = 'comp'  # from the Builder filename that created this script
# information about this experiment
expInfo = {
    'participant': '',
    'computer': '',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = [1920, 1080]
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='/Users/seanconway/Research/Perceptual_CE/comparability_2/experiment_code/comp.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('info')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=True, allowStencil=False,
            monitor='testMonitor', color=[1.0000, 1.0000, 1.0000], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='pix',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [1.0000, 1.0000, 1.0000]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'pix'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    # show a visual indicator if we're in piloting mode
    if PILOTING and prefs.piloting['showPilotingIndicator']:
        win.showPilotingIndicator()
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    # Setup iohub experiment
    ioConfig['Experiment'] = dict(filename=thisExp.dataFileName)
    
    # Start ioHub server
    ioServer = io.launchHubServer(window=win, **ioConfig)
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='iohub'
        )
    if deviceManager.getDevice('key_resp') is None:
        # initialise key_resp
        key_resp = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp',
        )
    if deviceManager.getDevice('key_resp_2') is None:
        # initialise key_resp_2
        key_resp_2 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_2',
        )
    if deviceManager.getDevice('key_resp_3') is None:
        # initialise key_resp_3
        key_resp_3 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_3',
        )
    if deviceManager.getDevice('key_resp_4') is None:
        # initialise key_resp_4
        key_resp_4 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_4',
        )
    if deviceManager.getDevice('key_resp_5') is None:
        # initialise key_resp_5
        key_resp_5 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_5',
        )
    if deviceManager.getDevice('key_resp_6') is None:
        # initialise key_resp_6
        key_resp_6 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_6',
        )
    if deviceManager.getDevice('rect_choice') is None:
        # initialise rect_choice
        rect_choice = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='rect_choice',
        )
    if deviceManager.getDevice('key_resp_7') is None:
        # initialise key_resp_7
        key_resp_7 = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='key_resp_7',
        )
    if deviceManager.getDevice('end_debrief') is None:
        # initialise end_debrief
        end_debrief = deviceManager.addDevice(
            deviceClass='keyboard',
            deviceName='end_debrief',
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='ioHub',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ioHub'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "consent" ---
    agree_button = visual.ButtonStim(win, 
        text='I agree', font='Arvo',
        pos=(-75, -500),
        letterHeight=20.0,
        size=[100,100], 
        ori=0.0
        ,borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='black', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='agree_button',
        depth=0
    )
    agree_button.buttonClock = core.Clock()
    decline_button = visual.ButtonStim(win, 
        text='I do not agree', font='Arvo',
        pos=[75,-500],
        letterHeight=20.0,
        size=[100,100], 
        ori=0.0
        ,borderWidth=0.0,
        fillColor='darkgrey', borderColor=None,
        color='black', colorSpace='rgb',
        opacity=None,
        bold=True, italic=False,
        padding=None,
        anchor='center',
        name='decline_button',
        depth=-1
    )
    decline_button.buttonClock = core.Clock()
    consent_img = visual.ImageStim(
        win=win,
        name='consent_img', 
        image='consent.png', mask=None, anchor='bottom-center',
        ori=0.0, pos=(0, -475), draggable=False, size=[825,1000],
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=-2.0)
    mouse = event.Mouse(win=win)
    x, y = [None, None]
    mouse.mouseClock = core.Clock()
    
    # --- Initialize components for Routine "exp_params" ---
    # Run 'Begin Experiment' code from params
    # setting constant parameters for the experiment
    import psychopy
    import numpy as np
    
    # lower diagonal for catch trials
    d1_r=np.arange(57,133)
    
    # upper diagonal for catch trials
    d2_r=np.arange(125,200)
    
    # intercept for lower diagonal for catch trials
    d1_int=190
    
    # intercept for upper diagonal for catch trials
    d2_int=325
    
    # lowest dimension size possible on fillers
    dim_min = 57
    
    # larrgest dimension size possible on fillers
    dim_max = 200
    
    # screen params
    screen_width=win.size[0]
    screen_height=win.size[1]
    screen_center_x=0
    screen_center_y=0
    
    # distance between rectangles on x axis
    rect_dist_perc = .10
    rect_dist=round(rect_dist_perc*(.5*screen_width))
    
    # jitter for rectangle y position
    y_jitter=20
    
    # prompt text on each trial
    prompt_x_loc=0
    prompt_y_loc=-round(screen_height * .5)+80
    
    # inter-stimulus interval in secs
    isi=.15
    # Run 'Begin Experiment' code from fncs_
    # function to sample stimulus from the diagonal
    # requires a diagonal range and an intercept
    def sample_diag (d, intcpt):
        w=np.random.choice(d)
        h=intcpt-w
        stim=np.array([w,h])
        return stim
    
    # --- Initialize components for Routine "welcome" ---
    welcome_text = visual.TextStim(win=win, name='welcome_text',
        text='Welcome to the experiment!',
        font='Arial',
        pos=(0, 0), draggable=False, height=35.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "instructions_1" ---
    instructions_1_text_1 = visual.TextStim(win=win, name='instructions_1_text_1',
        text='In this experiment, you will be making decisions about rectangles.',
        font='Arial',
        pos=(0, 300), draggable=False, height=30.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    instructions_1_text_2 = visual.TextStim(win=win, name='instructions_1_text_2',
        text='Press space to continue the instructions.',
        font='Arial',
        pos=(0, -300), draggable=False, height=30.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    key_resp = keyboard.Keyboard(deviceName='key_resp')
    
    # --- Initialize components for Routine "instructions_2" ---
    instructions_2_text_1 = visual.TextStim(win=win, name='instructions_2_text_1',
        text='On each trial, you will see three rectangles labeled 1, 2, and 3. You will select the rectangle with the largest area by pressing the corresponding key.',
        font='Arial',
        pos=(0, 0), draggable=False, height=30.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    instructions_2_text_2 = visual.TextStim(win=win, name='instructions_2_text_2',
        text='Press space to continue the instructions.',
        font='Arial',
        pos=(0, -300), draggable=False, height=30.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    key_resp_2 = keyboard.Keyboard(deviceName='key_resp_2')
    
    # --- Initialize components for Routine "instructions_3" ---
    instructions_3_text_1 = visual.TextStim(win=win, name='instructions_3_text_1',
        text='Here is an example of the rectangles you might see:',
        font='Arial',
        pos=(0, 300), draggable=False, height=30.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    r1_instr3 = visual.Rect(
        win=win, name='r1_instr3',
        width=(150, 100)[0], height=(150, 100)[1],
        ori=0.0, pos=(-300, 10), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor=[-1.0000, -1.0000, -1.0000], fillColor=[0.0039, 0.0039, 0.0039],
        opacity=None, depth=-1.0, interpolate=True)
    r2_instr3 = visual.Rect(
        win=win, name='r2_instr3',
        width=(200, 225)[0], height=(200, 225)[1],
        ori=0.0, pos=(0, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor=[-1.0000, -1.0000, -1.0000], fillColor=[0.0039, 0.0039, 0.0039],
        opacity=None, depth=-2.0, interpolate=True)
    r3_instr3 = visual.Rect(
        win=win, name='r3_instr3',
        width=(100, 75)[0], height=(100, 75)[1],
        ori=0.0, pos=(300, 0), draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor=[-1.0000, -1.0000, -1.0000], fillColor=[0.0039, 0.0039, 0.0039],
        opacity=None, depth=-3.0, interpolate=True)
    r1_instr3_label = visual.TextStim(win=win, name='r1_instr3_label',
        text='1',
        font='Arial',
        pos=(-300, -100), draggable=False, height=25.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-4.0);
    r2_instr3_label = visual.TextStim(win=win, name='r2_instr3_label',
        text='2',
        font='Arial',
        pos=(0, -150), draggable=False, height=25.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-5.0);
    r3_instr3_label = visual.TextStim(win=win, name='r3_instr3_label',
        text='3',
        font='Arial',
        pos=(300, -100), draggable=False, height=25.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-6.0);
    instructions_3_text_3 = visual.TextStim(win=win, name='instructions_3_text_3',
        text="On this trial, rectangle 2 has the largest area, so you would press the '2' key.",
        font='Arial',
        pos=(0, -300), draggable=False, height=30.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-7.0);
    key_resp_3 = keyboard.Keyboard(deviceName='key_resp_3')
    instructions_3_text_4 = visual.TextStim(win=win, name='instructions_3_text_4',
        text="Press 'space' to continue the instructions.",
        font='Arial',
        pos=(0, -400), draggable=False, height=30.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-9.0);
    
    # --- Initialize components for Routine "instructions_4" ---
    instructions_4_text_1 = visual.TextStim(win=win, name='instructions_4_text_1',
        text='Not all trials will be this easy. However, please try your best regardless.',
        font='Arial',
        pos=(0, 200), draggable=False, height=35.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    instructions_4_text_3 = visual.TextStim(win=win, name='instructions_4_text_3',
        text='Press space to continue the instructions.',
        font='Arial',
        pos=(0, -300), draggable=False, height=35.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    instructions_4_text_2 = visual.TextStim(win=win, name='instructions_4_text_2',
        text='There will be 3 blocks of trials. There will be a short break in between each block.',
        font='Arial',
        pos=(0, 0), draggable=False, height=35.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-2.0);
    key_resp_4 = keyboard.Keyboard(deviceName='key_resp_4')
    
    # --- Initialize components for Routine "instructions_5" ---
    instructions_5_text_1 = visual.TextStim(win=win, name='instructions_5_text_1',
        text='At this point, you should let the researcher know if you have any questions.',
        font='Arial',
        pos=(0, 0), draggable=False, height=35.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    instructions_5_text_2 = visual.TextStim(win=win, name='instructions_5_text_2',
        text='Press space to continue the instructions.',
        font='Arial',
        pos=(0, -300), draggable=False, height=35.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-1.0);
    key_resp_5 = keyboard.Keyboard(deviceName='key_resp_5')
    
    # --- Initialize components for Routine "start_exp" ---
    start_exp_text = visual.TextStim(win=win, name='start_exp_text',
        text='Press the spacebar to start the experiment.',
        font='Arial',
        pos=(0, 0), draggable=False, height=35.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_resp_6 = keyboard.Keyboard(deviceName='key_resp_6')
    
    # --- Initialize components for Routine "pre_trial" ---
    
    # --- Initialize components for Routine "choice_trial" ---
    r_1 = visual.Rect(
        win=win, name='r_1',
        width=[1.0, 1.0][0], height=[1.0, 1.0][1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor=[-1.0000, -1.0000, -1.0000], fillColor=[0.0039, 0.0039, 0.0039],
        opacity=None, depth=0.0, interpolate=True)
    r_2 = visual.Rect(
        win=win, name='r_2',
        width=[1.0, 1.0][0], height=[1.0, 1.0][1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor=[-1.0000, -1.0000, -1.0000], fillColor=[0.0039, 0.0039, 0.0039],
        opacity=None, depth=-1.0, interpolate=True)
    r_3 = visual.Rect(
        win=win, name='r_3',
        width=[1.0, 1.0][0], height=[1.0, 1.0][1],
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor=[-1.0000, -1.0000, -1.0000], fillColor=[0.0039, 0.0039, 0.0039],
        opacity=None, depth=-2.0, interpolate=True)
    r_1_label = visual.TextStim(win=win, name='r_1_label',
        text='1',
        font='Arial',
        pos=[0,0], draggable=False, height=20.0, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-3.0);
    r_2_label = visual.TextStim(win=win, name='r_2_label',
        text='2',
        font='Arial',
        pos=[0,0], draggable=False, height=20.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-4.0);
    r_3_label = visual.TextStim(win=win, name='r_3_label',
        text='3',
        font='Arial',
        pos=[0,0], draggable=False, height=20.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-5.0);
    prompt = visual.TextStim(win=win, name='prompt',
        text='Which rectangle has the largest area?',
        font='Arial',
        pos=[0,0], draggable=False, height=35.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=-6.0);
    rect_choice = keyboard.Keyboard(deviceName='rect_choice')
    
    # --- Initialize components for Routine "end_block" ---
    end_block_text = visual.TextStim(win=win, name='end_block_text',
        text='You just finished a block of trials. Take a quick break. The experiment will resume in 15 seconds',
        font='Arial',
        pos=(0, 0), draggable=False, height=55.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    
    # --- Initialize components for Routine "end" ---
    end_text = visual.TextStim(win=win, name='end_text',
        text="You have completed the experiment. Press 'space' to read the debriefing screen. When you are done reading, press 'space' and let the researcher know you have finished.",
        font='Arial',
        pos=(0, 0), draggable=False, height=35.0, wrapWidth=None, ori=0.0, 
        color=[-1.0000, -1.0000, -1.0000], colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    key_resp_7 = keyboard.Keyboard(deviceName='key_resp_7')
    
    # --- Initialize components for Routine "debriefing" ---
    debrief_form = visual.ImageStim(
        win=win,
        name='debrief_form', 
        image='Judg_choice_debrief.png', mask=None, anchor='bottom-center',
        ori=0.0, pos=(0, -500), draggable=False, size=(800, 1000),
        color=[1,1,1], colorSpace='rgb', opacity=None,
        flipHoriz=False, flipVert=False,
        texRes=128.0, interpolate=True, depth=0.0)
    end_debrief = keyboard.Keyboard(deviceName='end_debrief')
    # Run 'Begin Experiment' code from log_import
    from psychopy import logging
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # --- Prepare to start Routine "consent" ---
    # create an object to store info about Routine consent
    consent = data.Routine(
        name='consent',
        components=[agree_button, decline_button, consent_img, mouse],
    )
    consent.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # reset agree_button to account for continued clicks & clear times on/off
    agree_button.reset()
    # reset decline_button to account for continued clicks & clear times on/off
    decline_button.reset()
    # setup some python lists for storing info about the mouse
    mouse.x = []
    mouse.y = []
    mouse.leftButton = []
    mouse.midButton = []
    mouse.rightButton = []
    mouse.time = []
    mouse.clicked_name = []
    gotValidClick = False  # until a click is received
    # store start times for consent
    consent.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    consent.tStart = globalClock.getTime(format='float')
    consent.status = STARTED
    thisExp.addData('consent.started', consent.tStart)
    consent.maxDuration = None
    # keep track of which components have finished
    consentComponents = consent.components
    for thisComponent in consent.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "consent" ---
    consent.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        # *agree_button* updates
        
        # if agree_button is starting this frame...
        if agree_button.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            agree_button.frameNStart = frameN  # exact frame index
            agree_button.tStart = t  # local t and not account for scr refresh
            agree_button.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(agree_button, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'agree_button.started')
            # update status
            agree_button.status = STARTED
            win.callOnFlip(agree_button.buttonClock.reset)
            agree_button.setAutoDraw(True)
        
        # if agree_button is active this frame...
        if agree_button.status == STARTED:
            # update params
            pass
            # check whether agree_button has been pressed
            if agree_button.isClicked:
                if not agree_button.wasClicked:
                    # if this is a new click, store time of first click and clicked until
                    agree_button.timesOn.append(agree_button.buttonClock.getTime())
                    agree_button.timesOff.append(agree_button.buttonClock.getTime())
                elif len(agree_button.timesOff):
                    # if click is continuing from last frame, update time of clicked until
                    agree_button.timesOff[-1] = agree_button.buttonClock.getTime()
                if not agree_button.wasClicked:
                    # end routine when agree_button is clicked
                    continueRoutine = False
                if not agree_button.wasClicked:
                    # run callback code when agree_button is clicked
                    pass
        # take note of whether agree_button was clicked, so that next frame we know if clicks are new
        agree_button.wasClicked = agree_button.isClicked and agree_button.status == STARTED
        # *decline_button* updates
        
        # if decline_button is starting this frame...
        if decline_button.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            decline_button.frameNStart = frameN  # exact frame index
            decline_button.tStart = t  # local t and not account for scr refresh
            decline_button.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(decline_button, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'decline_button.started')
            # update status
            decline_button.status = STARTED
            win.callOnFlip(decline_button.buttonClock.reset)
            decline_button.setAutoDraw(True)
        
        # if decline_button is active this frame...
        if decline_button.status == STARTED:
            # update params
            pass
            # check whether decline_button has been pressed
            if decline_button.isClicked:
                if not decline_button.wasClicked:
                    # if this is a new click, store time of first click and clicked until
                    decline_button.timesOn.append(decline_button.buttonClock.getTime())
                    decline_button.timesOff.append(decline_button.buttonClock.getTime())
                elif len(decline_button.timesOff):
                    # if click is continuing from last frame, update time of clicked until
                    decline_button.timesOff[-1] = decline_button.buttonClock.getTime()
                if not decline_button.wasClicked:
                    # end routine when decline_button is clicked
                    continueRoutine = False
                if not decline_button.wasClicked:
                    # run callback code when decline_button is clicked
                    pass
        # take note of whether decline_button was clicked, so that next frame we know if clicks are new
        decline_button.wasClicked = decline_button.isClicked and decline_button.status == STARTED
        
        # *consent_img* updates
        
        # if consent_img is starting this frame...
        if consent_img.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            consent_img.frameNStart = frameN  # exact frame index
            consent_img.tStart = t  # local t and not account for scr refresh
            consent_img.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(consent_img, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'consent_img.started')
            # update status
            consent_img.status = STARTED
            consent_img.setAutoDraw(True)
        
        # if consent_img is active this frame...
        if consent_img.status == STARTED:
            # update params
            pass
        # *mouse* updates
        
        # if mouse is starting this frame...
        if mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            mouse.frameNStart = frameN  # exact frame index
            mouse.tStart = t  # local t and not account for scr refresh
            mouse.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(mouse, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.addData('mouse.started', t)
            # update status
            mouse.status = STARTED
            mouse.mouseClock.reset()
            prevButtonState = mouse.getPressed()  # if button is down already this ISN'T a new click
        if mouse.status == STARTED:  # only update if started and not finished!
            buttons = mouse.getPressed()
            if buttons != prevButtonState:  # button state changed?
                prevButtonState = buttons
                if sum(buttons) > 0:  # state changed to a new click
                    # check if the mouse was inside our 'clickable' objects
                    gotValidClick = False
                    clickableList = environmenttools.getFromNames([agree_button, decline_button], namespace=locals())
                    for obj in clickableList:
                        # is this object clicked on?
                        if obj.contains(mouse):
                            gotValidClick = True
                            mouse.clicked_name.append(obj.name)
                    if not gotValidClick:
                        mouse.clicked_name.append(None)
                    x, y = mouse.getPos()
                    mouse.x.append(x)
                    mouse.y.append(y)
                    buttons = mouse.getPressed()
                    mouse.leftButton.append(buttons[0])
                    mouse.midButton.append(buttons[1])
                    mouse.rightButton.append(buttons[2])
                    mouse.time.append(mouse.mouseClock.getTime())
                    if gotValidClick:
                        continueRoutine = False  # end routine on response
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            consent.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in consent.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "consent" ---
    for thisComponent in consent.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for consent
    consent.tStop = globalClock.getTime(format='float')
    consent.tStopRefresh = tThisFlipGlobal
    thisExp.addData('consent.stopped', consent.tStop)
    thisExp.addData('agree_button.numClicks', agree_button.numClicks)
    if agree_button.numClicks:
       thisExp.addData('agree_button.timesOn', agree_button.timesOn)
       thisExp.addData('agree_button.timesOff', agree_button.timesOff)
    else:
       thisExp.addData('agree_button.timesOn', "")
       thisExp.addData('agree_button.timesOff', "")
    thisExp.addData('decline_button.numClicks', decline_button.numClicks)
    if decline_button.numClicks:
       thisExp.addData('decline_button.timesOn', decline_button.timesOn)
       thisExp.addData('decline_button.timesOff', decline_button.timesOff)
    else:
       thisExp.addData('decline_button.timesOn', "")
       thisExp.addData('decline_button.timesOff', "")
    # Run 'End Routine' code from check_consent
    if decline_button.numClicks==1:
        core.quit()
    # store data for thisExp (ExperimentHandler)
    thisExp.addData('mouse.x', mouse.x)
    thisExp.addData('mouse.y', mouse.y)
    thisExp.addData('mouse.leftButton', mouse.leftButton)
    thisExp.addData('mouse.midButton', mouse.midButton)
    thisExp.addData('mouse.rightButton', mouse.rightButton)
    thisExp.addData('mouse.time', mouse.time)
    thisExp.addData('mouse.clicked_name', mouse.clicked_name)
    thisExp.nextEntry()
    # the Routine "consent" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "exp_params" ---
    # create an object to store info about Routine exp_params
    exp_params = data.Routine(
        name='exp_params',
        components=[],
    )
    exp_params.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for exp_params
    exp_params.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    exp_params.tStart = globalClock.getTime(format='float')
    exp_params.status = STARTED
    thisExp.addData('exp_params.started', exp_params.tStart)
    exp_params.maxDuration = None
    # keep track of which components have finished
    exp_paramsComponents = exp_params.components
    for thisComponent in exp_params.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "exp_params" ---
    exp_params.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            exp_params.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in exp_params.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "exp_params" ---
    for thisComponent in exp_params.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for exp_params
    exp_params.tStop = globalClock.getTime(format='float')
    exp_params.tStopRefresh = tThisFlipGlobal
    thisExp.addData('exp_params.stopped', exp_params.tStop)
    thisExp.nextEntry()
    # the Routine "exp_params" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "welcome" ---
    # create an object to store info about Routine welcome
    welcome = data.Routine(
        name='welcome',
        components=[welcome_text],
    )
    welcome.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # store start times for welcome
    welcome.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    welcome.tStart = globalClock.getTime(format='float')
    welcome.status = STARTED
    thisExp.addData('welcome.started', welcome.tStart)
    welcome.maxDuration = None
    # keep track of which components have finished
    welcomeComponents = welcome.components
    for thisComponent in welcome.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "welcome" ---
    welcome.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine and routineTimer.getTime() < 2.0:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *welcome_text* updates
        
        # if welcome_text is starting this frame...
        if welcome_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            welcome_text.frameNStart = frameN  # exact frame index
            welcome_text.tStart = t  # local t and not account for scr refresh
            welcome_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(welcome_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'welcome_text.started')
            # update status
            welcome_text.status = STARTED
            welcome_text.setAutoDraw(True)
        
        # if welcome_text is active this frame...
        if welcome_text.status == STARTED:
            # update params
            pass
        
        # if welcome_text is stopping this frame...
        if welcome_text.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > welcome_text.tStartRefresh + 2-frameTolerance:
                # keep track of stop time/frame for later
                welcome_text.tStop = t  # not accounting for scr refresh
                welcome_text.tStopRefresh = tThisFlipGlobal  # on global time
                welcome_text.frameNStop = frameN  # exact frame index
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'welcome_text.stopped')
                # update status
                welcome_text.status = FINISHED
                welcome_text.setAutoDraw(False)
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            welcome.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in welcome.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "welcome" ---
    for thisComponent in welcome.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for welcome
    welcome.tStop = globalClock.getTime(format='float')
    welcome.tStopRefresh = tThisFlipGlobal
    thisExp.addData('welcome.stopped', welcome.tStop)
    # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
    if welcome.maxDurationReached:
        routineTimer.addTime(-welcome.maxDuration)
    elif welcome.forceEnded:
        routineTimer.reset()
    else:
        routineTimer.addTime(-2.000000)
    thisExp.nextEntry()
    
    # set up handler to look after randomisation of conditions etc
    instructions_loop = data.TrialHandler2(
        name='instructions_loop',
        nReps=1.0, 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=[None], 
        seed=None, 
    )
    thisExp.addLoop(instructions_loop)  # add the loop to the experiment
    thisInstructions_loop = instructions_loop.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisInstructions_loop.rgb)
    if thisInstructions_loop != None:
        for paramName in thisInstructions_loop:
            globals()[paramName] = thisInstructions_loop[paramName]
    
    for thisInstructions_loop in instructions_loop:
        currentLoop = instructions_loop
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        # abbreviate parameter names if possible (e.g. rgb = thisInstructions_loop.rgb)
        if thisInstructions_loop != None:
            for paramName in thisInstructions_loop:
                globals()[paramName] = thisInstructions_loop[paramName]
        
        # --- Prepare to start Routine "instructions_1" ---
        # create an object to store info about Routine instructions_1
        instructions_1 = data.Routine(
            name='instructions_1',
            components=[instructions_1_text_1, instructions_1_text_2, key_resp],
        )
        instructions_1.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # create starting attributes for key_resp
        key_resp.keys = []
        key_resp.rt = []
        _key_resp_allKeys = []
        # store start times for instructions_1
        instructions_1.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        instructions_1.tStart = globalClock.getTime(format='float')
        instructions_1.status = STARTED
        thisExp.addData('instructions_1.started', instructions_1.tStart)
        instructions_1.maxDuration = None
        # keep track of which components have finished
        instructions_1Components = instructions_1.components
        for thisComponent in instructions_1.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "instructions_1" ---
        # if trial has changed, end Routine now
        if isinstance(instructions_loop, data.TrialHandler2) and thisInstructions_loop.thisN != instructions_loop.thisTrial.thisN:
            continueRoutine = False
        instructions_1.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *instructions_1_text_1* updates
            
            # if instructions_1_text_1 is starting this frame...
            if instructions_1_text_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instructions_1_text_1.frameNStart = frameN  # exact frame index
                instructions_1_text_1.tStart = t  # local t and not account for scr refresh
                instructions_1_text_1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instructions_1_text_1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instructions_1_text_1.started')
                # update status
                instructions_1_text_1.status = STARTED
                instructions_1_text_1.setAutoDraw(True)
            
            # if instructions_1_text_1 is active this frame...
            if instructions_1_text_1.status == STARTED:
                # update params
                pass
            
            # *instructions_1_text_2* updates
            
            # if instructions_1_text_2 is starting this frame...
            if instructions_1_text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instructions_1_text_2.frameNStart = frameN  # exact frame index
                instructions_1_text_2.tStart = t  # local t and not account for scr refresh
                instructions_1_text_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instructions_1_text_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instructions_1_text_2.started')
                # update status
                instructions_1_text_2.status = STARTED
                instructions_1_text_2.setAutoDraw(True)
            
            # if instructions_1_text_2 is active this frame...
            if instructions_1_text_2.status == STARTED:
                # update params
                pass
            
            # *key_resp* updates
            waitOnFlip = False
            
            # if key_resp is starting this frame...
            if key_resp.status == NOT_STARTED and tThisFlip >= 1.5-frameTolerance:
                # keep track of start time/frame for later
                key_resp.frameNStart = frameN  # exact frame index
                key_resp.tStart = t  # local t and not account for scr refresh
                key_resp.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp.started')
                # update status
                key_resp.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp.status == STARTED and not waitOnFlip:
                theseKeys = key_resp.getKeys(keyList=['space'], ignoreKeys=None, waitRelease=False)
                _key_resp_allKeys.extend(theseKeys)
                if len(_key_resp_allKeys):
                    key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
                    key_resp.rt = _key_resp_allKeys[-1].rt
                    key_resp.duration = _key_resp_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                instructions_1.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in instructions_1.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "instructions_1" ---
        for thisComponent in instructions_1.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for instructions_1
        instructions_1.tStop = globalClock.getTime(format='float')
        instructions_1.tStopRefresh = tThisFlipGlobal
        thisExp.addData('instructions_1.stopped', instructions_1.tStop)
        # check responses
        if key_resp.keys in ['', [], None]:  # No response was made
            key_resp.keys = None
        instructions_loop.addData('key_resp.keys',key_resp.keys)
        if key_resp.keys != None:  # we had a response
            instructions_loop.addData('key_resp.rt', key_resp.rt)
            instructions_loop.addData('key_resp.duration', key_resp.duration)
        # the Routine "instructions_1" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "instructions_2" ---
        # create an object to store info about Routine instructions_2
        instructions_2 = data.Routine(
            name='instructions_2',
            components=[instructions_2_text_1, instructions_2_text_2, key_resp_2],
        )
        instructions_2.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # create starting attributes for key_resp_2
        key_resp_2.keys = []
        key_resp_2.rt = []
        _key_resp_2_allKeys = []
        # store start times for instructions_2
        instructions_2.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        instructions_2.tStart = globalClock.getTime(format='float')
        instructions_2.status = STARTED
        thisExp.addData('instructions_2.started', instructions_2.tStart)
        instructions_2.maxDuration = None
        # keep track of which components have finished
        instructions_2Components = instructions_2.components
        for thisComponent in instructions_2.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "instructions_2" ---
        # if trial has changed, end Routine now
        if isinstance(instructions_loop, data.TrialHandler2) and thisInstructions_loop.thisN != instructions_loop.thisTrial.thisN:
            continueRoutine = False
        instructions_2.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *instructions_2_text_1* updates
            
            # if instructions_2_text_1 is starting this frame...
            if instructions_2_text_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instructions_2_text_1.frameNStart = frameN  # exact frame index
                instructions_2_text_1.tStart = t  # local t and not account for scr refresh
                instructions_2_text_1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instructions_2_text_1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instructions_2_text_1.started')
                # update status
                instructions_2_text_1.status = STARTED
                instructions_2_text_1.setAutoDraw(True)
            
            # if instructions_2_text_1 is active this frame...
            if instructions_2_text_1.status == STARTED:
                # update params
                pass
            
            # *instructions_2_text_2* updates
            
            # if instructions_2_text_2 is starting this frame...
            if instructions_2_text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instructions_2_text_2.frameNStart = frameN  # exact frame index
                instructions_2_text_2.tStart = t  # local t and not account for scr refresh
                instructions_2_text_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instructions_2_text_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instructions_2_text_2.started')
                # update status
                instructions_2_text_2.status = STARTED
                instructions_2_text_2.setAutoDraw(True)
            
            # if instructions_2_text_2 is active this frame...
            if instructions_2_text_2.status == STARTED:
                # update params
                pass
            
            # *key_resp_2* updates
            waitOnFlip = False
            
            # if key_resp_2 is starting this frame...
            if key_resp_2.status == NOT_STARTED and tThisFlip >= 1.5-frameTolerance:
                # keep track of start time/frame for later
                key_resp_2.frameNStart = frameN  # exact frame index
                key_resp_2.tStart = t  # local t and not account for scr refresh
                key_resp_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp_2.started')
                # update status
                key_resp_2.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp_2.status == STARTED and not waitOnFlip:
                theseKeys = key_resp_2.getKeys(keyList=['space'], ignoreKeys=None, waitRelease=False)
                _key_resp_2_allKeys.extend(theseKeys)
                if len(_key_resp_2_allKeys):
                    key_resp_2.keys = _key_resp_2_allKeys[-1].name  # just the last key pressed
                    key_resp_2.rt = _key_resp_2_allKeys[-1].rt
                    key_resp_2.duration = _key_resp_2_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                instructions_2.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in instructions_2.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "instructions_2" ---
        for thisComponent in instructions_2.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for instructions_2
        instructions_2.tStop = globalClock.getTime(format='float')
        instructions_2.tStopRefresh = tThisFlipGlobal
        thisExp.addData('instructions_2.stopped', instructions_2.tStop)
        # check responses
        if key_resp_2.keys in ['', [], None]:  # No response was made
            key_resp_2.keys = None
        instructions_loop.addData('key_resp_2.keys',key_resp_2.keys)
        if key_resp_2.keys != None:  # we had a response
            instructions_loop.addData('key_resp_2.rt', key_resp_2.rt)
            instructions_loop.addData('key_resp_2.duration', key_resp_2.duration)
        # the Routine "instructions_2" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "instructions_3" ---
        # create an object to store info about Routine instructions_3
        instructions_3 = data.Routine(
            name='instructions_3',
            components=[instructions_3_text_1, r1_instr3, r2_instr3, r3_instr3, r1_instr3_label, r2_instr3_label, r3_instr3_label, instructions_3_text_3, key_resp_3, instructions_3_text_4],
        )
        instructions_3.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # create starting attributes for key_resp_3
        key_resp_3.keys = []
        key_resp_3.rt = []
        _key_resp_3_allKeys = []
        # store start times for instructions_3
        instructions_3.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        instructions_3.tStart = globalClock.getTime(format='float')
        instructions_3.status = STARTED
        thisExp.addData('instructions_3.started', instructions_3.tStart)
        instructions_3.maxDuration = None
        # keep track of which components have finished
        instructions_3Components = instructions_3.components
        for thisComponent in instructions_3.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "instructions_3" ---
        # if trial has changed, end Routine now
        if isinstance(instructions_loop, data.TrialHandler2) and thisInstructions_loop.thisN != instructions_loop.thisTrial.thisN:
            continueRoutine = False
        instructions_3.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *instructions_3_text_1* updates
            
            # if instructions_3_text_1 is starting this frame...
            if instructions_3_text_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instructions_3_text_1.frameNStart = frameN  # exact frame index
                instructions_3_text_1.tStart = t  # local t and not account for scr refresh
                instructions_3_text_1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instructions_3_text_1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instructions_3_text_1.started')
                # update status
                instructions_3_text_1.status = STARTED
                instructions_3_text_1.setAutoDraw(True)
            
            # if instructions_3_text_1 is active this frame...
            if instructions_3_text_1.status == STARTED:
                # update params
                pass
            
            # *r1_instr3* updates
            
            # if r1_instr3 is starting this frame...
            if r1_instr3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                r1_instr3.frameNStart = frameN  # exact frame index
                r1_instr3.tStart = t  # local t and not account for scr refresh
                r1_instr3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(r1_instr3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'r1_instr3.started')
                # update status
                r1_instr3.status = STARTED
                r1_instr3.setAutoDraw(True)
            
            # if r1_instr3 is active this frame...
            if r1_instr3.status == STARTED:
                # update params
                pass
            
            # *r2_instr3* updates
            
            # if r2_instr3 is starting this frame...
            if r2_instr3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                r2_instr3.frameNStart = frameN  # exact frame index
                r2_instr3.tStart = t  # local t and not account for scr refresh
                r2_instr3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(r2_instr3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'r2_instr3.started')
                # update status
                r2_instr3.status = STARTED
                r2_instr3.setAutoDraw(True)
            
            # if r2_instr3 is active this frame...
            if r2_instr3.status == STARTED:
                # update params
                pass
            
            # *r3_instr3* updates
            
            # if r3_instr3 is starting this frame...
            if r3_instr3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                r3_instr3.frameNStart = frameN  # exact frame index
                r3_instr3.tStart = t  # local t and not account for scr refresh
                r3_instr3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(r3_instr3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'r3_instr3.started')
                # update status
                r3_instr3.status = STARTED
                r3_instr3.setAutoDraw(True)
            
            # if r3_instr3 is active this frame...
            if r3_instr3.status == STARTED:
                # update params
                pass
            
            # *r1_instr3_label* updates
            
            # if r1_instr3_label is starting this frame...
            if r1_instr3_label.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                r1_instr3_label.frameNStart = frameN  # exact frame index
                r1_instr3_label.tStart = t  # local t and not account for scr refresh
                r1_instr3_label.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(r1_instr3_label, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'r1_instr3_label.started')
                # update status
                r1_instr3_label.status = STARTED
                r1_instr3_label.setAutoDraw(True)
            
            # if r1_instr3_label is active this frame...
            if r1_instr3_label.status == STARTED:
                # update params
                pass
            
            # *r2_instr3_label* updates
            
            # if r2_instr3_label is starting this frame...
            if r2_instr3_label.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                r2_instr3_label.frameNStart = frameN  # exact frame index
                r2_instr3_label.tStart = t  # local t and not account for scr refresh
                r2_instr3_label.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(r2_instr3_label, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'r2_instr3_label.started')
                # update status
                r2_instr3_label.status = STARTED
                r2_instr3_label.setAutoDraw(True)
            
            # if r2_instr3_label is active this frame...
            if r2_instr3_label.status == STARTED:
                # update params
                pass
            
            # *r3_instr3_label* updates
            
            # if r3_instr3_label is starting this frame...
            if r3_instr3_label.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                r3_instr3_label.frameNStart = frameN  # exact frame index
                r3_instr3_label.tStart = t  # local t and not account for scr refresh
                r3_instr3_label.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(r3_instr3_label, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'r3_instr3_label.started')
                # update status
                r3_instr3_label.status = STARTED
                r3_instr3_label.setAutoDraw(True)
            
            # if r3_instr3_label is active this frame...
            if r3_instr3_label.status == STARTED:
                # update params
                pass
            
            # *instructions_3_text_3* updates
            
            # if instructions_3_text_3 is starting this frame...
            if instructions_3_text_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instructions_3_text_3.frameNStart = frameN  # exact frame index
                instructions_3_text_3.tStart = t  # local t and not account for scr refresh
                instructions_3_text_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instructions_3_text_3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instructions_3_text_3.started')
                # update status
                instructions_3_text_3.status = STARTED
                instructions_3_text_3.setAutoDraw(True)
            
            # if instructions_3_text_3 is active this frame...
            if instructions_3_text_3.status == STARTED:
                # update params
                pass
            
            # *key_resp_3* updates
            waitOnFlip = False
            
            # if key_resp_3 is starting this frame...
            if key_resp_3.status == NOT_STARTED and tThisFlip >= 1.5-frameTolerance:
                # keep track of start time/frame for later
                key_resp_3.frameNStart = frameN  # exact frame index
                key_resp_3.tStart = t  # local t and not account for scr refresh
                key_resp_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp_3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp_3.started')
                # update status
                key_resp_3.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp_3.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp_3.status == STARTED and not waitOnFlip:
                theseKeys = key_resp_3.getKeys(keyList=['space'], ignoreKeys=None, waitRelease=False)
                _key_resp_3_allKeys.extend(theseKeys)
                if len(_key_resp_3_allKeys):
                    key_resp_3.keys = _key_resp_3_allKeys[-1].name  # just the last key pressed
                    key_resp_3.rt = _key_resp_3_allKeys[-1].rt
                    key_resp_3.duration = _key_resp_3_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            
            # *instructions_3_text_4* updates
            
            # if instructions_3_text_4 is starting this frame...
            if instructions_3_text_4.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instructions_3_text_4.frameNStart = frameN  # exact frame index
                instructions_3_text_4.tStart = t  # local t and not account for scr refresh
                instructions_3_text_4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instructions_3_text_4, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instructions_3_text_4.started')
                # update status
                instructions_3_text_4.status = STARTED
                instructions_3_text_4.setAutoDraw(True)
            
            # if instructions_3_text_4 is active this frame...
            if instructions_3_text_4.status == STARTED:
                # update params
                pass
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                instructions_3.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in instructions_3.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "instructions_3" ---
        for thisComponent in instructions_3.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for instructions_3
        instructions_3.tStop = globalClock.getTime(format='float')
        instructions_3.tStopRefresh = tThisFlipGlobal
        thisExp.addData('instructions_3.stopped', instructions_3.tStop)
        # check responses
        if key_resp_3.keys in ['', [], None]:  # No response was made
            key_resp_3.keys = None
        instructions_loop.addData('key_resp_3.keys',key_resp_3.keys)
        if key_resp_3.keys != None:  # we had a response
            instructions_loop.addData('key_resp_3.rt', key_resp_3.rt)
            instructions_loop.addData('key_resp_3.duration', key_resp_3.duration)
        # the Routine "instructions_3" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "instructions_4" ---
        # create an object to store info about Routine instructions_4
        instructions_4 = data.Routine(
            name='instructions_4',
            components=[instructions_4_text_1, instructions_4_text_3, instructions_4_text_2, key_resp_4],
        )
        instructions_4.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # create starting attributes for key_resp_4
        key_resp_4.keys = []
        key_resp_4.rt = []
        _key_resp_4_allKeys = []
        # store start times for instructions_4
        instructions_4.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        instructions_4.tStart = globalClock.getTime(format='float')
        instructions_4.status = STARTED
        thisExp.addData('instructions_4.started', instructions_4.tStart)
        instructions_4.maxDuration = None
        # keep track of which components have finished
        instructions_4Components = instructions_4.components
        for thisComponent in instructions_4.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "instructions_4" ---
        # if trial has changed, end Routine now
        if isinstance(instructions_loop, data.TrialHandler2) and thisInstructions_loop.thisN != instructions_loop.thisTrial.thisN:
            continueRoutine = False
        instructions_4.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *instructions_4_text_1* updates
            
            # if instructions_4_text_1 is starting this frame...
            if instructions_4_text_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instructions_4_text_1.frameNStart = frameN  # exact frame index
                instructions_4_text_1.tStart = t  # local t and not account for scr refresh
                instructions_4_text_1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instructions_4_text_1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instructions_4_text_1.started')
                # update status
                instructions_4_text_1.status = STARTED
                instructions_4_text_1.setAutoDraw(True)
            
            # if instructions_4_text_1 is active this frame...
            if instructions_4_text_1.status == STARTED:
                # update params
                pass
            
            # *instructions_4_text_3* updates
            
            # if instructions_4_text_3 is starting this frame...
            if instructions_4_text_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instructions_4_text_3.frameNStart = frameN  # exact frame index
                instructions_4_text_3.tStart = t  # local t and not account for scr refresh
                instructions_4_text_3.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instructions_4_text_3, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instructions_4_text_3.started')
                # update status
                instructions_4_text_3.status = STARTED
                instructions_4_text_3.setAutoDraw(True)
            
            # if instructions_4_text_3 is active this frame...
            if instructions_4_text_3.status == STARTED:
                # update params
                pass
            
            # *instructions_4_text_2* updates
            
            # if instructions_4_text_2 is starting this frame...
            if instructions_4_text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instructions_4_text_2.frameNStart = frameN  # exact frame index
                instructions_4_text_2.tStart = t  # local t and not account for scr refresh
                instructions_4_text_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instructions_4_text_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instructions_4_text_2.started')
                # update status
                instructions_4_text_2.status = STARTED
                instructions_4_text_2.setAutoDraw(True)
            
            # if instructions_4_text_2 is active this frame...
            if instructions_4_text_2.status == STARTED:
                # update params
                pass
            
            # *key_resp_4* updates
            waitOnFlip = False
            
            # if key_resp_4 is starting this frame...
            if key_resp_4.status == NOT_STARTED and tThisFlip >= 1.5-frameTolerance:
                # keep track of start time/frame for later
                key_resp_4.frameNStart = frameN  # exact frame index
                key_resp_4.tStart = t  # local t and not account for scr refresh
                key_resp_4.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp_4, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp_4.started')
                # update status
                key_resp_4.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp_4.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp_4.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp_4.status == STARTED and not waitOnFlip:
                theseKeys = key_resp_4.getKeys(keyList=['space'], ignoreKeys=None, waitRelease=False)
                _key_resp_4_allKeys.extend(theseKeys)
                if len(_key_resp_4_allKeys):
                    key_resp_4.keys = _key_resp_4_allKeys[-1].name  # just the last key pressed
                    key_resp_4.rt = _key_resp_4_allKeys[-1].rt
                    key_resp_4.duration = _key_resp_4_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                instructions_4.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in instructions_4.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "instructions_4" ---
        for thisComponent in instructions_4.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for instructions_4
        instructions_4.tStop = globalClock.getTime(format='float')
        instructions_4.tStopRefresh = tThisFlipGlobal
        thisExp.addData('instructions_4.stopped', instructions_4.tStop)
        # check responses
        if key_resp_4.keys in ['', [], None]:  # No response was made
            key_resp_4.keys = None
        instructions_loop.addData('key_resp_4.keys',key_resp_4.keys)
        if key_resp_4.keys != None:  # we had a response
            instructions_loop.addData('key_resp_4.rt', key_resp_4.rt)
            instructions_loop.addData('key_resp_4.duration', key_resp_4.duration)
        # the Routine "instructions_4" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "instructions_5" ---
        # create an object to store info about Routine instructions_5
        instructions_5 = data.Routine(
            name='instructions_5',
            components=[instructions_5_text_1, instructions_5_text_2, key_resp_5],
        )
        instructions_5.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # create starting attributes for key_resp_5
        key_resp_5.keys = []
        key_resp_5.rt = []
        _key_resp_5_allKeys = []
        # store start times for instructions_5
        instructions_5.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        instructions_5.tStart = globalClock.getTime(format='float')
        instructions_5.status = STARTED
        thisExp.addData('instructions_5.started', instructions_5.tStart)
        instructions_5.maxDuration = None
        # keep track of which components have finished
        instructions_5Components = instructions_5.components
        for thisComponent in instructions_5.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "instructions_5" ---
        # if trial has changed, end Routine now
        if isinstance(instructions_loop, data.TrialHandler2) and thisInstructions_loop.thisN != instructions_loop.thisTrial.thisN:
            continueRoutine = False
        instructions_5.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *instructions_5_text_1* updates
            
            # if instructions_5_text_1 is starting this frame...
            if instructions_5_text_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instructions_5_text_1.frameNStart = frameN  # exact frame index
                instructions_5_text_1.tStart = t  # local t and not account for scr refresh
                instructions_5_text_1.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instructions_5_text_1, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instructions_5_text_1.started')
                # update status
                instructions_5_text_1.status = STARTED
                instructions_5_text_1.setAutoDraw(True)
            
            # if instructions_5_text_1 is active this frame...
            if instructions_5_text_1.status == STARTED:
                # update params
                pass
            
            # *instructions_5_text_2* updates
            
            # if instructions_5_text_2 is starting this frame...
            if instructions_5_text_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                instructions_5_text_2.frameNStart = frameN  # exact frame index
                instructions_5_text_2.tStart = t  # local t and not account for scr refresh
                instructions_5_text_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(instructions_5_text_2, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'instructions_5_text_2.started')
                # update status
                instructions_5_text_2.status = STARTED
                instructions_5_text_2.setAutoDraw(True)
            
            # if instructions_5_text_2 is active this frame...
            if instructions_5_text_2.status == STARTED:
                # update params
                pass
            
            # *key_resp_5* updates
            waitOnFlip = False
            
            # if key_resp_5 is starting this frame...
            if key_resp_5.status == NOT_STARTED and tThisFlip >= 1.5-frameTolerance:
                # keep track of start time/frame for later
                key_resp_5.frameNStart = frameN  # exact frame index
                key_resp_5.tStart = t  # local t and not account for scr refresh
                key_resp_5.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(key_resp_5, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'key_resp_5.started')
                # update status
                key_resp_5.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(key_resp_5.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(key_resp_5.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if key_resp_5.status == STARTED and not waitOnFlip:
                theseKeys = key_resp_5.getKeys(keyList=['space'], ignoreKeys=None, waitRelease=False)
                _key_resp_5_allKeys.extend(theseKeys)
                if len(_key_resp_5_allKeys):
                    key_resp_5.keys = _key_resp_5_allKeys[-1].name  # just the last key pressed
                    key_resp_5.rt = _key_resp_5_allKeys[-1].rt
                    key_resp_5.duration = _key_resp_5_allKeys[-1].duration
                    # a response ends the routine
                    continueRoutine = False
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                instructions_5.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in instructions_5.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "instructions_5" ---
        for thisComponent in instructions_5.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for instructions_5
        instructions_5.tStop = globalClock.getTime(format='float')
        instructions_5.tStopRefresh = tThisFlipGlobal
        thisExp.addData('instructions_5.stopped', instructions_5.tStop)
        # check responses
        if key_resp_5.keys in ['', [], None]:  # No response was made
            key_resp_5.keys = None
        instructions_loop.addData('key_resp_5.keys',key_resp_5.keys)
        if key_resp_5.keys != None:  # we had a response
            instructions_loop.addData('key_resp_5.rt', key_resp_5.rt)
            instructions_loop.addData('key_resp_5.duration', key_resp_5.duration)
        # the Routine "instructions_5" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
    # completed 1.0 repeats of 'instructions_loop'
    
    
    # --- Prepare to start Routine "start_exp" ---
    # create an object to store info about Routine start_exp
    start_exp = data.Routine(
        name='start_exp',
        components=[start_exp_text, key_resp_6],
    )
    start_exp.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_resp_6
    key_resp_6.keys = []
    key_resp_6.rt = []
    _key_resp_6_allKeys = []
    # store start times for start_exp
    start_exp.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    start_exp.tStart = globalClock.getTime(format='float')
    start_exp.status = STARTED
    thisExp.addData('start_exp.started', start_exp.tStart)
    start_exp.maxDuration = None
    # keep track of which components have finished
    start_expComponents = start_exp.components
    for thisComponent in start_exp.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "start_exp" ---
    start_exp.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *start_exp_text* updates
        
        # if start_exp_text is starting this frame...
        if start_exp_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            start_exp_text.frameNStart = frameN  # exact frame index
            start_exp_text.tStart = t  # local t and not account for scr refresh
            start_exp_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(start_exp_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'start_exp_text.started')
            # update status
            start_exp_text.status = STARTED
            start_exp_text.setAutoDraw(True)
        
        # if start_exp_text is active this frame...
        if start_exp_text.status == STARTED:
            # update params
            pass
        
        # *key_resp_6* updates
        waitOnFlip = False
        
        # if key_resp_6 is starting this frame...
        if key_resp_6.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_6.frameNStart = frameN  # exact frame index
            key_resp_6.tStart = t  # local t and not account for scr refresh
            key_resp_6.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_6, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_6.started')
            # update status
            key_resp_6.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_6.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_6.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_6.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_6.getKeys(keyList=['space'], ignoreKeys=None, waitRelease=False)
            _key_resp_6_allKeys.extend(theseKeys)
            if len(_key_resp_6_allKeys):
                key_resp_6.keys = _key_resp_6_allKeys[-1].name  # just the last key pressed
                key_resp_6.rt = _key_resp_6_allKeys[-1].rt
                key_resp_6.duration = _key_resp_6_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            start_exp.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in start_exp.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "start_exp" ---
    for thisComponent in start_exp.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for start_exp
    start_exp.tStop = globalClock.getTime(format='float')
    start_exp.tStopRefresh = tThisFlipGlobal
    thisExp.addData('start_exp.stopped', start_exp.tStop)
    # check responses
    if key_resp_6.keys in ['', [], None]:  # No response was made
        key_resp_6.keys = None
    thisExp.addData('key_resp_6.keys',key_resp_6.keys)
    if key_resp_6.keys != None:  # we had a response
        thisExp.addData('key_resp_6.rt', key_resp_6.rt)
        thisExp.addData('key_resp_6.duration', key_resp_6.duration)
    thisExp.nextEntry()
    # the Routine "start_exp" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # set up handler to look after randomisation of conditions etc
    blocks = data.TrialHandler2(
        name='blocks',
        nReps=4.0, 
        method='sequential', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=[None], 
        seed=None, 
    )
    thisExp.addLoop(blocks)  # add the loop to the experiment
    thisBlock = blocks.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
    if thisBlock != None:
        for paramName in thisBlock:
            globals()[paramName] = thisBlock[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisBlock in blocks:
        currentLoop = blocks
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisBlock.rgb)
        if thisBlock != None:
            for paramName in thisBlock:
                globals()[paramName] = thisBlock[paramName]
        
        # set up handler to look after randomisation of conditions etc
        trials = data.TrialHandler2(
            name='trials',
            nReps=1.0, 
            method='random', 
            extraInfo=expInfo, 
            originPath=-1, 
            trialList=data.importConditions('trials.csv'), 
            seed=None, 
        )
        thisExp.addLoop(trials)  # add the loop to the experiment
        thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                globals()[paramName] = thisTrial[paramName]
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        for thisTrial in trials:
            currentLoop = trials
            thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
            if thisSession is not None:
                # if running in a Session with a Liaison client, send data up to now
                thisSession.sendExperimentData()
            # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
            if thisTrial != None:
                for paramName in thisTrial:
                    globals()[paramName] = thisTrial[paramName]
            
            # --- Prepare to start Routine "pre_trial" ---
            # create an object to store info about Routine pre_trial
            pre_trial = data.Routine(
                name='pre_trial',
                components=[],
            )
            pre_trial.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            # Run 'Begin Routine' code from rect_dims
            # rectangle dimensions depending on effect (trial type)
            # 4 possible options:
            # critical - experimental trials - predefined dimension values
            # filler random - randomly sample 3 stimuli anywhere in stimulus space
            # filler square - randomly sample 1 square and 2 smaller rectangles
            # catch - randomly sample 1 stimulus from upper diagonal and 2 from lower diagonals
            
            if effect=="critical":
                h_1_tmp=h_1
                w_1_tmp=w_1
                h_2_tmp=h_2
                w_2_tmp=w_2
                h_3_tmp=h_3
                w_3_tmp=w_3
            elif effect=="filler_random":
                h_1_tmp=np.random.uniform(dim_min,dim_max,1)[0]
                w_1_tmp=np.random.uniform(dim_min,dim_max,1)[0]
                h_2_tmp=np.random.uniform(dim_min,dim_max,1)[0]
                w_2_tmp=np.random.uniform(dim_min,dim_max,1)[0]
                h_3_tmp=np.random.uniform(dim_min,dim_max,1)[0]
                w_3_tmp=np.random.uniform(dim_min,dim_max,1)[0]
            elif effect=="filler_square":
                # have to randomly select where the square goes
                which_large=np.random.choice(np.arange(3))
                
                # randomly sample square and then sample other rectangles from U[dim_min, square size]
                if which_large==0:
                    h_1_tmp=np.random.uniform(dim_min, dim_max,1)[0]
                    w_1_tmp=h_1_tmp
                    h_2_tmp=np.random.uniform(dim_min,h_1_tmp,1)[0]
                    w_2_tmp=np.random.uniform(dim_min,h_1_tmp,1)[0]
                    h_3_tmp=np.random.uniform(dim_min,h_1_tmp,1)[0]
                    w_3_tmp=np.random.uniform(dim_min,h_1_tmp,1)[0]
                elif which_large==1:
                    h_2_tmp=np.random.uniform(dim_min, dim_max,1)[0]
                    w_2_tmp=h_2_tmp
                    h_1_tmp=np.random.uniform(dim_min,h_2_tmp,1)[0]
                    w_1_tmp=np.random.uniform(dim_min,h_2_tmp,1)[0]
                    h_3_tmp=np.random.uniform(dim_min,h_2_tmp,1)[0]
                    w_3_tmp=np.random.uniform(dim_min,h_2_tmp,1)[0]
                elif which_large==2:
                    h_3_tmp=np.random.uniform(dim_min, dim_max,1)[0]
                    w_3_tmp=h_3_tmp
                    h_1_tmp=np.random.uniform(dim_min,h_3_tmp,1)[0]
                    w_1_tmp=np.random.uniform(dim_min,h_3_tmp,1)[0]
                    h_2_tmp=np.random.uniform(dim_min,h_3_tmp,1)[0]
                    w_2_tmp=np.random.uniform(dim_min,h_3_tmp,1)[0]
            elif effect=="catch":
                # randomly sample a stimulus from upper and lower diagonals
                u_1=sample_diag(d2_r, d2_int)
                l_1=sample_diag(d1_r, d1_int)
                l_2=sample_diag(d1_r, d1_int)
                
                # then randomly assign position of upper
                # other 2 positions don't matter
                which_upper=np.random.choice(np.arange(3))
                if which_upper==0:
                    w_1_tmp=u_1[0]
                    h_1_tmp=u_1[1]
                    w_2_tmp=l_1[0]
                    h_2_tmp=l_1[1]
                    w_3_tmp=l_2[0]
                    h_3_tmp=l_2[1]
                elif which_upper==1:
                    w_1_tmp=l_1[0]
                    h_1_tmp=l_1[1]
                    w_2_tmp=u_1[0]
                    h_2_tmp=u_1[1]
                    w_3_tmp=l_2[0]
                    h_3_tmp=l_2[1]
                elif which_upper==2:
                    w_1_tmp=l_1[0]
                    h_1_tmp=l_1[1]
                    w_2_tmp=l_2[0]
                    h_2_tmp=l_2[1]
                    w_3_tmp=u_1[0]
                    h_3_tmp=u_1[1]
                    
            print("=========NEW TRIAL=========")
            print(effect)
            print(order)
            print("distance")
            print(distance)
            
            print("h1")
            print(h_1_tmp)
            print("w1")
            print(w_1_tmp)
            
            print("h2")
            print(h_2_tmp)
            print("w2")
            print(w_2_tmp)
            
            print("h3")
            print(h_3_tmp)
            print("w3")
            print(w_3_tmp)
            
            # add params to data
            # heights and widths already stored for critical, but not other trial types
            thisExp.addData('h_1_tmp',h_1_tmp)
            thisExp.addData('w_1_tmp',w_1_tmp)
            thisExp.addData('h_2_tmp',h_2_tmp)
            thisExp.addData('w_2_tmp',w_2_tmp)
            thisExp.addData('h_3_tmp',h_3_tmp)
            thisExp.addData('w_3_tmp',w_3_tmp)
            # Run 'Begin Routine' code from rect_locs
            # figure out rectangle locations
            # this is a PAIN
            
            # config_tmp - main configuration (fully balanced)
            # config_tmp - secondary configuration (randomized)
            
            # config_tmp predefined for critical trials but not other trials
            if effect == "critical":
                config_tmp = config
            else:
                config_tmp = np.random.choice([1, 2.1, 2.2, 3, 4])
                
            # figuring out the center or the left and right hand of the screen
            ctr_left = -round(screen_width*.5*.5)
            ctr_right= round(screen_width*.5*.5)
            
            # configuration 1: all 3 stimui next to each other
            if config_tmp == 1:
                config_tmp_1 = np.random.choice([1.1, 1.2, 1.3])
                
                # 1.1: stimuli on upper left of screen
                if config_tmp_1 == 1.1:
                    r_2_x = ctr_left
                    r_1_x= round(r_2_x - .5*w_2_tmp - .5*w_1_tmp - rect_dist)
                    r_3_x= round(r_2_x +.5*w_2_tmp + .5*w_3_tmp + rect_dist)
                    r_1_y = round((.5 * screen_height *.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_2_y = round((.5 * screen_height *.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_3_y = round((.5 * screen_height *.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                # 1.2 - stimuli in center of screen
                elif config_tmp_1 == 1.2:
                    r_1_x = round(-.5 * w_1_tmp - rect_dist - .5 * w_2_tmp)
                    r_2_x = 0
                    r_3_x = round(.5 * w_2_tmp + rect_dist + .5 * w_3_tmp)
                    r_1_y = round(0 + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_2_y = round(0 + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_3_y = round(0 + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                # 1.3 - stimuli in lower right of screen
                elif config_tmp_1 == 1.3:
                    r_2_x = ctr_right
                    r_1_x=round(r_2_x - .5*w_2_tmp - .5*w_1_tmp - rect_dist)
                    r_3_x=round(r_2_x +.5*w_2_tmp + .5*w_3_tmp + rect_dist)
                    r_1_y = -round((.5 * screen_height *.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_2_y = -round((.5 * screen_height *.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_3_y = -round((.5 * screen_height *.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                # configuration 2 - only 2 stimuli comparable
                # 2.1 - stimuli 1 and 2 are comparable
            elif config_tmp == 2.1:
                config_tmp_1 = np.random.choice([2.11, 2.12])
                r_1_x = round(- .5*w_1_tmp - rect_dist - .5*w_2_tmp)
                r_2_x = 0
                r_3_x = round(.5*w_2_tmp +rect_dist + .5*w_3_tmp)
                # 2.11 - stimuli 1 and 2 are comparable, but placed in upper left of screen
                # stimulus 3 in bottom left
                if config_tmp_1 == 2.11:
                    r_1_y = round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_2_y = round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_3_y = -round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                # 2.12 - stimuli 1 and 2 are comparable, but placed in lower left of screen
                # stimulus 3 in upper left
                elif config_tmp_1 == 2.12:
                    r_1_y = -round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_2_y = -round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_3_y = round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                # 2.2 - stimuli 2 and 3 are comparable
            elif config_tmp == 2.2:
                r_1_x = round(- .5*w_1_tmp - rect_dist - .5*w_2_tmp)
                r_2_x = 0
                r_3_x = round(.5*w_2_tmp +rect_dist + .5*w_3_tmp)
                # 2.21 stimuli 2 and 3 next to each other in upper right of screen
                config_tmp_1 = np.random.choice([2.21, 2.22])
                if config_tmp_1 == 2.21:
                    r_1_y = -round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_2_y = round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_3_y = round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                # 2.22 - stimuli 2 and 3 next to each other in bottom right of screen
                elif config_tmp_1 == 2.22:
                    r_1_y = round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_2_y = -round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_3_y = -round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
            # configuration 3 - no stimuli are comparable
            elif config_tmp == 3:
                config_tmp_1 = np.random.choice([3.1, 3.2])
                r_2_x = 0
                r_1_x = round(r_2_x - .5*w_2_tmp - rect_dist - .5*w_1_tmp)
                r_3_x = round(r_2_x +.5*w_2_tmp + rect_dist + .5*w_3_tmp)
                # 3.1 - stimulus 1 upper left, 2 center, 3 bottom right
                if config_tmp_1 == 3.1:
                    r_1_y = round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_2_y = round(np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_3_y = -round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                # 3.2 - stimulus 1 bottom left, 2 center, 3 upper right
                elif config_tmp_1 == 3.2:
                    r_1_y = -round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_2_y = round(np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_3_y = round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                # configuration 4 - triangle (spektor 2018 style)
            elif config_tmp == 4:
                config_tmp_1 = np.random.choice([4.1, 4.2])
                r_2_x = 0
                r_1_x = round(r_2_x - .5*w_2_tmp - rect_dist - .5*w_1_tmp)
                r_3_x = round(r_2_x +.5*w_2_tmp + rect_dist + .5*w_3_tmp)
                # 4.1 - regular triangle
                if config_tmp_1 == 4.1:
                    r_1_y = -round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_2_y = round(np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_3_y = -round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
                # 4.2 - inverted triangle
                elif config_tmp_1==4.2:
                    r_1_y = round(np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_3_y = round(np.random.uniform(-y_jitter, y_jitter, 1)[0])
                    r_2_y = -round((.5 * screen_height*.5) + np.random.uniform(-y_jitter, y_jitter, 1)[0])
            # text locations
            r_1_txt_x=r_1_x
            r_1_txt_y=r_1_y-.5*h_1_tmp-25
            r_2_txt_x=r_2_x
            r_2_txt_y=r_2_y-.5*h_2_tmp-25
            r_3_txt_x=r_3_x
            r_3_txt_y=r_3_y-.5*h_3_tmp-25
            
            thisExp.addData('config_tmp',config_tmp)
            thisExp.addData('config_tmp_1',config_tmp_1)
            thisExp.addData('r_1_x',r_1_x)
            thisExp.addData('r_1_y',r_1_y)
            thisExp.addData('r_2_x',r_2_x)
            thisExp.addData('r_2_y',r_2_y)
            thisExp.addData('r_3_x',r_3_x)
            thisExp.addData('r_3_y',r_3_y)
            
            # store start times for pre_trial
            pre_trial.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            pre_trial.tStart = globalClock.getTime(format='float')
            pre_trial.status = STARTED
            thisExp.addData('pre_trial.started', pre_trial.tStart)
            pre_trial.maxDuration = None
            # keep track of which components have finished
            pre_trialComponents = pre_trial.components
            for thisComponent in pre_trial.components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "pre_trial" ---
            # if trial has changed, end Routine now
            if isinstance(trials, data.TrialHandler2) and thisTrial.thisN != trials.thisTrial.thisN:
                continueRoutine = False
            pre_trial.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer], 
                        playbackComponents=[]
                    )
                    # skip the frame we paused on
                    continue
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    pre_trial.forceEnded = routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in pre_trial.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "pre_trial" ---
            for thisComponent in pre_trial.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for pre_trial
            pre_trial.tStop = globalClock.getTime(format='float')
            pre_trial.tStopRefresh = tThisFlipGlobal
            thisExp.addData('pre_trial.stopped', pre_trial.tStop)
            # the Routine "pre_trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            # --- Prepare to start Routine "choice_trial" ---
            # create an object to store info about Routine choice_trial
            choice_trial = data.Routine(
                name='choice_trial',
                components=[r_1, r_2, r_3, r_1_label, r_2_label, r_3_label, prompt, rect_choice],
            )
            choice_trial.status = NOT_STARTED
            continueRoutine = True
            # update component parameters for each repeat
            r_1.setPos((r_1_x, r_1_y))
            r_1.setSize((w_1_tmp, h_1_tmp))
            r_2.setPos((r_2_x, r_2_y))
            r_2.setSize((w_2_tmp, h_2_tmp))
            r_3.setPos((r_3_x, r_3_y))
            r_3.setSize((w_3_tmp, h_3_tmp))
            r_1_label.setColor([-1.0000, -1.0000, -1.0000], colorSpace='rgb')
            r_1_label.setPos((r_1_txt_x, r_1_txt_y))
            r_2_label.setPos((r_2_txt_x, r_2_txt_y))
            r_3_label.setPos((r_3_txt_x, r_3_txt_y))
            prompt.setPos((prompt_x_loc, prompt_y_loc))
            # create starting attributes for rect_choice
            rect_choice.keys = []
            rect_choice.rt = []
            _rect_choice_allKeys = []
            # store start times for choice_trial
            choice_trial.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
            choice_trial.tStart = globalClock.getTime(format='float')
            choice_trial.status = STARTED
            thisExp.addData('choice_trial.started', choice_trial.tStart)
            choice_trial.maxDuration = None
            # keep track of which components have finished
            choice_trialComponents = choice_trial.components
            for thisComponent in choice_trial.components:
                thisComponent.tStart = None
                thisComponent.tStop = None
                thisComponent.tStartRefresh = None
                thisComponent.tStopRefresh = None
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED
            # reset timers
            t = 0
            _timeToFirstFrame = win.getFutureFlipTime(clock="now")
            frameN = -1
            
            # --- Run Routine "choice_trial" ---
            # if trial has changed, end Routine now
            if isinstance(trials, data.TrialHandler2) and thisTrial.thisN != trials.thisTrial.thisN:
                continueRoutine = False
            choice_trial.forceEnded = routineForceEnded = not continueRoutine
            while continueRoutine:
                # get current time
                t = routineTimer.getTime()
                tThisFlip = win.getFutureFlipTime(clock=routineTimer)
                tThisFlipGlobal = win.getFutureFlipTime(clock=None)
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame
                
                # *r_1* updates
                
                # if r_1 is starting this frame...
                if r_1.status == NOT_STARTED and tThisFlip >= isi-frameTolerance:
                    # keep track of start time/frame for later
                    r_1.frameNStart = frameN  # exact frame index
                    r_1.tStart = t  # local t and not account for scr refresh
                    r_1.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(r_1, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'r_1.started')
                    # update status
                    r_1.status = STARTED
                    r_1.setAutoDraw(True)
                
                # if r_1 is active this frame...
                if r_1.status == STARTED:
                    # update params
                    pass
                
                # *r_2* updates
                
                # if r_2 is starting this frame...
                if r_2.status == NOT_STARTED and tThisFlip >= isi-frameTolerance:
                    # keep track of start time/frame for later
                    r_2.frameNStart = frameN  # exact frame index
                    r_2.tStart = t  # local t and not account for scr refresh
                    r_2.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(r_2, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'r_2.started')
                    # update status
                    r_2.status = STARTED
                    r_2.setAutoDraw(True)
                
                # if r_2 is active this frame...
                if r_2.status == STARTED:
                    # update params
                    pass
                
                # *r_3* updates
                
                # if r_3 is starting this frame...
                if r_3.status == NOT_STARTED and tThisFlip >= isi-frameTolerance:
                    # keep track of start time/frame for later
                    r_3.frameNStart = frameN  # exact frame index
                    r_3.tStart = t  # local t and not account for scr refresh
                    r_3.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(r_3, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'r_3.started')
                    # update status
                    r_3.status = STARTED
                    r_3.setAutoDraw(True)
                
                # if r_3 is active this frame...
                if r_3.status == STARTED:
                    # update params
                    pass
                
                # *r_1_label* updates
                
                # if r_1_label is starting this frame...
                if r_1_label.status == NOT_STARTED and tThisFlip >= isi-frameTolerance:
                    # keep track of start time/frame for later
                    r_1_label.frameNStart = frameN  # exact frame index
                    r_1_label.tStart = t  # local t and not account for scr refresh
                    r_1_label.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(r_1_label, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'r_1_label.started')
                    # update status
                    r_1_label.status = STARTED
                    r_1_label.setAutoDraw(True)
                
                # if r_1_label is active this frame...
                if r_1_label.status == STARTED:
                    # update params
                    pass
                
                # *r_2_label* updates
                
                # if r_2_label is starting this frame...
                if r_2_label.status == NOT_STARTED and tThisFlip >= isi-frameTolerance:
                    # keep track of start time/frame for later
                    r_2_label.frameNStart = frameN  # exact frame index
                    r_2_label.tStart = t  # local t and not account for scr refresh
                    r_2_label.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(r_2_label, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'r_2_label.started')
                    # update status
                    r_2_label.status = STARTED
                    r_2_label.setAutoDraw(True)
                
                # if r_2_label is active this frame...
                if r_2_label.status == STARTED:
                    # update params
                    pass
                
                # *r_3_label* updates
                
                # if r_3_label is starting this frame...
                if r_3_label.status == NOT_STARTED and tThisFlip >= isi-frameTolerance:
                    # keep track of start time/frame for later
                    r_3_label.frameNStart = frameN  # exact frame index
                    r_3_label.tStart = t  # local t and not account for scr refresh
                    r_3_label.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(r_3_label, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'r_3_label.started')
                    # update status
                    r_3_label.status = STARTED
                    r_3_label.setAutoDraw(True)
                
                # if r_3_label is active this frame...
                if r_3_label.status == STARTED:
                    # update params
                    pass
                
                # *prompt* updates
                
                # if prompt is starting this frame...
                if prompt.status == NOT_STARTED and tThisFlip >= isi-frameTolerance:
                    # keep track of start time/frame for later
                    prompt.frameNStart = frameN  # exact frame index
                    prompt.tStart = t  # local t and not account for scr refresh
                    prompt.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(prompt, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'prompt.started')
                    # update status
                    prompt.status = STARTED
                    prompt.setAutoDraw(True)
                
                # if prompt is active this frame...
                if prompt.status == STARTED:
                    # update params
                    pass
                
                # *rect_choice* updates
                waitOnFlip = False
                
                # if rect_choice is starting this frame...
                if rect_choice.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                    # keep track of start time/frame for later
                    rect_choice.frameNStart = frameN  # exact frame index
                    rect_choice.tStart = t  # local t and not account for scr refresh
                    rect_choice.tStartRefresh = tThisFlipGlobal  # on global time
                    win.timeOnFlip(rect_choice, 'tStartRefresh')  # time at next scr refresh
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'rect_choice.started')
                    # update status
                    rect_choice.status = STARTED
                    # keyboard checking is just starting
                    waitOnFlip = True
                    win.callOnFlip(rect_choice.clock.reset)  # t=0 on next screen flip
                    win.callOnFlip(rect_choice.clearEvents, eventType='keyboard')  # clear events on next screen flip
                if rect_choice.status == STARTED and not waitOnFlip:
                    theseKeys = rect_choice.getKeys(keyList=['1','2','3'], ignoreKeys=None, waitRelease=False)
                    _rect_choice_allKeys.extend(theseKeys)
                    if len(_rect_choice_allKeys):
                        rect_choice.keys = _rect_choice_allKeys[-1].name  # just the last key pressed
                        rect_choice.rt = _rect_choice_allKeys[-1].rt
                        rect_choice.duration = _rect_choice_allKeys[-1].duration
                        # a response ends the routine
                        continueRoutine = False
                if thisExp.status == FINISHED or endExpNow:
                    endExperiment(thisExp, win=win)
                    return
                # pause experiment here if requested
                if thisExp.status == PAUSED:
                    pauseExperiment(
                        thisExp=thisExp, 
                        win=win, 
                        timers=[routineTimer], 
                        playbackComponents=[]
                    )
                    # skip the frame we paused on
                    continue
                
                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    choice_trial.forceEnded = routineForceEnded = True
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in choice_trial.components:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished
                
                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()
            
            # --- Ending Routine "choice_trial" ---
            for thisComponent in choice_trial.components:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store stop times for choice_trial
            choice_trial.tStop = globalClock.getTime(format='float')
            choice_trial.tStopRefresh = tThisFlipGlobal
            thisExp.addData('choice_trial.stopped', choice_trial.tStop)
            # check responses
            if rect_choice.keys in ['', [], None]:  # No response was made
                rect_choice.keys = None
            trials.addData('rect_choice.keys',rect_choice.keys)
            if rect_choice.keys != None:  # we had a response
                trials.addData('rect_choice.rt', rect_choice.rt)
                trials.addData('rect_choice.duration', rect_choice.duration)
            # the Routine "choice_trial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()
            
        # completed 1.0 repeats of 'trials'
        
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        
        # --- Prepare to start Routine "end_block" ---
        # create an object to store info about Routine end_block
        end_block = data.Routine(
            name='end_block',
            components=[end_block_text],
        )
        end_block.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # store start times for end_block
        end_block.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        end_block.tStart = globalClock.getTime(format='float')
        end_block.status = STARTED
        thisExp.addData('end_block.started', end_block.tStart)
        end_block.maxDuration = None
        # keep track of which components have finished
        end_blockComponents = end_block.components
        for thisComponent in end_block.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "end_block" ---
        # if trial has changed, end Routine now
        if isinstance(blocks, data.TrialHandler2) and thisBlock.thisN != blocks.thisTrial.thisN:
            continueRoutine = False
        end_block.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 15.0:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *end_block_text* updates
            
            # if end_block_text is starting this frame...
            if end_block_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                end_block_text.frameNStart = frameN  # exact frame index
                end_block_text.tStart = t  # local t and not account for scr refresh
                end_block_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(end_block_text, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'end_block_text.started')
                # update status
                end_block_text.status = STARTED
                end_block_text.setAutoDraw(True)
            
            # if end_block_text is active this frame...
            if end_block_text.status == STARTED:
                # update params
                pass
            
            # if end_block_text is stopping this frame...
            if end_block_text.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > end_block_text.tStartRefresh + 15-frameTolerance:
                    # keep track of stop time/frame for later
                    end_block_text.tStop = t  # not accounting for scr refresh
                    end_block_text.tStopRefresh = tThisFlipGlobal  # on global time
                    end_block_text.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'end_block_text.stopped')
                    # update status
                    end_block_text.status = FINISHED
                    end_block_text.setAutoDraw(False)
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                end_block.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in end_block.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "end_block" ---
        for thisComponent in end_block.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for end_block
        end_block.tStop = globalClock.getTime(format='float')
        end_block.tStopRefresh = tThisFlipGlobal
        thisExp.addData('end_block.stopped', end_block.tStop)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if end_block.maxDurationReached:
            routineTimer.addTime(-end_block.maxDuration)
        elif end_block.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-15.000000)
        thisExp.nextEntry()
        
    # completed 4.0 repeats of 'blocks'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # --- Prepare to start Routine "end" ---
    # create an object to store info about Routine end
    end = data.Routine(
        name='end',
        components=[end_text, key_resp_7],
    )
    end.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for key_resp_7
    key_resp_7.keys = []
    key_resp_7.rt = []
    _key_resp_7_allKeys = []
    # store start times for end
    end.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    end.tStart = globalClock.getTime(format='float')
    end.status = STARTED
    thisExp.addData('end.started', end.tStart)
    end.maxDuration = None
    # keep track of which components have finished
    endComponents = end.components
    for thisComponent in end.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "end" ---
    end.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *end_text* updates
        
        # if end_text is starting this frame...
        if end_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            end_text.frameNStart = frameN  # exact frame index
            end_text.tStart = t  # local t and not account for scr refresh
            end_text.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(end_text, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'end_text.started')
            # update status
            end_text.status = STARTED
            end_text.setAutoDraw(True)
        
        # if end_text is active this frame...
        if end_text.status == STARTED:
            # update params
            pass
        
        # *key_resp_7* updates
        waitOnFlip = False
        
        # if key_resp_7 is starting this frame...
        if key_resp_7.status == NOT_STARTED and tThisFlip >= 2.0-frameTolerance:
            # keep track of start time/frame for later
            key_resp_7.frameNStart = frameN  # exact frame index
            key_resp_7.tStart = t  # local t and not account for scr refresh
            key_resp_7.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(key_resp_7, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'key_resp_7.started')
            # update status
            key_resp_7.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(key_resp_7.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(key_resp_7.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if key_resp_7.status == STARTED and not waitOnFlip:
            theseKeys = key_resp_7.getKeys(keyList=['space'], ignoreKeys=None, waitRelease=False)
            _key_resp_7_allKeys.extend(theseKeys)
            if len(_key_resp_7_allKeys):
                key_resp_7.keys = _key_resp_7_allKeys[-1].name  # just the last key pressed
                key_resp_7.rt = _key_resp_7_allKeys[-1].rt
                key_resp_7.duration = _key_resp_7_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            end.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in end.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "end" ---
    for thisComponent in end.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for end
    end.tStop = globalClock.getTime(format='float')
    end.tStopRefresh = tThisFlipGlobal
    thisExp.addData('end.stopped', end.tStop)
    # check responses
    if key_resp_7.keys in ['', [], None]:  # No response was made
        key_resp_7.keys = None
    thisExp.addData('key_resp_7.keys',key_resp_7.keys)
    if key_resp_7.keys != None:  # we had a response
        thisExp.addData('key_resp_7.rt', key_resp_7.rt)
        thisExp.addData('key_resp_7.duration', key_resp_7.duration)
    thisExp.nextEntry()
    # the Routine "end" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # --- Prepare to start Routine "debriefing" ---
    # create an object to store info about Routine debriefing
    debriefing = data.Routine(
        name='debriefing',
        components=[debrief_form, end_debrief],
    )
    debriefing.status = NOT_STARTED
    continueRoutine = True
    # update component parameters for each repeat
    # create starting attributes for end_debrief
    end_debrief.keys = []
    end_debrief.rt = []
    _end_debrief_allKeys = []
    # store start times for debriefing
    debriefing.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
    debriefing.tStart = globalClock.getTime(format='float')
    debriefing.status = STARTED
    thisExp.addData('debriefing.started', debriefing.tStart)
    debriefing.maxDuration = None
    # keep track of which components have finished
    debriefingComponents = debriefing.components
    for thisComponent in debriefing.components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    frameN = -1
    
    # --- Run Routine "debriefing" ---
    debriefing.forceEnded = routineForceEnded = not continueRoutine
    while continueRoutine:
        # get current time
        t = routineTimer.getTime()
        tThisFlip = win.getFutureFlipTime(clock=routineTimer)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *debrief_form* updates
        
        # if debrief_form is starting this frame...
        if debrief_form.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            debrief_form.frameNStart = frameN  # exact frame index
            debrief_form.tStart = t  # local t and not account for scr refresh
            debrief_form.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(debrief_form, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'debrief_form.started')
            # update status
            debrief_form.status = STARTED
            debrief_form.setAutoDraw(True)
        
        # if debrief_form is active this frame...
        if debrief_form.status == STARTED:
            # update params
            pass
        
        # *end_debrief* updates
        waitOnFlip = False
        
        # if end_debrief is starting this frame...
        if end_debrief.status == NOT_STARTED and tThisFlip >= 4.0-frameTolerance:
            # keep track of start time/frame for later
            end_debrief.frameNStart = frameN  # exact frame index
            end_debrief.tStart = t  # local t and not account for scr refresh
            end_debrief.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(end_debrief, 'tStartRefresh')  # time at next scr refresh
            # add timestamp to datafile
            thisExp.timestampOnFlip(win, 'end_debrief.started')
            # update status
            end_debrief.status = STARTED
            # keyboard checking is just starting
            waitOnFlip = True
            win.callOnFlip(end_debrief.clock.reset)  # t=0 on next screen flip
            win.callOnFlip(end_debrief.clearEvents, eventType='keyboard')  # clear events on next screen flip
        if end_debrief.status == STARTED and not waitOnFlip:
            theseKeys = end_debrief.getKeys(keyList=['space'], ignoreKeys=None, waitRelease=False)
            _end_debrief_allKeys.extend(theseKeys)
            if len(_end_debrief_allKeys):
                end_debrief.keys = _end_debrief_allKeys[-1].name  # just the last key pressed
                end_debrief.rt = _end_debrief_allKeys[-1].rt
                end_debrief.duration = _end_debrief_allKeys[-1].duration
                # a response ends the routine
                continueRoutine = False
        if thisExp.status == FINISHED or endExpNow:
            endExperiment(thisExp, win=win)
            return
        # pause experiment here if requested
        if thisExp.status == PAUSED:
            pauseExperiment(
                thisExp=thisExp, 
                win=win, 
                timers=[routineTimer], 
                playbackComponents=[]
            )
            # skip the frame we paused on
            continue
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            debriefing.forceEnded = routineForceEnded = True
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in debriefing.components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # --- Ending Routine "debriefing" ---
    for thisComponent in debriefing.components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    # store stop times for debriefing
    debriefing.tStop = globalClock.getTime(format='float')
    debriefing.tStopRefresh = tThisFlipGlobal
    thisExp.addData('debriefing.stopped', debriefing.tStop)
    # check responses
    if end_debrief.keys in ['', [], None]:  # No response was made
        end_debrief.keys = None
    thisExp.addData('end_debrief.keys',end_debrief.keys)
    if end_debrief.keys != None:  # we had a response
        thisExp.addData('end_debrief.rt', end_debrief.rt)
        thisExp.addData('end_debrief.duration', end_debrief.duration)
    thisExp.nextEntry()
    # the Routine "debriefing" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
