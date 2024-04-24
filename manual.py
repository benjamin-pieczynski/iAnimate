#----------------------------------------------------------------------------------------
# Module : manual.py
#----------------------------------------------------------------------------------------
#
# Programmer : Benjamin Pieczynski
# 2024-04-10 18:18
#
#----------------------------------------------------------------------------------------
#
# This module houses the manual mode for the iAnimate program. This was separated from
# directives.py in version 3.0.0. The manual version of the program asks the user for
# inputs via command line. The program will check the users input and ask them to
# resubmit if an error occurs in the input.
#
# Added to version 3.0.0
# - unlimited patterns can be entered with the * separator 
#   (pattern1*pattern2*...*patternN)
# - resizing options to make sure all images have even dimensions (ffmpeg struggles with
#   odd dimensions, previously requiring different command files)
#
#---------------------------------------------------------------------------------------

# imports
import os
from datetime import datetime, timedelta, timezone
from operations import *
from defaults import *
#----------------------------------------------------------------------------------------

# Mode Specific (Manual / Automatic)
def manual_mode() -> None:
    """
    Runs the manual version of the iAnimate program.
    
    modifications
    -------------
    2024-04-10 - Benjamin Pieczynski (added docstring, v3.0.0)
    """
    
    global cwd
    
    # load in parameters
    params = read_params(default_param)

    # Basic user inputs
    out_dir = input("Please enter the desired output directory in the format /home/user/output_directory (default - current directory): ").strip() or cwd
    print('out_dir: ', out_dir)
    outfile = input("Please enter a name for the output file (do not include file extension): ").strip() or "animate_output"
    print('outfile: ',outfile)
    
        # inputs for MP4 and GIF options
    cond = False # condition to check for correct format input
    while cond==False:
        format_choice = input("Please select one of the following format options...\n 1 - GIF \n 2 - MP4\n... ").strip()
        print('format_choice: ', format_choice)
        if format_choice not in ['1','2']:
            print("ERROR: Search Choice must be '1' or '2'")
        else:
            if format_choice == '1':
                format_choice = 'GIF'
            elif format_choice == '2':
                format_choice = 'MP4'
            cond=True
    
    # GIF user inputs
    if format_choice=='GIF':
        print('\nGIF option selected...')
        delay = input('Enter delay (default is 20): ').strip()
        delay = int(delay) if delay else 20
        print('delay: {}'.format(delay))
        params['delay'] = delay
        loop = input('Enter loop (default is 0-endless): ').strip()
        loop = int(loop) if loop else 0
        print('loop: {}\n'.format(loop))
        params['loop'] = loop
        cmd_file = None
    
    # MP4 user inputs
    elif format_choice=='MP4':
        print('MP4 option selected...\n')
        cmd_file = input('PLEASE SELECT COMMAND FILE (Enter = Default)').strip() or default_command
        fps = input('Enter FPS (default is 10): ').strip()
        fps = int(fps) if fps else 10
        print('FPS: {}'.format(fps))
        params['fps'] = fps
        bitrate = input('Enter video bitrate in kbps (default is 1000): ').strip()
        bitrate= int(bitrate) if bitrate else 1000
        print('Bitrate: {}'.format(bitrate))
        params['bitrate'] = bitrate
        cond = True
        while cond:
            resize_in = input('Would you like to resize the images to even dimensions? (Y/N): ').strip().upper()
            if resize_in in ['Y', 'YES', 'TRUE', 'T', '1']:
                bResize = True
                break
            elif resize_in in ['N', 'NO', 'FALSE', 'F', '0']:
                bResize = False
                break
            else:
                pass
        print(f'RESIZE IMAGES = {bResize}\n')
        
    print()
    
    # Conditional input for search choice
    cond = False
    while cond==False:
        print("Please select one of the following options...\n--------------------------------------------------")
        search_choice = input(" 1 - Select All .PNG files \n 2 - Select .PNG files by pattern\n 3 - Files List\n... ").strip()
        print('SEARCH_CHOICE: ', search_choice)
        if search_choice not in ['1','2','3']:
            print("ERROR: Search Choice must be '1' or '2' or '3'")
        else:
            search_choice = int(search_choice)
            cond=True
    
    if search_choice in [1,2]:
        cond = False
        while cond==False:
            print("\nPlease select a time option...\n--------------------------------------------------")
            print(' 1 - FORECAST MODE (3 days prior / 4 days ahead)')
            print(' 2 - RANGE MODE (Select all images within a given time period)')
            print(' 3 - NONE (time is not considered in image selection)')
            try:
                time_choice = int(input('ENTER CHOICE: ').strip())
                if time_choice not in [1, 2, 3]:
                    print('ERROR: must select options 1, 2, or 3')
                else:
                    cond = True
            except:
                print('Error: Time choice must be an integer')
    
        # Store time parameters
        time_parms = {}
        print('\nUser has selected option {}'.format(time_choice))
        if time_choice==1:
            print('FORECAST MODE SELECTED')
            parmfile = input('\nPlease enter a parameter file:').strip() or default_param
            params = read_params(parmfile)
            time_parms['current_time']  = datetime.now(timezone.utc)
            time_parms['end_time']      = time_parms['current_time'] + timedelta(days=params['future'])
            time_parms['start_time']    = time_parms['current_time'] - timedelta(days=params['past'])
            time_parms['time_step']     = params['time_step']
            print('START DATE: {} | END DATE: {} | TIME STEP {} hours\n'.format(time_converter(time_parms['start_time']),
                                                                                        time_converter(time_parms['end_time']),
                                                                                        time_parms['time_step']))

        elif time_choice==2:
            cond = False
            print('RANGE MODE SELECTED')

            # enter the start date
            while cond == False:
                # User input for date
                start_date = input("Enter the START DATE in YYYY-MM-DD-HH:MM  format: ")

                # Convert user input to UTC timestamp
                try:
                    time_parms['start_time'] = datetime.strptime(start_date, "%Y-%m-%d-%H:%M")
                    print(f"START DATE: {time_converter(time_parms['start_time'])}")
                    cond = True
                except ValueError:
                    print("Invalid date format. Please enter date in YYYY-MM-DD-HH:MM format.")

            # enter the end date
            cond = False
            while cond == False:
                # User input for date
                end_date = input("Enter the END DATE in YYYY-MM-DD-HH:MM  format: ")

                # Convert user input to UTC timestamp
                try:
                    time_parms['end_time'] = datetime.strptime(end_date, "%Y-%m-%d-%H:%M")
                    print(f"END DATE: {time_converter(time_parms['end_time'])}")
                    cond = True
                except ValueError:
                    print("Invalid date format. Please enter date in YYYY-MM-DD-HH:MM format.")

            # enter the time step parameters
            cond = False
            while cond == False:
                h = input(f'Please enter a step size in hours (must be a multiple of 6): ')
                try:
                    time_parms['time_step'] = float(h)
                    print(f"TIME STEP: {time_parms['time_step']} hours")
                    cond = True
                except:
                    print('Please enter a real positive number for the time step...')

        elif time_choice==3:
            print('NO TIME OPTION SELECTED')
        else:
            print('TIME CHOICE ERROR')
            
        # Select .PNG files based on pattern
        if search_choice == 2:
            pattern = input('Please input a pattern (format patternA*patternB): ').strip()
            search_dir = input('Please enter search directory (default is cwd): ').strip() or cwd
            print(f'Search Directory: {search_dir}')
            matched_files = pattern_match(params, pattern, search_dir)
        # Select all .PNG files within the current directory
        elif search_choice == 1:
            search_dir = input('Enter search directory (default is current): ') or cwd
            matched_files = os.listdir(search_dir)
            matched_files = [f'{search_dir}/{file}' for file in matched_files if file.lower().endswith('.png')]
            print('FOUND {} MATCHED FILES'.format(len(matched_files)))

        # From the matched files, select the options with a matching timestamp if time mode is available
        if time_choice == 3:
            print('NO TIME MODE SELECTED... MOVING TO NEXT PROCESS...\n')
        else:
            time_array = make_time_array(time_parms['start_time'], time_parms['end_time'],h=time_parms['time_step'])
            matched_files = match_times(matched_files, time_array)
            
        # Sort the matched files
        matched_files = sorted(matched_files)
            
    elif search_choice == 3:
            print('LIST MODE SELECTED')
            search_dir = input("Please enter the desired input directory in the format /home/user/input_directory (default - 0 use file paths): ").strip() or '0'
            if search_dir == '0':
                print('paths included')
            else:
                print('search_dir: ', search_dir)
            img_listfile = input("Please enter the name of the input  list file (default - image_list.txt): ").strip() or 'image_list.txt'
            print('image list file: ', img_listfile)
            
            matched_files = read_list(search_dir, img_listfile)
            
    # resize located images if the resizing option is utilized
    if format_choice == 'MP4':
        resize_images(matched_files) if bResize else None
    
    format_handler(cmd_file, out_dir, outfile, format_choice, params, matched_files)
    success = check_exists(out_dir, outfile)
    if success:
        print(f'Animation creation - SUCCESS\nanimation written')
    else:
        print('Animation creation - FAILED')
    return