#MIT License
#
#Copyright (c) 2018 Luis Victor Muller Fabris
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#In this file we declare the toolbar itens that are specific to the spectrometer.
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------


#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#Import necessary modules here.



#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#Always import the folowing module.
from ui_headers import *
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#We will use configfile to save the values in the widgets defined below to disk.
#The argument passed to initconfig must not be used in other module and can not contain "/"
#or any other character that can't be in a file name (for exemple the null character)
configfile=initconfig("Generic")
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#Below we add the widgets that we want in the toolbar that are device specific
label = Gtk.Label("F:")

tool_itemc = Gtk.ToolItem()
tool_itemc.add(label)
labelb = Gtk.Label("")

tool_itemd = Gtk.ToolItem()
tool_itemd.add(labelb)




labeltriggerlevel = Gtk.Label("Tr:")
tool_itemtriggerlevel = Gtk.ToolItem()
tool_itemtriggerlevel.add(labeltriggerlevel)


labelpointsbefore = Gtk.Label("Pre:")
tool_itempointsbefore = Gtk.ToolItem()
tool_itempointsbefore.add(labelpointsbefore)


labelpointsafter = Gtk.Label("Aft:")
tool_itempointsafter = Gtk.ToolItem()
tool_itempointsafter.add(labelpointsafter)

tool_itemb = Gtk.ToolItem()
adjustment = Gtk.Adjustment(value=0,lower=0,upper=5,step_increment=0.01,page_increment=0.01)
entry = Gtk.SpinButton(adjustment=adjustment, digits=3)
#Fix a bug in some GTK themes (For example Mint-Y) that causes the buttons to disappear (white background and text in white text entry) when the spin button has focus.
entry.get_style_context().remove_class(Gtk.STYLE_CLASS_SPINBUTTON)
entry.set_numeric(True)
entry.set_width_chars(4)
tool_itemb.add(entry)


tool_itembb = Gtk.ToolItem()
adjustmentb = Gtk.Adjustment(value=1,lower=1,upper=128,step_increment=1,page_increment=1,page_size=10)
entryb = Gtk.SpinButton(adjustment=adjustmentb, digits=0)
#Fix a bug in some GTK themes (For example Mint-Y) that causes the buttons to disappear (white background and text in white text entry) when the spin button has focus.
entryb.get_style_context().remove_class(Gtk.STYLE_CLASS_SPINBUTTON)
entryb.set_numeric(True)
entryb.set_width_chars(3)
tool_itembb.add(entryb)



tool_itembbb = Gtk.ToolItem()
adjustmentbb = Gtk.Adjustment(value=100,lower=100,upper=600,step_increment=1,page_increment=1,page_size=10)
entrybb = Gtk.SpinButton(adjustment=adjustmentbb, digits=0)
#Fix a bug in some GTK themes (For example Mint-Y) that causes the buttons to disappear (white background and text in white text entry) when the spin button has focus.
entrybb.get_style_context().remove_class(Gtk.STYLE_CLASS_SPINBUTTON)
entrybb.set_numeric(True)
entrybb.set_width_chars(3)
tool_itembbb.add(entrybb)


freq = Gtk.ListStore(int, str)
tool_itemcombo = Gtk.ToolItem()
tool_itemlabelcombo = Gtk.ToolItem()
tool_itemlabelaverages = Gtk.ToolItem()
#tool_itemlabelaverages.add(labeld)
freq_combo = Gtk.ComboBox.new_with_model(freq)
renderer_textb = Gtk.CellRendererText()
freq_combo.pack_start(renderer_textb, True)
freq_combo.add_attribute(renderer_textb, "text", 1)
tool_itemcombo.add(freq_combo)
#tool_itemlabelcombo.add(labelc)
freq.append([1, "10KHz 128"])
freq.append([2, "19KHz 64"])
freq.append([3, "38KHz 32"])
freq.append([4, "77KHz 16"])
#freq.append([5, "153KHz 8"])
#freq.append([6, "307KHz 4"])
#freq.append([7, "615KHz 2"])
freq_combo.set_active(0)

tool_itemrising = Gtk.ToolItem()
button = Gtk.ToggleButton()
img=Gtk.Image.new_from_file('spectrometer_modules/generic/rb.png')
button.set_image(img)
tool_itemrising.add(button)

tool_itemfalling = Gtk.ToolItem()
buttonb = Gtk.ToggleButton()
img=Gtk.Image.new_from_file('spectrometer_modules/generic/fb.png')
buttonb.set_image(img)
tool_itemfalling.add(buttonb)
button.set_active(True)

#Here we will load the values from the configuration file into the widgets.
#We use the try/except do avoid errors if the value stored is not an float/int or if there is no value stored yet.
vsettings="1"
try:
	vsettings=float(configfile['4'])
except:
	configfile['4']=""
if(str(vsettings)+""!=""):
	entry.set_value(float(vsettings))
vsettings="1"
try:
	vsettings=float(configfile['5'])
except:
	configfile['5']=""
if(str(vsettings)+""!=""):
	entryb.set_value(float(vsettings))
vsettings="100"
try:
	vsettings=float(configfile['6'])
except:
	configfile['6']=""
if(str(vsettings)+""!=""):
	entrybb.set_value(float(vsettings))


vsettings="1"
try:
	vsettings=float(configfile['1'])
except:
	configfile['1']=""
if(str(vsettings)+""!=""):
	freq_combo.set_active(int(vsettings))
configfile.close()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
#The folowing function receives the toolbar object and insert the widgets declared before in order.
#This function must always be declared here.
def additems(toolbar):
	toolbar.insert(tool_itemrising,0)
	toolbar.insert(tool_itemfalling,0)
	toolbar.insert(tool_itemd,0)
	toolbar.insert(tool_itemcombo,0)
	toolbar.insert(tool_itemc,0)
	toolbar.insert(tool_itemb,0)
	toolbar.insert(tool_itemtriggerlevel,0)
	toolbar.insert(tool_itembb,0)
	toolbar.insert(tool_itempointsbefore,0)
	toolbar.insert(tool_itembbb,0)
	toolbar.insert(tool_itempointsafter,0)
	#toolbar.insert(tool_itemlabelaverages,0)
	pass
#The folowing function sends the values from the widgets to the main program. This values will be returned to the spectrometer data acquisition function.
#Please don't use any separator in the string other than ; because this string will be concatenated later.
#This function must always be declared here.
def gettoolbarvalues():
	trigmode=0
	if(button.get_active()==1):
		if(buttonb.get_active()==0):
			trigmode=0 #rising
	if(button.get_active()==0):
		if(buttonb.get_active()==1):
			trigmode=1 #failing
	if(button.get_active()==1):
		if(buttonb.get_active()==1):
			trigmode=2
	gettoolbarvaluesreturnvalue=""
	gettoolbarvaluesreturnvalue=gettoolbarvaluesreturnvalue+str(freq_combo.get_model()[freq_combo.get_active_iter()][:2][0]-1)+";"
	gettoolbarvaluesreturnvalue=gettoolbarvaluesreturnvalue+str(trigmode)+";"
	gettoolbarvaluesreturnvalue=gettoolbarvaluesreturnvalue+str(buttonb.get_active())+" "
	gettoolbarvaluesreturnvalue=gettoolbarvaluesreturnvalue+str(float(entry.get_value()))+" "
	gettoolbarvaluesreturnvalue=gettoolbarvaluesreturnvalue+str(int(entryb.get_value()))+" "
	gettoolbarvaluesreturnvalue=gettoolbarvaluesreturnvalue+str(int(entrybb.get_value()))+";"
	return gettoolbarvaluesreturnvalue
#This function returns an array with the widgets that the user can change values. The "changed" event will be connected to this widgets.
#This function must always be declared here.
def getchangedeventelements():
	returnarray=[None] * 4
	returnarray[0]=freq_combo
	returnarray[1]=entry
	returnarray[2]=entryb
	returnarray[3]=entrybb
	return returnarray
#Emit event on entry, single togglebutton event is not compatible with spectraread on above function.
def eventbutton(self):
	if(button.get_active()==0):
		if(buttonb.get_active()==0):
			button.set_active(True)
	entry.set_value(entry.get_value()+1)
	entry.set_value(entry.get_value()-1)
button.connect("toggled",eventbutton)
buttonb.connect("toggled",eventbutton)
#This function is called when some value on a widget changes.
#Here we will store the new values on the configuration file.
#This function must always be declared here.
def changedelement():
	configfile=initconfig("Generic")
	configfile['1']=str(freq_combo.get_model()[freq_combo.get_active_iter()][:2][0]-1)
	configfile['2']=str(button.get_active())
	configfile['3']=str(buttonb.get_active())
	configfile['4']=str(float(entry.get_value()))
	configfile['5']=str(int(entryb.get_value()))
	configfile['6']=str(int(entrybb.get_value()))
	configfile.close()
#This function removes all the toolbar buttons from the toolbar.
#This function is called when the user changes the spectrometer in the botton left combo box.
#This function must always be declared here.
def removeallwidgets(toolbar):
	toolbar.remove(tool_itemrising)
	toolbar.remove(tool_itemfalling)
	toolbar.remove(tool_itemd)
	toolbar.remove(tool_itemcombo)
	toolbar.remove(tool_itemc)
	toolbar.remove(tool_itemb)
	toolbar.remove(tool_itemtriggerlevel)
	toolbar.remove(tool_itembb)
	toolbar.remove(tool_itempointsbefore)
	toolbar.remove(tool_itembbb)
	toolbar.remove(tool_itempointsafter)
def getdevicelist():
	return ["01"]
