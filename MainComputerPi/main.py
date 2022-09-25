import serial
import pygame
import urwid as urwid
from urwid_timed_progress import TimedProgressBar
import UI
import GridItem
import json
import time
from slowprint.slowprint import *
import os
from time import sleep
from tqdm import tqdm
import math
import datetime

power_current = 0  # current power
powerTotal = 100  # total power needed
power_target = 0  # power supplied by existing batteries
minutes_until_failure = 15  # minutes until portal control failure
portal_opening_time = 0  # time portal will open
boot_up_text = False  # display portal control boot up text
power_up_complete = False  # state of portal control unit
battery_processor_device = "/dev/ttyACM0"  # battery processor device
ending_music_played = False  # has the ending music played yet
sec1_sound_played = False
sec2_sound_played = False
sec3_sound_played = False
sec4_sound_played = False
sec5_sound_played = False
sec30_sound_played = False
min1_sound_played = False
min2_sound_played = False
min3_sound_played = False
min4_sound_played = False
min5_sound_played = False
min10_sound_played = False
min15_sound_played = False

# color pallet
palette = [
    ('titlebar', 'white, bold', 'light blue'),
    ('headers', 'white,bold', 'dark blue'),
    ('body', 'white', 'dark blue'),
    ('on', 'yellow,bold', 'dark blue'),
    ('off', 'light red', 'dark blue'),
    ('regular', 'light gray', 'dark blue'),
    ('red', 'light red', 'dark blue'),
    ('redflash', 'dark red', 'dark blue'),
    ('yellow', 'yellow', 'dark blue'),
    ('lightbar', 'light blue', 'dark blue'),
    ('darkbar', 'black', 'dark blue'),
    ('normal', 'white', 'dark blue', 'standout'),
    ('complete', 'white', 'light blue'),
    ('warning', 'light gray', 'dark blue')]


# main refresh loop
def refresh(_loop, _data):
    global power_current
    global power_target
    global portal_opening_time
    global power_up_complete
    global minutes_until_failure
    global big_header_text
    global ending_music_played
    global sec30_sound, min1_sound, min2_sound, min3_sound, min4_sound, min5_sound, min10_sound, min15_sound, victory_sound, failure_sound
    global sec30_sound_played, min1_sound_played, min2_sound_played, min3_sound_played, min4_sound_played, min5_sound_played, min10_sound_played, min15_sound_played
    global sec5_sound, sec4_sound, sec3_sound, sec2_sound, sec1_sound
    global sec5_sound_played, sec4_sound_played, sec3_sound_played, sec2_sound_played, sec1_sound_played
    global serialPort
    if portal_opening_time == 0:
        portal_opening_time = datetime.datetime.now() + datetime.timedelta(minutes=minutes_until_failure)
    main_loop.draw_screen()  # redraw screen

    if not power_up_complete:
        main_status_text.set_text(get_update())  # refresh battery status

    # process data from battery processor
    serialPort.write(b"getbytes\r\n")  # request update from battery processor
    if serialPort.inWaiting() > 0:  # if request results waiting
        serial_input = serialPort.readline().strip()  # read results
        if serial_input.isalnum():  # if is a number
            if int(serial_input) & 1 == 1:
                if item_list[0].status == GridItem.Status.OFF.value:
                    fanfare_sound.play()
                    item_list[0].status = GridItem.Status.ON.value
                    serialPort.write(b"door\r\n")
            elif item_list[0].status == GridItem.Status.ON.value:
                beeoo_sound.play()
                item_list[0].status = GridItem.Status.OFF.value
            if int(serial_input) & 2 == 2:
                if item_list[1].status == GridItem.Status.OFF.value:
                    fanfare_sound.play()
                    item_list[1].status = GridItem.Status.ON.value
            elif item_list[1].status == GridItem.Status.ON.value:
                beeoo_sound.play()
                item_list[1].status = GridItem.Status.OFF.value
            if int(serial_input) & 4 == 4:
                if item_list[2].status == GridItem.Status.OFF.value:
                    fanfare_sound.play()
                    item_list[2].status = GridItem.Status.ON.value
            elif item_list[2].status == GridItem.Status.ON.value:
                beeoo_sound.play()
                item_list[2].status = GridItem.Status.OFF.value
            if int(serial_input) & 8 == 8:
                if item_list[3].status == GridItem.Status.OFF.value:
                    fanfare_sound.play()
                    item_list[3].status = GridItem.Status.ON.value
            elif item_list[3].status == GridItem.Status.ON.value:
                beeoo_sound.play()
                item_list[3].status = GridItem.Status.OFF.value


    # refresh power bar
    if power_current < power_target:
        progress_bar.add_progress(1)
        power_current = power_current + 1
    elif power_current > power_target:
        progress_bar.add_progress(-1)
        power_current = power_current - 1
    elif power_current == 100:
        power_up_complete = True

    # update timer
    current_time = datetime.datetime.now()
    seconds_until_open = int((portal_opening_time - current_time).total_seconds())
    days = seconds_until_open // 86400
    hours = (seconds_until_open - days * 86400) // 3600
    minutes = (seconds_until_open - days * 86400 - hours * 3600) // 60
    seconds = seconds_until_open - days * 86400 - hours * 3600 - minutes * 60
    if not power_up_complete:
        if big_text_countdown.get_text()[0] == '15:00' and not min15_sound_played:
            min15_sound.play()
            min15_sound_played = True
        elif big_text_countdown.get_text()[0] == '10:00' and not min10_sound_played:
            min10_sound.play()
            min10_sound_played = True
        elif big_text_countdown.get_text()[0] == '05:00' and not min5_sound_played:
            min5_sound.play()
            min5_sound_played = True
        elif big_text_countdown.get_text()[0] == '04:00' and not min4_sound_played:
            min4_sound.play()
            min4_sound_played = True
        elif big_text_countdown.get_text()[0] == '03:00' and not min3_sound_played:
            min3_sound.play()
            min3_sound_played = True
        elif big_text_countdown.get_text()[0] == '02:00' and not min2_sound_played:
            min2_sound.play()
            min2_sound_played = True
        elif big_text_countdown.get_text()[0] == '01:00' and not min1_sound_played:
            min1_sound.play()
            min1_sound_played = True
        elif big_text_countdown.get_text()[0] == '00:30' and not sec30_sound_played:
            sec30_sound.play()
            sec30_sound_played = True
        elif big_text_countdown.get_text()[0] == '00:05' and not sec5_sound_played:
            sec5_sound.play()
            sec5_sound_played = True
        elif big_text_countdown.get_text()[0] == '00:04' and not sec4_sound_played:
            sec4_sound.play()
            sec4_sound_played = True
        elif big_text_countdown.get_text()[0] == '00:03' and not sec3_sound_played:
            sec3_sound.play()
            sec3_sound_played = True
        elif big_text_countdown.get_text()[0] == '00:02' and not sec2_sound_played:
            sec2_sound.play()
            sec2_sound_played = True
        elif big_text_countdown.get_text()[0] == '00:01' and not sec1_sound_played:
            sec1_sound.play()
            sec1_sound_played = True

        if minutes < 1:
            if (seconds % 2) == 0:
                countdown_timer_value = [('redflash', str(minutes).zfill(2) + ":" + str(seconds).zfill(2))]
                main_loop.screen.register_palette_entry('warning', 'light red', 'dark blue')
                main_loop.screen.clear()
            else:
                countdown_timer_value = [('red', str(minutes).zfill(2) + ":" + str(seconds).zfill(2))]
                main_loop.screen.register_palette_entry('warning', 'dark red', 'dark blue')
                main_loop.screen.clear()
            big_header_text.set_text("STATUS: CRITICAL")
            main_loop.screen.register_palette_entry('warning', 'light red', 'dark blue')
        elif minutes < 3:
            big_header_text.set_text("STATUS: CRITICAL")
            main_loop.screen.register_palette_entry('warning', 'light red', 'dark blue')
            countdown_timer_value = [('red', str(minutes).zfill(2) + ":" + str(seconds).zfill(2))]
        elif minutes < 5:
            countdown_timer_value = [('yellow', str(minutes).zfill(2) + ":" + str(seconds).zfill(2))]
        else:
            countdown_timer_value = str(minutes).zfill(2) + ":" + str(seconds).zfill(2)
        big_text_countdown.set_text(countdown_timer_value)

    # out of time
    if current_time >= portal_opening_time and not power_up_complete:
        countdown_timer_value = [('red', "00:00")];
        big_header_text.set_text("STATUS: FAILURE")
        big_text_countdown.set_text(countdown_timer_value)
        main_loop.screen.register_palette_entry('body', 'white', 'dark red')
        main_loop.screen.register_palette_entry('titlebar', 'white, bold', 'light red')
        main_loop.screen.register_palette_entry('headers', 'white,bold', 'dark red')
        main_loop.screen.register_palette_entry('on', 'yellow,bold', 'dark red')
        main_loop.screen.register_palette_entry('off', 'light red', 'dark red')
        main_loop.screen.register_palette_entry('regular', 'light gray', 'dark red')
        main_loop.screen.register_palette_entry('lightbar', 'light red', 'dark red')
        main_loop.screen.register_palette_entry('darkbar', 'black', 'dark red')
        main_loop.screen.register_palette_entry('normal', 'white', 'dark red', 'standout')
        main_loop.screen.register_palette_entry('complete', 'white', 'dark red')
        main_loop.screen.register_palette_entry('red', 'light red', 'dark red')
        main_loop.screen.register_palette_entry('warning', 'light red', 'dark red')
        count_down_text.set_text("PORTAL CONTROL FAILURE!!! PORTAL OPENING!!! EVACUATE IMMEDIATELY! INVASION IMMINENT!")
        if not ending_music_played:
            error_sound.play(loops=20)
            error_sound.fadeout(10000)
            sleep(1)
            failure_sound.play()
            ending_music_played = True
        main_loop.screen.clear()

        # success!
    if power_up_complete:
        big_header_text.set_text("STATUS: NORMAL")
        main_loop.screen.register_palette_entry('warning', 'light gray', 'dark blue')
        count_down_text.set_text("CONGRATULATIONS! PORTAL CONTROL FULLY POWERED UP! PORTAL SHUTDOWN INITIATED!\n")
        if not ending_music_played:
            sleep(1.5)
            victory_sound.play()
            ending_music_played = True
        serialPort.write(b"bookcase\r\n")
    main_loop.set_alarm_in(0.01, refresh)


# is this a number?
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


# update battery status
def get_update():
    global power_target
    updates = [
        ('headers', u'Socket\t'.expandtabs(6)),
        ('headers', u'Device \t '.expandtabs(25)),
        ('headers', u'Status \n'.expandtabs(5))]
    active_power_cells = 0
    for item in item_list:
        if item.key != '':
            append_text(updates, '({}) \t '.format(item.key), tabsize=11)
        else:
            append_text(updates, '{} \t '.format(''), tabsize=6)
        append_text(updates, '{} \t '.format(item.label), tabsize=25)
        append_text(updates, '{} \t '.format(item.status), tabsize=4, text_type=item.status)
        append_text(updates, '\n')
        if item.status == GridItem.Status.ON.value:
            active_power_cells = active_power_cells + 1
    append_text(updates, '\n')
    append_text(updates, 'Last update: ')
    append_text(updates, time.asctime(time.localtime(time.time())))
    power_target = math.ceil(active_power_cells / 6 * 100)
    return updates


# append text to status message
def append_text(l, s, tabsize=10, color='body', text_type='default'):
    if text_type == GridItem.Status.ON.value:
        l.append(('on', s.expandtabs(tabsize)))
    elif text_type == GridItem.Status.OFF.value:
        l.append(('off', s.expandtabs(tabsize)))
    else:
        l.append(('regular', s.expandtabs(tabsize)))


# handle keyboard input
def handle_input(key):
    global fanfare_sound, beeoo_sound
    if key in ('q', 'Q'):
        raise urwid.ExitMainLoop()
    elif key in ('r', 'R'):
        refresh(main_loop, '')
        return
    #for keyitem in item_list:
    #    if keyitem.key != '':
    #        if key == keyitem.key:
    #            if keyitem.status == GridItem.Status.OFF.value:
    #                fanfare_sound.play()
    #                keyitem.status = GridItem.Status.ON.value
    #            elif keyitem.status == GridItem.Status.ON.value:
    #                beeoo_sound.play()
    #                keyitem.status = GridItem.Status.OFF.value


# main program
with open('resources/griditems.json', 'r') as f:
    data = json.load(f)
items = data.get('Griditems')
item_list = []
for item in items:
    item_list.append(GridItem.GridItem(item.get('name'), item.get('label'), item.get('status'), item.get('key')))

# set up screen widgets
header = urwid.AttrMap(urwid.Text(u' Portal Control Grid', align='center'), 'titlebar')
menu = urwid.AttrMap(urwid.Text([
    u'Portal Control Grid copyright 1986 Integrated Computer Systems'
], align='center'), 'body')

big_header_text = urwid.BigText("STATUS: WARNING", urwid.HalfBlock5x4Font())
big_header_padding = urwid.Padding(big_header_text, "center", None)
progress_bar = TimedProgressBar('normal', 'complete', label='Secondary Power',
                                units='%', done=powerTotal)
progress_box = UI.LineBox(urwid.AttrMap(progress_bar, 'body'), light_attr='lightbar', dark_attr='darkbar')
count_down_text = urwid.Text("Time until portal shielding failure:\n\n\n", align='center')
big_text_countdown = urwid.BigText(str(minutes_until_failure).zfill(2) + ":00", urwid.HalfBlock5x4Font())
countdown_padding = urwid.Padding(big_text_countdown, "center", None)
countdown_pile = UI.LineBox(
    urwid.Pile([urwid.AttrMap(count_down_text, 'body'), urwid.AttrMap(countdown_padding, 'body')]),
    light_attr='lightbar', dark_attr='darkbar')
main_status_text = urwid.Text(u'CRITICAL: ' + str(minutes_until_failure).zfill(2) + ':00 UNTIL DIMENSIONAL PORTAL '
                                                                                    'SHIELDING FAILURE! RESTORE FULL '
                                                                                    'POWER TO SHUTDOWN PORTAL!')
main_status_textbox = UI.LineBox(urwid.AttrMap(main_status_text, 'body'), light_attr='lightbar',
                                 dark_attr='darkbar')
primary_interface_columns = urwid.Columns([('weight', 2, main_status_textbox), countdown_pile])
primary_interface_pile = urwid.Pile(
    [urwid.AttrMap(big_header_padding, 'warning'), urwid.AttrMap(primary_interface_columns, 'body'),
     urwid.AttrMap(progress_box,
                   'body')])
primary_interface_padding = urwid.AttrMap(urwid.Padding(urwid.Filler(urwid.AttrMap(primary_interface_pile, 'body')),
                                                        left=1, right=1), 'body')
primary_interface = UI.LineBox(primary_interface_padding, light_attr='lightbar', dark_attr='darkbar')
layout = urwid.Frame(header=header, body=primary_interface, footer=menu)

# boot up sequence
os.system('clear')

# audio setup
pygame.mixer.init()
modem_sound = pygame.mixer.Sound("resources/modem.wav")
modem_sound.set_volume(0.6)
error_sound = pygame.mixer.Sound("resources/DELETED.ogg")
error_sound.set_volume(1)
floppy_sound = pygame.mixer.Sound("resources/525_floppyload_sound.ogg")
floppy_sound.set_volume(1)
startup_sound = pygame.mixer.Sound("resources/Compy386startup.ogg")
startup_sound.set_volume(0.5)
ding_sound = pygame.mixer.Sound("resources/Win95_ding.ogg")
ding_sound.set_volume(1)
beeoo_sound = pygame.mixer.Sound("resources/Beeoo.ogg")
beeoo_sound.set_volume(0.5)
creepy_sound = pygame.mixer.Sound("resources/Lurking_horrors.ogg")
packstart_sound = pygame.mixer.Sound("resources/KJH_PackstartCombo.ogg")
packstart_sound.set_volume(0.1)
power_sound = pygame.mixer.Sound("resources/KJH_Nutrona3.ogg")
packstart_sound.set_volume(0.8)
min15_sound = pygame.mixer.Sound("resources/15.wav")
min10_sound = pygame.mixer.Sound("resources/10.wav")
min5_sound = pygame.mixer.Sound("resources/5.wav")
min4_sound = pygame.mixer.Sound("resources/4.wav")
min3_sound = pygame.mixer.Sound("resources/3.wav")
min2_sound = pygame.mixer.Sound("resources/2.wav")
min1_sound = pygame.mixer.Sound("resources/1.wav")
sec30_sound = pygame.mixer.Sound("resources/30sec.wav")
sec5_sound = pygame.mixer.Sound("resources/5sec.wav")
sec4_sound = pygame.mixer.Sound("resources/4sec.wav")
sec3_sound = pygame.mixer.Sound("resources/3sec.wav")
sec2_sound = pygame.mixer.Sound("resources/2sec.wav")
sec1_sound = pygame.mixer.Sound("resources/1sec.wav")
winxp_sound = pygame.mixer.Sound("resources/erro-2.ogg")
fanfare_sound = pygame.mixer.Sound("resources/fanfare.ogg")
fanfare_sound.set_volume(0.7)
victory_sound = pygame.mixer.Sound("resources/victory.ogg")
failure_sound = pygame.mixer.Sound("resources/metalgeargameov5235.ogg")
winxp_sound.set_volume(0.8)
if boot_up_text:
    startup_sound.play()
    print('------------------------------------------')
    slowprint("Dimensional Portal Emergency Shutdown v0.6", 0.3)
    print('------------------------------------------')
    floppy_sound.play()
    sleep(1)
    slowprint("Control Grid:           Online", 0.2)
    floppy_sound.play()
    slowprint("Biostasis Containment:  Online", 0.2)
    slowprint("Reactor Safety Primary: Offline", 0.3)
    floppy_sound.play()
    sleep(0.5)
    slowprint("Reactor Safety Backup:  Offline", 0.3)
    sleep(0.5)
    floppy_sound.play()
    slowprint("SAFETY SYSTEMS DISENGAGED", 0.5)
    slowprint("Ventilation:            Online", 0.3)
    slowprint("Initializing Quantum Dampers", 0.3)
    packstart_sound.play()
    for i in tqdm(range(100)):
        sleep(0.01)
    packstart_sound.fadeout(500)
    sleep(1)
    packstart_sound.stop()
    slowprint("Connecting to Portal", 0.3)
    modem_sound.play()
    for i in tqdm(range(100)):
        sleep(0.025)
    sleep(1)
    slowprint("Reticulating Splines", 0.3)
    for i in tqdm(range(100)):
        sleep(0.005)
    sleep(1)
    slowprint("Power System Initialization", 0.3)
    power_sound.play()
    for i in tqdm(range(100)):
        sleep(0.05)
        if i > 80:
            break
    power_sound.stop()
    error_sound.play()
    sleep(1)
    floppy_sound.play()
    slowprint("Primary Power System Failure", 0.3)
    sleep(3)
    slowprint("Secondary Power Initialization", 0.3)
    power_sound.play()
    with tqdm(total=100) as pbar:
        for i in range(100):
            sleep(0.1)
            pbar.update(1)
            if i > 17:
                break
    power_sound.stop()
    error_sound.play()
    slowprint("Flagrant System Error - Secondary Power Offline", 0.3)
    sleep(1)
    floppy_sound.play()
    slowprint("2 of 6 power cells online", 0.3)
    sleep(4)
    slowprint("Please insert 6 power cells to shut down dimensional portal", 0.3)
    sleep(6)
    os.system('clear')
    floppy_sound.play()
    sleep(1)
slowprint(
    "Vgl = GetHandl {dat.dt} tempCall {itm.temp} \n Vg2 = GetHandl {dat.itl} tempCall {itm.temp} \nif Link(Vgl,"
    "Vg2) set Lim(Vgl,Vg2) \n return \nif Link(Vg2,Vgl) set Lim(Vg2,Vgl) \n return \non whte_rbt.obj \n link set "
    "security (Vgl), perimeter (Vg2) \n limitDat.1 = maxbits (%22) to {limit .04} \n set on limitDat.2 = setzero, "
    "setfive, 0 {limit .2-var(dzh)} \non fini.obi call link.sst {security, perimeter} set to on \n on fini.obi "
    "set link.sst {security, perimeter} restore \n on fini.obi delete line rf whte_rbt.obj, fini.obj \nVgl = "
    "GetHandl {dat.dt} tempCall {itm.temp} \nVg2 = GetHandl {dat.itl} tempCall {itm.temp} \nIimitDat.4 = maxbits "
    "(%33) to {limit .04} set on \nlimitDat.5 = setzero, setfive, 0 {limit .2-var(szh)}",
    0.03)
sleep(1)
os.system('clear')
winxp_sound.play()
with open('resources/ascii-art.txt', 'r') as f:
    print(f.read())
sleep(0.1)
os.system('clear')

# connect to battery processor
serialPort = serial.Serial(battery_processor_device, 115200, timeout=0)
serialPort.write(b"reset\r\n")

# create main interface and start program loop
main_loop = urwid.MainLoop(layout, palette, unhandled_input=handle_input)
main_loop.set_alarm_in(2, refresh)
main_loop.run()
