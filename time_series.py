#----------------------------------------------------------------------------------------
# Module : time_series.py
#----------------------------------------------------------------------------------------
#
# Programmer : Benjamin Pieczynski
# 2024-04-10 18:18
#
#----------------------------------------------------------------------------------------
#
# This module houses the time series mode for building the time-series animations by
# making multiple plots with ts_plot. This code is based on the original ts_animator
# code.
#
#---------------------------------------------------------------------------------------

# imports
import os
from datetime import datetime, timedelta
from plot_command import run_ts_plot, run_ts_forecast
from operations import *
from defaults import *
from ts_utils import utc_days_difference, make_ts_time_array 

def ts_animator(args):
    
    # handle initial arguments
    measurement  = args['measurement'     ]
    instrument   = args['instrument'      ]
    time_range   = args['ts_range'        ]
    forecast     = args['forecast_time'   ]
    tomography   = args['tomography'      ]    
    search_dir   = args['search_directory'] # equivalent to tomography directory
    video_format = args['video_format'    ]
    img_format   = args['image_format'    ]
    parmfile     = args['parameter_file'  ]
    cmd_file     = args['command_file'    ]
    start_time   = args['start_time'      ]
    end_time     = args['end_time'        ]
    h            = args['step_size'       ]
    out_dir      = args['out_directory'   ] # default in parameter file
    outfile      = args['outfile'         ]
    bitrate      = args['bitrate'         ] # default in parameter file
    fps          = args['fps'             ] # default in parameter file
    delay        = args['delay'           ] # default in parameter file
    loop         = args['loop'            ] # default in parameter file
    try:
        bRemove = args['bRemove']
    except:
        bRemove = False
    
    #bResize      = args['bResize'         ] resizing not needed

    # read in parameters
    params = read_params(parmfile)

    # Adjust parameters for specific flags
    if search_dir == '0':
        search_dir = ''
    elif search_dir == None:
        search_dir = cwd
    if h != None:
        params['time_step'] = h
    if out_dir in [None, 'cwd']:
        out_dir = cwd
    elif out_dir != None:
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
    if outfile == None:
        outfile = f'{start_time}_{instrument}_{measurement}'
    
    # make output directory for temporary files
    temp_dir = f'temp_{instrument}_{measurement}'
    ts_out_dir = os.path.join(out_dir, temp_dir)
    if os.path.exists(ts_out_dir):
        subprocess.run(f'rm {ts_out_dir}')
    else:
        os.makedirs(ts_out_dir)
        
    # set time step
    if h == None:
        h = float(params['time_step'])
    else:
        h = float(h)

    # set forecast mode
    if time_range == None:
        print('\nTIME-SERIES - FORECAST MODE\n')
        past   = int(params['past'])
        future = int(params['future'])
        ts_time_array = make_ts_time_array(forecast, past, future, h)
        
        # loop through each time and build a time-series image
        matched_files = []
        for cur_time in ts_time_array:
            print(f'\nTS_PLOT: {cur_time}')
            fname = f'{cur_time}{img_format}'
            run_ts_forecast(measurement, instrument, forecast, tomography, search_dir, 
                            ts_out_dir, fname, cur_time)
            if video_format == 'MP4':
                matched_files.append(os.path.join(temp_dir, fname))
            else:
                matched_files.append(os.path.join(ts_out_dir, fname))
        
    else:
        print('\nTIME-SERIES - RANGE MODE\n')

        # set the start and end times if they were not provided
        if start_time == None:
            print('Setting start_time = time_range[0]')
            start_time = datetime.strptime(time_range.split('_')[0], "%Y%m%d%H")
        else:
            start_time = datetime.strptime(start_time, "%Y%m%d%H")
            
        if end_time == None:
            print('Setting start_time = time_range[1]')
            end_time = datetime.strptime(time_range.split('_')[1], "%Y%m%d%H")
        else:
            end_time = datetime.strptime(end_time, "%Y%m%d%H")
        
        # make time array for animated bar    
        ts_time_array = make_time_array(start_time, end_time, h)
        
        # make an image for each time in the time array
        matched_files = []
        for cur_time in ts_time_array:
            cur_time = cur_time[0:8] + cur_time[9:11]
            print(f'\nTS_PLOT: {cur_time}')
            fname = f'{cur_time}{img_format}'
            run_ts_plot(measurement, instrument, forecast, time_range, tomography, search_dir, 
                        ts_out_dir, fname, cur_time)
            if video_format == 'MP4':
                matched_files.append(os.path.join(temp_dir, fname))
            else:
                matched_files.append(os.path.join(ts_out_dir, fname))
        print('COMPLETE')

    # matched files
    print(matched_files)
    
    # MP4/GIF handler
    print('handling animation creation...')
    format_handler(cmd_file, out_dir, outfile, video_format, params, sorted(matched_files))

    # remove the temporary directory
    if bRemove:
        print(f'\nREMOVING: {ts_out_dir}')
        subprocess.run(f'rm -r {ts_out_dir}', shell=True, check=True)
    print('\nPROGRAM COMPLETE')

    # check file creation
    success = check_exists(out_dir, outfile)
    ext = '.mp4' if video_format == 'MP4' else '.gif'
    if success == True:
        print(f'Animation creation - SUCCESS\nanimation written')
        print('FILE LOCATION - {}\n'.format(os.path.join(out_dir,outfile+ext)))
    else:
        print('Animation creation - FAILED')
    return