# Created by Scarlet Ghorbani, 2018
# use it for whatever
import pygame.midi as midi
import pygame
import sys
import pprint

pygame.init()
midi.init()

INPUT = None #midi.Input
OUTPUT = None #midi.Output

MIDI_COUNT = midi.get_count()
IN_TARGET = 'LoopBe Internal MIDI' #we want to intercept a specific midi message from this and then send a sysex back to induce a change of bank
OUT_TARGET = "Launch Control XL"

DEVICE_IN = None #id number of input device
DEVICE_OUT = None #id number of output device

for x in range(0, MIDI_COUNT):
    device = midi.get_device_info(x)
    # print "_____" + device[1]
    if device[1] == IN_TARGET:
        print "TARGET DETECTED AND STORED..."
        if device[2] == 1:
            DEVICE_IN = x
    if device[1] == OUT_TARGET:
        if device[3] == 1:
            DEVICE_OUT = x

print
print
print "Welcome to the Better LCXL script, to start, do the following:"
print "1: Press the side arrows to switch around a few banks"
print "2: Touch a few knobs and faders to make sure they're on"
print "3: Switch banks once more to make sure they're remembering properly."
print
print "------------------------- Troubleshooting ----------------------------"
print "If the program isn't working, make sure MidiOx is running, with Launch Control XL's input linked to the LoopBe Internal Midi port in the routing configs."
print "Also make sure FL studio isn't running before you launch the script."
print "----------------------------------------------------------------------"
print
print
print "INPUT: " + str(DEVICE_IN) + "   " + str(midi.get_device_info(DEVICE_IN))
print "OUTPUT: " + str(DEVICE_OUT) + "   " + str(midi.get_device_info(DEVICE_OUT))

INPUT = midi.Input(DEVICE_IN)
OUTPUT = midi.Output(DEVICE_OUT)
#
#
current_template = 1
bank_count = 8

id_range = [176, 178, 179, 180, 181, 182, 183] #I don't know what that leading number is but it changes with the bank

fader_range = [77,78,79,80,81,82,83,84]

knobs_top_row_range = [13,14,15,16,17,18,19,20]
knobs_mid_row_range = [29,30,31,32,33,34,35,36]
knobs_bot_row_range = [49,50,51,52,53,54,55,56]

top_remap = [0,1,2,3,4,5,6,7]
mid_remap = [8,9,10,11,12,13,14,15]
bot_remap = [16,17,18,19,20,21,22,23]


curr_val_top_row = {
    0:0,
    1:0,
    2:0,
    3:0,
    4:0,
    5:0,
    6:0,
    7:0
}

curr_val_mid_row = {
    0:0,
    1:0,
    2:0,
    3:0,
    4:0,
    5:0,
    6:0,
    7:0
}

curr_val_bot_row = {
    0:0,
    1:0,
    2:0,
    3:0,
    4:0,
    5:0,
    6:0,
    7:0
}

stored_top_row_vals = {
    0: [0,0,0,0,0,0,0,0],
    1: [0,0,0,0,0,0,0,0],
    2: [0,0,0,0,0,0,0,0],
    3: [0,0,0,0,0,0,0,0],
    4: [0,0,0,0,0,0,0,0],
    5: [0,0,0,0,0,0,0,0],
    6: [0,0,0,0,0,0,0,0],
    7: [0,0,0,0,0,0,0,0]
}

stored_mid_row_vals = {
    0: [0,0,0,0,0,0,0,0],
    1: [0,0,0,0,0,0,0,0],
    2: [0,0,0,0,0,0,0,0],
    3: [0,0,0,0,0,0,0,0],
    4: [0,0,0,0,0,0,0,0],
    5: [0,0,0,0,0,0,0,0],
    6: [0,0,0,0,0,0,0,0],
    7: [0,0,0,0,0,0,0,0]
}

stored_bot_row_vals = {
    0: [0,0,0,0,0,0,0,0],
    1: [0,0,0,0,0,0,0,0],
    2: [0,0,0,0,0,0,0,0],
    3: [0,0,0,0,0,0,0,0],
    4: [0,0,0,0,0,0,0,0],
    5: [0,0,0,0,0,0,0,0],
    6: [0,0,0,0,0,0,0,0],
    7: [0,0,0,0,0,0,0,0]
}


fader_map = {
    77: (24,0),
    78: (25,1),
    79: (26,2),
    80: (27,3),
    81: (28,4),
    82: (29,5),
    83: (30,6),
    84: (31,7),
}

color_map = {
    0: 12,
    1: 28,
    2: 60,
    3: 62,
    4: 29,
    5: 63,
    6: 13,
    7: 15,

}

flash_map = {
    0: 12,
    1: 56,
    2: 56,
    3: 58,
    4: 59,
    5: 59,
    6: 11,
    7: 11
}

curr_val_faders = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
}

stored_fader_vals = {
    0: [0,0,0,0,0,0,0,0],
    1: [0,0,0,0,0,0,0,0],
    2: [0,0,0,0,0,0,0,0],
    3: [0,0,0,0,0,0,0,0],
    4: [0,0,0,0,0,0,0,0],
    5: [0,0,0,0,0,0,0,0],
    6: [0,0,0,0,0,0,0,0],
    7: [0,0,0,0,0,0,0,0],
}


def calculate_knob_led_color(param_level, knob_id): #super ugly, could've been streamlined if I designed it better
    global knobs_bot_row_range, knobs_mid_row_range, knobs_top_row_range, curr_val_bot_row, curr_val_mid_row, curr_val_top_row
    scaled_val = int(param_level/16) % 8
    if knob_id in knobs_bot_row_range:
        curr_val_bot_row[knobs_bot_row_range.index(knob_id)] = scaled_val
    elif knob_id in knobs_mid_row_range:
        curr_val_mid_row[knobs_mid_row_range.index(knob_id)] = scaled_val
    elif knob_id in knobs_top_row_range:
        curr_val_top_row[knobs_top_row_range.index(knob_id)] = scaled_val
    return color_map[scaled_val]


def calculate_led_color(param_level, fader_id):
    global curr_val_faders
    #this will scale the fader level across a b->g->y->o->r
    scaled_val = int(param_level / 16) % 8
    curr_val_faders[fader_id] = scaled_val
    return color_map[scaled_val]





for t in range(0,8):
    for b in range(0,128):
        OUTPUT.write_sys_ex(pygame.midi.time(),[240, 0, 32, 41, 2, 17, 120, t, b, 12, 247]) #wipe all buttons on start

while True:

    if INPUT.poll():
        in_data = INPUT.read(1000)
        #a template change looks like [[[240, 0, 32, 41], 1627], [[2, 17, 119, 2], 1627], [[247, 0, 0, 0], 1627]] where the 2 in the middle means which one to jump to

        #first detect which template we are on
        new_template = current_template
        fader_shift = False
        knob_shift = False

        for event in in_data:
            m_sig = event[0]
            ts = event[1]

            if m_sig[0] == 2: #this is reserved for bank changes
                new_template = m_sig[3]
            elif m_sig[0] in id_range and m_sig[2] == 127: #indicates one of the arrow keys I guess
                if m_sig[1] == 106: #decrement one bank
                    new_template -= 1
                elif m_sig[1] == 107: #increment one bank
                    new_template += 1
                elif m_sig[0] == 182 and m_sig[1] == 116: #for some reason, bank 6 reassigns the CC numbers so it needs a special case
                    new_template -= 1
                elif m_sig[0] == 182 and m_sig[1] == 117:
                    new_template += 1
                new_template %= bank_count
            elif m_sig[0] in id_range and m_sig[1] in fader_range:
                fader_shift = (fader_map[m_sig[1]][0],m_sig[2],current_template, fader_map[m_sig[1]][1])
            elif m_sig[0] in id_range and m_sig[1] in knobs_top_row_range:
                knob_shift = (top_remap[knobs_top_row_range.index(m_sig[1])], m_sig[2], current_template, m_sig[1])
            elif m_sig[0] in id_range and m_sig[1] in knobs_mid_row_range:
                knob_shift = (mid_remap[knobs_mid_row_range.index(m_sig[1])], m_sig[2], current_template, m_sig[1])
            elif m_sig[0] in id_range and m_sig[1] in knobs_bot_row_range:
                knob_shift = (bot_remap[knobs_bot_row_range.index(m_sig[1])], m_sig[2], current_template, m_sig[1])

        if new_template != current_template:
            print "Template change to " + str(new_template)
            pprint.pprint(in_data)
            print
            #now do a sysex to induce the bank change on the controller
            button_num = 32 + new_template

            OUTPUT.write_sys_ex(pygame.midi.time(), [240, 0, 32, 41, 2, 17, 120, new_template, button_num, 15, 247])
            OUTPUT.write_sys_ex(pygame.midi.time(), [240, 0, 32, 41, 2, 17, 119, new_template, 247])
            current_template = new_template
        if fader_shift is not False:
            fader_val = calculate_led_color(fader_shift[1], fader_shift[3])
            OUTPUT.write_sys_ex(pygame.midi.time(), [240, 0, 32, 41, 2, 17, 120, current_template, fader_shift[0], fader_val, 247])
        if knob_shift is not False:
            knob_val = calculate_knob_led_color(knob_shift[1], knob_shift[3])
            OUTPUT.write_sys_ex(pygame.midi.time(),[240, 0, 32, 41, 2, 17, 120, current_template, knob_shift[0], knob_val, 247])
    pygame.time.wait(10)

INPUT.close()
OUTPUT.close()