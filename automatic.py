#-------------------------------------------------------------------
# MODULE: automatic.py
# BY: Benjamin Pieczynski (UCSD A&A: bpieczynsk@ucsd.edu)
# DATE: 2024-04-11T11:14
#
# PURPOSE:
#   Automatic mode for the iAnimate program. This was introduced 
#
# FUNCTIONS:
#   automatic_mode
#
#-------------------------------------------------------------------

# imports
import os
from datetime import datetime, timedelta, timezone
from operations import *
from defaults import *
from time_series import ts_animator

def automatic_mode(args: dict) -> None:
    """
    Runs the automatic version of the iAnimate program
    
    parameters
    ----------
    args: dict
        dictionary of arguments from argparse CLI
    
    modifications
    -------------
    2024-04-11 - Benjamin Pieczynski (added docstring, v3.0.0)
    """
    
    global cwd
    
    # System Arguments
    mode         = args['mode'            ]
    search_dir   = args['search_directory']
    pattern      = args['pattern'         ]
    video_format = args['video_format'    ]
    img_format   = args['image_format'    ]
    parmfile     = args['parameter_file'  ]
    cmd_file     = args['command_file'    ]
    start_time   = args['start_time'      ]
    end_time     = args['end_time'        ]
    h            = args['step_size'       ]
    listfile     = args['list_file'       ]
    out_dir      = args['out_directory'   ] # default in parameter file
    outfile      = args['outfile'         ]
    bitrate      = args['bitrate'         ] # default in parameter file
    fps          = args['fps'             ] # default in parameter file
    delay        = args['delay'           ] # default in parameter file
    loop         = args['loop'            ] # default in parameter file
    bResize      = args['bResize'         ]
    
    # if mode is 5 redirect it to time-series mode (for GUI)
    if mode == 5:
        ts_animator(args)
        return

    # read files
    params = read_params(parmfile)
    
    # Adjust parameters for specific flags
    if search_dir in ['0', None]:
        search_dir=''
    if h != None:
        params['time_step'] = h
    if out_dir.lower() in [None, 'cwd']:
        out_dir = cwd
    if out_dir != None:
        params['store_dir'] = out_dir
    else:
        out_dir = params['store_dir']
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
    
    elif mode == 4: # STANDARD MODE
        log_message = f'STANDARD MODE: No time specification'

    else: # FORECAST MODE (option 1)
        
        # get current time
        current_time = datetime.now(timezone.utc)
        
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
    
    if mode in [1, 2]: # INPUT IS NOT A LIST

        # Create time array
        write_to_log(params, 'MATCHING TIME ARRAY')
        time_array = make_time_array(start_time, end_time, h=h)
        len_times = len(time_array)
        log_message = f'COMPLETE...\n{len_times} DIFFERENT TIMES IN TIME ARRAY\n'
        write_to_log(params, log_message)

        if pattern != '0': # perform pattern search

            # Look for matched patterns
            write_to_log(params, 'MATCHING PATTERNS')
            matched_files = pattern_match(params, pattern, search_dir, 
                                          img_format=img_format)
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
        
    elif mode == 4:
        log_message = f'SEARCHING FOR PATTERN: {pattern} IN {search_dir}'
        write_to_log(params, log_message)
        matched_files = pattern_match(params, pattern, search_dir,
                                      img_format=img_format)
        log_message = 'FOUND {} FILES'.format(len(matched_files))
        write_to_log(params, log_message)

    else: # INPUT is a list
        write_to_log(params,'READING FILES LIST')
        matched_files = read_list(search_dir, listfile)
        log_message = 'FOUND {} FILES'.format(len(matched_files))
        write_to_log(params, log_message)
    
    # adjust image size if resize option is true
    if bResize:
        log_message = 'Adjusting matched image dimensions...'
        write_to_log(params, log_message)
        resize_images(matched_files)
    
    # Sort the matched files if they are not a listfile
    if listfile == None:
        matched_files = sorted(matched_files)
        
    # MP4/GIF handler
    format_handler(cmd_file, out_dir, outfile, video_format, params, matched_files)

    # check file creation
    success = check_exists(out_dir, outfile)
    ext = '.mp4' if video_format == 'MP4' else '.gif'
    if success == True:
        print(f'Animation creation - SUCCESS\nanimation written')
        log_message = 'PROCESS COMPLETE: FILE LOCATION - {}\n'.format(os.path.join(out_dir,outfile+ext))
    else:
        log_message = 'Animation creation failed...'
        print('Animation creation - FAILED')
    write_to_log(params, log_message)
    return