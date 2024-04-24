#----------------------------------------------------------------------------------------
# Program : Image Animator (MASTER PROGRAM)
#----------------------------------------------------------------------------------------
#
# Programmer : Benjamin Pieczynski
# Version - 3.0.0 2024-04-09
#
#----------------------------------------------------------------------------------------
#
# This program is the master version of the Image Animator program. The program compiles
# png files stored in various ways to build a animation using the ffmpeg linux
# program. This version has support for manual, automated, or listed image input.
# Via command-line arguments one can specify the mode. This program expands on the use
# of animator.parm files and adds the instruct.command file for more control over
# ffmpeg command construction. Added in version 3.0.0 is a Graphic User Interface that
# utilizes all features. In addition to adding a GUI, I have added a time-series option
# to build animations from our time-series plot using ts-plot. 
#
#---------------------------------------------------------------------------------------
# 
# Modification History
# v1.0: Benjamin Pieczynski 2023-12-21
# v2.0: Benjamin Pieczynski 2024-01-25
# v3.0: Benjamin Pieczynski 2024-04-09
#
#----------------------------------------------------------------------------------------
# imports
import sys
from defaults import *
from manual import manual_mode
from automatic import automatic_mode
from graphic_interface import gui_mode
from time_series import ts_animator
from operations import *
#----------------------------------------------------------------------------------------

# Main function

def main(args):
    
    #print(f'IMAGE ANIMATOR - VERSION {version}')
    #print('WRITTEN BY: BENJAMIN PIECZYNSKI')
    #print('INITIAL VERSION: 12.15.2023')
    #print(f'UPDATED: {release_date}')
    
    # Create list of keys to the args dictionary
    args = parser.parse_args().__dict__
    
    mode = args['mode']
    
    print('\n------------------------------------------')
    print(f'\nPROGRAM:  {fullname}')
    print(f'BY:       {programmer}')
    print(f'RELEASED: {release_date}\n')
    print('------------------------------------------')
    
    # mode selection 0 -> MANUAL MODE
    if mode==0:
        print('\n   SELECTED - MANUAL MODE\n')
        print('------------------------------------------')
        manual_mode()
    elif mode in [1, 2, 3, 4]:
        print('\n   SELECTED - AUTOMATIC MODE\n')
        print('------------------------------------------')
        automatic_mode(args)
    elif mode == 5:
        print('\n SELECTED - TIMES SERIES MODE\n')
        print('------------------------------------------')
        ts_animator(args)
    elif mode == 6:
        print('\n   SELECTED - GUI MODE\n')
        print('------------------------------------------')
        gui_mode()
    else:
        print('ERROR: MODE 0,1,2,3 NOT SELECTED')

#----------------------------------------------------------------------------------------

# init
if __name__ == "__main__":
    args = sys.argv
    main(args)
