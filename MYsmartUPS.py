#!/usr/bin/env python
#
# Copyright (c) 2014 OpenElectrons.com
# SmartUPS Python class.
# for more information about SmatUPS,  please visit:
# http://www.openelectrons.com/pages/33
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
# History:
# Date      Author      Comments
# 02/26/13    Nitin Patil    Initial authoring.
# 05/22/14    Michael Giles  SmartUPS conversion, error handling
# 06/20/14    Michael Giles  customer ready
# 
#
# this is driver for the driveing Openelectrons.com PiLight with any RGB values 
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

## @package smartups
# This is the OpenElectrons_i2c module for SmartUPS.

from OpenElectrons_i2c import OpenElectrons_i2c
import time

## SmartUPS: this class provides functions for SmartUPS
#  for read and write operations.
class SmartUPS(OpenElectrons_i2c):
    #"""Class for the SmartUPS"""

    # Minimal constants required by library
    
    I2C_ADDRESS = (0x24)  
    
    SmartUPS_WHO_AM_I    =  0x10
    SmartUPS_VERSION    =  0x00
    SmartUPS_VENDOR    =  0x08
    
    SmartUPS_COMMAND  = 0x41
    SmartUPS_RESTART_OPTION  =  0x42
    SmartUPS_BUTTON_CLICK   =  0x43
    SmartUPS_RESTART_TIME   =  0x44
    SmartUPS_STATE   =  0x46
    SmartUPS_BAT_CURRENT   =  0x48
    SmartUPS_BAT_VOLTAGE   =  0x4a
    SmartUPS_BAT_CAPACITY   =  0x4c
    SmartUPS_TIME   =  0x4e
    SmartUPS_BAT_TEMPERATURE   =  0x50
    SmartUPS_BAT_HEALTH   =  0x51
    SmartUPS_OUT_VOLTAGE   =  0x52
    SmartUPS_OUT_CURRENT   =  0x54
    SmartUPS_MAX_CAPACITY   =  0x56
    SmartUPS_SECONDS   = 0x58 
    
    ## Initialize the class with the i2c address of the SmartUPS
    #  @param self The object pointer.
    #  @param i2c_address Address of your SmartUPS.
    def __init__(self, address = I2C_ADDRESS):
        OpenElectrons_i2c.__init__(self, address >> 1)  
    
    ## Reads the SmartUPS battery voltage values
    #  @param self The object pointer.
    def readBattVoltage(self):
        try:
            value = self.readInteger(self.SmartUPS_BAT_VOLTAGE)
            return value   
        except:
            print "Error: Could not read battery voltage"
            return ""
        
    ## Reads the SmartUPS battery current values
    #  @param self The object pointer.
    def readBattCurrent(self):
        try:
            value = self.readIntegerSigned(self.SmartUPS_BAT_CURRENT)
            return value
        except:
            print "Error: Could not read battery current"
            return ""
    
    ## Reads the SmartUPS battery temperature values
    #  @param self The object pointer.
    def readBattTemperature(self):
        try:
            value = self.readByte(self.SmartUPS_BAT_TEMPERATURE)
            return value
        except:
            print "Error: Could not read battery temperature"
            return ""
    
    ## Reads the SmartUPS battery capacity values
    #  @param self The object pointer.
    def readBattCapacity(self):
        try:
            value = self.readInteger(self.SmartUPS_BAT_CAPACITY)
            return value
        except:
            print "Error: Could not read battery capacity"
            return ""        
    
    ## Reads the SmartUPS battery estimated time values
    #  @param self The object pointer.
    def readBattEastimatedTime(self):
        try:
            value = self.readInteger(self.SmartUPS_TIME)
            return value
        except:
            print "Error: Could not read battery estimated time"
            return ""        
        
    ## Reads the SmartUPS battery health values
    #  @param self The object pointer.
    def readBattHealth(self):
        try:
            value = self.readByte(self.SmartUPS_BAT_HEALTH)
            return value
        except:
            print "Error: Could not read battery health"
            return ""
    
    ## Reads the SmartUPS battery state
    #  @param self The object pointer.
    def readBattState(self):
        try:
            state = ["IDLE", "PRECHARG" ,"CHARGING","TOPUP","CHARGED","DISCHARGING","CRITICAL","DISCHARGED","FAULT","SHUTDOWN" ]
            value = self.readByte(self.SmartUPS_STATE)
            return state[value]
        except:
            print "Error: Could not read battery state"
            return ""
        
    ## Reads the SmartUPS button click status values
    #  @param self The object pointer.
    def readButtonClick(self):
        try:
            value = self.readByte(self.SmartUPS_BUTTON_CLICK)
            if value != None:
                return value
            else:
                return chr(value)
        except:
            print "Error: Could not read button click"
            return ""
            
    ## Reads the SmartUPS output voltage values
    #  @param self The object pointer.
    def readOutputVoltage(self):
        try: 
            value = self.readInteger(self.SmartUPS_OUT_VOLTAGE)
            return value
        except:
            print "Error: Could not read output voltage"
            return ""        
        
    ## Reads the SmartUPS output current values
    #  @param self The object pointer.
    def readOutputCurrent(self):
        try:
            value = self.readIntegerSigned(self.SmartUPS_OUT_CURRENT)
            return value
        except:
            print "Error: Could not read output current"
            return ""        
    
    ## Reads the SmartUPS battery maximum capacity values
    #  @param self The object pointer.
    def readMaxCapacity(self):
        try:
            value = self.readInteger(self.SmartUPS_MAX_CAPACITY)
            return value 
        except:
            print "Error: Could not read maximum capacity"
            return ""        

    ## Reads the SmartUPS time in seconds
    #  @param self The object pointer.
    def readSeconds(self):
        try:
            value = self.readLong(self.SmartUPS_SECONDS)
            return value
        except:
            print "Error: Could not read seconds"
            return ""
        
    ## Reads the SmartUPS charged values
    #  @param self The object pointer.
    def readCharged(self):
        try: 
            value = self.readInteger(self.SmartUPS_BAT_CAPACITY)*100/(1+self.readInteger(self.SmartUPS_MAX_CAPACITY))
            return value
        except:
            print "Error: Could not read battery charged value"
            return ""
        
