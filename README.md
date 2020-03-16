# better_vst_lcxl
A homemade fix for the launch control XL to make the control flow a little simpler for VSTs


# Background
I wanted a better control flow for the Launch Control when using VSTs in FL Studio. I felt like the User mode's switching between banks was clunky (it involved a two-button combination) and the leds gave no real feedback. Nothing huge just some tweaks to the workflow.


# Features
* In User mode, pressing the Track Select arrows now increments/decrements banks, instead of needing to press two buttons (If I recall correctly, User + the bottom row toggle button for the target bank)
* The bottom row of toggle buttons now lights the button corresponding to the currently selected bank in red to make it simple to know what bank you are on.
* All knobs and faders now have the LED adjacent to them light up corresponding to the value of the input. I.e. a knob set to 0 has no light, 20 has Green, 127 has Red, this just helps make it easy to remember what values are set at at a glance.
* The LED values are preserved for each bank, switching away from one bank and coming back will show the LED lights of the values from that bank last time you were there, this is as close to "memory" as I could get it. This can't reflect the values from the DAW, it just lets you know where everything is in each bank.


# Installation
You will need the following for this to work:
* LoopBe1 Internal MIDI Port
* MIDI-OX
* Python 2.6
* pygame

Install the above, and we can begin doing setup.


# Setup
1. Initiate LoopBe1's internal MIDI Port
2. Plug in your Launch Control XL
3. Open MIDI-OX
4. Open the MIDI Devices window in MIDI-OX and make sure you have Launch Control XL added as an input, and LoopBe Internal MIDI added as an output.
5. Switch your LCXL into User mode
6. Open the MIDI-OX Input Monitor. Play with some controls on the LCXL and confirm it is detecting input in MIDI OX
7. Open the MIDI-OX MIDI Port Routing interface.
8. Send Input Port "Launch Control XL" to Output Port "LoopBe Internal MIDI".
9. Open the MIDI-OX Output Monitor. Play with some controls on the LCXL and confirm that the output matches the input.
10. Launch the python script "lcxl_remap.py".
11. You should now see the LCXL blink and then turn off all the knob and button lights except for the User light.
12. Press the Track Select buttons to confirm the red bank light at the bottom moves, and tweak some knobs or faders to confirm their LEDs respond.
13. Open your DAW
14. Open the MIDI Input settings, and make sure it is listening to "LoopBe Internal MIDI", not "Launch Control XL"
15. Congrats, if all is working, you now have a MIDI controller with 256 distinct controls split across 8 banks. 
16. Open any VST and start mapping the controls. Have fun!


# Other Comments
* Be warned the toggle buttons in this mode turn into note-on/note-off toggles. I advise not touching them unless you want an annoying endless note. 
* This is obviously very barebones and simplistic, it is only intended to make this device a bit more ideal for mapping VSTs in FL Studio. 
* I have only tested this on FL Studio. I make no guarantees of compatibility with other DAWs, including Ableton since I don't use it.