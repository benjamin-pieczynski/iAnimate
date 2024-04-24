#----------------------------------------------------------------------------------------
# Module : directives
#----------------------------------------------------------------------------------------
#
# Programmer : Benjamin Pieczynski
# 01/25/2024
#
#----------------------------------------------------------------------------------------
#
# This module is used by the main Image Animator program to run either the 
# manual, automatic, or list mode versions of the animation program. These
# are considered to be the mode specific options of the program.
#
#---------------------------------------------------------------------------------------
# imports
import os
from datetime import datetime, timedelta
from operations import *
from defaults import *
#----------------------------------------------------------------------------------------

# Mode Specific (Manual / Automatic)
def manual_mode():
    
    global cwd
    
    # Basic user inputs
    out_dir = input("Please enter the desired output directory in the format /home/user/output_directory (default - current directory): ").strip() or cwd
    print('out_dir: ', out_dir)
    outfile = input("Please enter a name for the output file (do not include file extension): ").strip() or "animate_output"
    print('outfile: ',outfile)
    
        # inputs for MP4 and GIF options
    cond = False # condition to check for correct format input
    params = {} # dictionary to store params
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
        print('Bitrate: {}\n'.format(bitrate))
        params['bitrate'] = bitrate
        
    print()
    
    # Conditional input for search choice
    cond = False
    while cond==False:
        print("Please select one of the following options...\n--------------------------------------------------")
        search_choice = input(" 1 - Select All .PNG files in the Current Directory \n 2 - Select .PNG files by pattern\n 3 - Files List\n... ").strip()
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
            time_choice = input('ENTER CHOICE: ')
            if time_choice not in ['1','2','3']:
                print('ERROR: must select options 1, 2, or 3')
            else:
                time_choice = int(time_choice)
                cond = True
    
        # Store time parameters
        time_parms = {}
        print('\nUser has selected option {}'.format(time_choice))
        if time_choice==1:
            print('FORECAST MODE SELECTED')
            parmfile = input('\nPlease enter a parameter file:').strip() or default_param
            params = read_params(parmfile)
            time_parms['current_time']  = datetime.utcnow()
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
            matched_files = pattern_match()

        # Select all .PNG files within the current directory
        elif search_choice == 1:
            cwd = os.getcwd()
            print(cwd)
            matched_files = os.listdir()
            matched_files = [f'{cwd}/{file}' for file in matched_files if file.lower().endswith('.png')]
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
    
    format_handler(cmd_file, out_dir, outfile, format_choice, params, matched_files)
    
    return

def automatic_mode(args):

    # System Arguments
    mode       = args['mode'            ]
    search_dir = args['search_directory']
    pattern    = args['pattern'         ]
    img_format = args['image_format'    ]
    parmfile   = args['parameter_file'  ]
    cmd_file   = args['command_file'    ]
    start_time = args['start_time'      ]
    end_time   = args['end_time'        ]
    h          = args['step_size'       ]
    listfile   = args['list_file'        ]
    out_dir    = args['out_directory'   ] # default in parameter file
    outfile    = args['outfile'         ]
    bitrate    = args['bitrate'         ] # default in parameter file
    fps        = args['fps'             ] # default in parameter file
    delay      = args['delay'           ] # default in parameter file
    loop       = args['loop'            ] # default in parameter file
    
    # read files
    params = read_params(parmfile)
    
    # Adjust parameters for specific flags
    if search_dir=='0':
        search_dir=''
    if h != None:
        params['time_step'] = h
    if out_dir != None:
        params['store_dir'] = out_dir
    if bitrate != None:
        params['bitrate'] = bitrate
    if fps != None:
        params['fps'] = fps
    if delay != None:
        params['delay'] = delay
    if loop != None:
        params['loop'] = loop
    
    # check user logs
    check_logs(params)
    
    if mode == 2: # RANGE MODE

        # get parameters
        if (start_time != None) and (end_time != None):
            start_time  = datetime.strptime(start_time, '%Y-%m-%d-%H:%M')
            end_time    = datetime.strptime(end_time, '%Y-%m-%d-%H:%M')
            h           = float(params['time_step'])
        else:
            print('ERROR: When LIST MODE is active you must provide the start and end times')
            log_message = ('ERROR: When LIST MODE is active you must provide the start and end times')
            write_to_log(params, log_message)
            return
        log_message = f'RANGE MODE: user input\n    --- START {start_time} | END {end_time} | TIME_STEP {h} ---'
        
    elif mode == 3: # LIST MODE
        log_message = f'LIST MODE: list input\n     --- LISTFILE {listfile}'

    else: # FORECAST MODE (option 1)
        
        # get current time
        current_time = datetime.utcnow()
        
        # use parameters
        past         = float(params['past']     )
        future       = float(params['future']   )
        h            = float(params['time_step'])
        if outfile == None:
            outfile      = '{}'.format(pattern.replace('*', ''))
        
        # get times for time array
        start_time = current_time - timedelta(days=past)
        end_time   = current_time + timedelta(days=future)
        
        log_message = f'FORECAST MODE: IPS REQUEST\n    --- START {start_time} | END {end_time} | TIME_STEP {h} ---'
    
    # Write mode selection
    write_to_log(params, log_message)
    
    if mode != 3: # INPUT IS NOT A LIST

        # Create time array
        write_to_log(params, 'MATCHING TIME ARRAY')
        time_array = make_time_array(start_time, end_time, h=h)
        len_times = len(time_array)
        log_message = f'COMPLETE...\n{len_times} DIFFERENT TIMES IN TIME ARRAY\n'
        write_to_log(params, log_message)

        if pattern != '0': # perform pattern search

            # Look for matched patterns
            write_to_log(params, 'MATCHING PATTERNS')
            matched_files = pattern_match(params, pattern, search_dir)
            len_matched = len(matched_files)
            log_message = f'FOUND {len_matched} MATCHING PATTERNS'
            write_to_log(params, log_message)

            # find the matched files
            write_to_log(params,'MATCHING TIMES')
            matched_files = match_times(matched_files, time_array)
            len_matched = len(matched_files)
            log_message = f'FOUND {len_matched} MATCHING TIMES'
            write_to_log(params, log_message)
        
        else:  # no pattern provided / no pattern search
            matched_files = structured_search(search_dir, time_array)
        
    else: # INPUT is a list
        write_to_log(params,'READING FILES LIST')
        matched_files = read_list(search_dir, listfile)
        log_message = 'FOUND {} FILES'.format(len(matched_files))
        write_to_log(params, log_message)
                    
    # MP4/GIF handler
    ext = '.mp4' if img_format=='MP4' else '.gif'
    format_handler(cmd_file, out_dir, outfile, img_format, params, matched_files)
    log_message = 'PROCESS COMPLETE: FILE LOCATION - {}{}\n'.format(os.path.join(out_dir,outfile), ext)
    write_to_log(params, log_message)
        
    return