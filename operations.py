#----------------------------------------------------------------------------------------
# Module : operations
#----------------------------------------------------------------------------------------
#
# Programmer : Benjamin Pieczynski
# 01/25/2024
#
#----------------------------------------------------------------------------------------
#
# This module is used by the main Image Animator program to run functions
# responsible for program operations. This is the lowest level code within
# the modules.
#
# MODIFICATIONS
#   v3.0.0 (2024-04-09) fixed deprication of utc.now with time
#---------------------------------------------------------------------------------------

# imports
import os
import subprocess
from datetime import datetime, timedelta, timezone
#----------------------------------------------------------------------------------------

def update_progress_bar(message: str, n_comp: int, n_len: int, optional: str ='',
                        reg: bool = True, newline: bool = False) -> None:
    """
    Update the user with a print statement that displays a progress bar.
    
    parameters
    ----------
    message: str
        program message
    n_comp: int
        number completed
    n_len: int 
        length of the array that must be processed.
    optional: str
        additional progress message
    reg: bool
        whether to return register to start of line.
    newline: bool
        if True, after this update go to the next line.
    """

    # check progress and build progress statement
    pid      = os.getpid()
    per_comp = int(100*n_comp / n_len)
    arrows   = '>' * (per_comp // 5)
    arrows   = arrows.ljust(20)
    per_comp = str(per_comp).rjust(3)
    prog_s   = f'({pid}) {message}:[{arrows}] progress - {per_comp}% {optional}'
    
    # if register return location
    if reg == True:
        print('\r' + ' ' * 100, end='')  # Clear previous line
        print('\r' + prog_s, end='')
    else:
        print(prog_s)
    
    if newline == True:
        print('\n')
    return

# read in parameters files
def read_params(parmfile: str) -> dict:
    """
    Reads in selected parameter file.
    
    parameters
    ----------
    parmfile: str
        path to parameter file.
    
    returns
    -------
    params: dict
        dictionary containing parameters specified in the parameter file.
        
    modifications
    -------------
    2024-04-10 - Benjamin Pieczynski (added docstring)
    """
    # create a dictionary to store global variables
    params = {}
    
    # open the parameter file and loop through each line to store each variable
    f = open(parmfile, 'r')
    for line in f:
        line = line.split(':')
        params[line[0].strip()] = line[1].strip()
    f.close()
    return params

# read ffmpeg command file
def read_commands(input_list: list, fps: int, 
                  bitrate: int, out_dir: str, 
                  outfile: str, command_file: str):
    """
    reads in the commands from the command files.
    
    parameters
    ----------
    input_list: str
        list of inputs from the program
    fps: int
        frames per second
    bitrate: int
        bitrate in kbs (kilobytes seconds)
    out_dir: str
        output directory
    outfile: str
        output file
    command_file: str
        path to command file
        
    returns
    -------
    ffmpeg_command: list[str]
        a list of strings that make up the ffmpeg command
    
    modifications
    -------------
    2024-04-10 - Benjamin Pieczynski (added docstring)
    """
    ffmpeg_command = []
    f = open(command_file,'r')
    info = f.read()
    info = info.strip().split(',')
    for i in info:
        if 'fps' in i:
            ffmpeg_command.append(str(fps))
        elif 'input_list' in i:
            ffmpeg_command.append(str(input_list))
        elif 'bitrate' in i:
            ffmpeg_command.append(str(bitrate)+'k')
        elif 'outfile' in i:
            ffmpeg_command.append(str('{}.mp4'.format(os.path.join(out_dir,outfile)))) 
        else:
            ffmpeg_command.append(str(i.strip(' ')))
    print(f'COMMAND {ffmpeg_command}')
    return ffmpeg_command

# list comprehension
def read_list(search_dir: str, img_listfile):
    """
    reads the list file for inputting images as a file
    
    parameters
    ----------
    search_dir: str
        path for the directory to search else '0'
    img_listfile: str
        path to the list file
    
    returns
    -------
    matched_files: list[str]
        a list with file paths
        
    modifications
    -------------
    2024-04-10 - Benjamin Pieczynski (added docstring)
    """
    # read in files from the list
    print(f'READING {img_listfile}')
    f = open(img_listfile, 'r')
    if search_dir != '0':
        matched_files = []
        for line in f:
            print(line)
            matched_files.append(os.path.join(search_dir,line.strip()))
    else: # option 0 - read in files as is
        info = f.read()
        matched_files = info.splitlines()
    f.close()
    return matched_files

# function to write a log entry
def write_to_log(params: dict, log_message: str) -> None:
    """
    Writes program actions to a log file
    
    parameters
    ----------
    params: dict
        dictionary containing log paths
    log_message: str
        string containing the message to display to the log
        
    modifications
    -------------
    2024-04-09 - Benjamin Pieczynski (changed current_time)\n
    2024-04-10 - Benjamin Pieczynski (added docstring)
    """
    try:
        current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        log_path = os.path.join(params['log_path'], params['log_file'])
        f = open(log_path, 'a') # open file in append mode
        f.write(f'{current_time} - {log_message}\n')
        f.close()
    except:
        print('Error - logfile not updated. Check parameter file for errors.')
    return

# function to remove same file names for overwrite
def prevent_overwrite(path: str, output_file: str) -> None:
    """
    For a given path, check to see if a file exists
    and remove it if it does.

    parameters
    ----------
    path: str
        path to file in question
    output_file: str
    
    modifications
    -------------
    2024-04-10 - Benjamin Pieczynski (added docstring)
    """
    # Check if the output file exists
    if os.path.exists(output_file):
        # If the file exists, remove it
        os.remove(output_file)
        write_to_log(path, f"Existing file {output_file} removed.")
    return
        
# check user files and delete if more than user limit
def check_user_files(params: dict) -> None:
    """
    Checks the number of files and removes them if there is more than
    the default limit.

    parameters
    ----------
    params: dict
        dictionary containing program parameters
    
    modifications
    -------------
    2024-04-10 - Benjamin Pieczynski (added docstring, changed current_time)
    """
    # time and directory path
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    directory_path = params['store_dir']
        
    # Get the list of files in the directory
    files_list = os.listdir(directory_path)

    # Count the number of files
    num_files = len(files_list)

    # Check if the number of files is greater than 600
    if num_files > int(params['user_limit']):
        # Filter files with .gif and .mp4 extensions and delete them
        for file in files_list:
            if file.endswith('.gif') or file.endswith('.mp4'):
                file_path = os.path.join(directory_path, file)
                os.remove(file_path)
        log_message = f'{current_time} - User animations removed'
    else:
        log_message = f'{current_time} - Checked user animations ({num_files} files)'
    
    # write to logs
    write_to_log(params, log_message)
    return

# convert time in to correct format for file
def time_converter(in_time):
    """
    Rounds an in time to the nearest png file located at 03,
    09, 15, 21. Meant for use in Forecast mode with building
    the IPS animations.
    
    parameters
    ----------
    in_time: datetime object
        a time in UTC
    
    returns
    -------
    formatted_time: datetime object
        the correctly formatted time
        
    modifications
    -------------
    2024-04-10 - Benjamin Pieczynski (added docstring)
    """
    # Round hour to the nearest .png file located at 03, 09, 15, 21
    in_hour = in_time.hour
    if in_hour < 3:
        new_hour = 21
        in_time = in_time - timedelta(hours=3) # convert time to previous day for nearest .png file
        in_hour = in_time.hour
    elif in_hour < 9:
        new_hour = 3
    elif in_hour < 15:
        new_hour = 9
    elif in_hour < 21:
        new_hour = 15
    elif in_hour < 24:
        new_hour = 21

    # Combine rounded hour and minute
    rounded_time = in_time.replace(hour=new_hour, minute=0, second=0, microsecond=0)

    # Format date and time as YYYYMMDD-HHMMUT
    formatted_time = rounded_time.strftime("%Y%m%d-%H%MUT")
    
    return formatted_time

def make_time_array(start_time, end_time, h: float) -> list:
    """
    Builds the time array using the start_time, end_time and time_step.
    
    parameters
    ----------
    start_time: datetime object
        starting time
    end_time: datetime object
        ending time
    h: float
        time step
        
    returns
    -------
    time_array: list
        array of times found
    
    modifications
    -------------
    2024-04-10 - Benjamin Pieczynski (added docstring)
    """
    print('CREATING TIME ARRAY\n...\n...\n...')
    time_array = []
    current_time = start_time
    time_array.append(time_converter(current_time)) # make sure the time is in the correct format
    while current_time <= end_time:
        current_time = current_time + timedelta(hours=h) # add the time step to the current time
        time_array.append(time_converter(current_time))
    len_times = len(time_array)
    print(f'COMPLETE...\n{len_times} DIFFERENT TIMES IN TIME ARRAY\n')
    return time_array

# function for checking if user logs exists and deleting excess user animations
def check_logs(params: dict) -> None:
    """
    Checks if logs file exists. Generates log file if it does not exist.
    
    parameters
    ----------
    params: dict
        program parameters
    
    modifications
    -------------
    2024-04-10 - Benjamin Pieczynski (added docstring)
    """
    try:
        # grab needed parameters
        log_file  = os.path.join(params['log_path'], params['log_file'])

        # check if log file exists
        if not os.path.exists(log_file):
            # Create the file if it doesn't exist
            f = open(log_file, 'w')
            current_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
            f.write(f'{current_time} - LOG FILE CREATED\n')

        # write log message
        c_version = params['version']
        log_message = f'Initializing Program: Version {c_version}'
        write_to_log(params, log_message)

        # check the amount of user animations
        check_user_files(params)
    except:
        print('Error - logs could not be checked. Check parameter file configuration.')
    return

def validate_pattern(pattern: str) -> bool:
    """
    Validates the pattern provided by the user. The user must provide patterns as
    pattern1*pattern2*pattern3 or just the individual pattern. This is only used
    in PATTERN MODE.
    
    parameters
    ----------
    pattern: str
        pattern provided by the user.
    
    returns
    -------
    bool
        True or False (valid / invalid)
        
    modifications
    -------------
    2024-04-10 - Benjamin Pieczynski (added docstring, modified * mechanism to
    take in larger arguments)
    """
    count_star = pattern.count('*')
    if count_star > 0:
        star_index = pattern.index('*')
        if star_index != 0 and star_index != len(pattern)-1:
            return True
        else:
            raise ValueError('Print * must be placed within the pattern (eg. pattern1*pattern2*pattern3)')
    else:
        if len(pattern) == 0:
            raise ValueError('PATTERN MODE SELECTED - you must provide a pattern in this mode')
        else:
            return False
        
def check_for_match(file: str, img_format: str, patterns: list) -> bool:
    """
    Checks the file for if the pattern is located within the
    filename.
    
    parameters
    ----------
    file: str
        filename
    img_format: str
        specified image format
    patterns: list[str]
        list of patterns to search for
    
    returns
    -------
    bMatch: bool
        whether or not there is a match
    """
    # first check if the image format is correct
    if img_format not in file:
        return False
    
    # check the file for a match
    bMatch = True
    try:
        for pattern in patterns:
            if pattern not in file:
                bMatch = False
                break
            else:
                None

    # filename is too short to match
    except:
        bMatch = False
    
    return bMatch
    
    
# Function to get a list of files in the current directory and filter based on pattern
def pattern_match(params: dict, pattern: str, search_dir: str, 
                  img_format: str ='.png') -> list:
    """
    Matches patterns within the search directory.
    
    parameters
    ----------
    params: dict
        dictionary containing program parameters
    pattern: str
        pattern to search for
    search_dir: str
        search_directory
    img_format: str
        format to search for (default .png)
    
    returns
    -------
    matched_files: list[str]
        list of paths to the matched files
    
    modifications
    -------------
    2024-04-10 - Benjamin Pieczynski (added docstring, added helper function,
    added progress bar.)
    """
    # array to store matched files
    matched_files = []

    if pattern != '0':

        # Split the pattern at the unique location
        print('\nBeginning Pattern Matching\n')
        patterns = pattern.split('*')
        for i, pattern in enumerate(patterns):
            p_num = i+1
            print(f'Pattern {p_num}: {pattern}')

        # Grab the matching files in the current working directory
        files_list = os.listdir(search_dir)
        for file in files_list:
            bMatch = check_for_match(file, img_format, patterns)
            match_message = 'MATCH' if bMatch else 'NO MATCH'
            optional = f'Checking File: {file} - {match_message}'
            print(optional)
            matched_files.append(f'{search_dir}/{file}') if bMatch else None
        
    # 0 option for no pattern search
    else:
        cap_format = img_format.upper()
        print(f'SELECTING ALL {cap_format} FILES IN THE CURRENT DIRECTORY')
        files = os.listdir(search_dir)
        for file in files:
            matched_files.append(f'{search_dir}/{file}') if img_format in file else None
        

    # log the message
    log_message = 'FOUND {} MATCHED FILES'.format(len(matched_files))
    write_to_log(params, log_message)
    print('FOUND {} MATCHED FILES\n'.format(len(matched_files)))
        
    return matched_files

# Function to create MP4 or GIF file from given files
def format_handler(command_file: str, out_dir: str, 
                   outfile: str, format_choice: str, 
                   params: dict, matched_files: list) -> None:

    """
    Creates an MP4 or GIF file from a list of files.
    
    parameters
    ----------
    command_file: str
        file to build ffmpeg command
    out_dir: str
        path to out directory
    outfile: str
        output file name
    format_choice: str
        MP4 or GIF media format
    params: dict
        dictionary containing program parameters
    matched_files: list[str]
        list of paths to the matched files
    
    modifications
    -------------
    2024-04-10 - Benjamin Pieczynski (added docstring)
    """

    # GIF option
    if format_choice=='GIF':
        print('.................................')
        print('\nCREATING GIF')
        print('.................................')
        file_list = ' '.join(matched_files)
        delay = params['delay']
        loop = params['loop']
        command = f'convert -delay {delay} -loop {loop} {file_list} {out_dir}/{outfile}.gif'
        subprocess.run(command, shell=True)
        
        print(f'PROCESS COMPLETE, TARGET OUTFILE = {out_dir}/{outfile}.gif')
        
    # MP4 option
    elif format_choice=='MP4':
        print('.................................')
        print('\nCREATING MP4')
        print('.................................')
        
        bitrate = params['bitrate']
        fps = params['fps']
        
        # Create a temporary file to store the 
        input_list = '{}/temp_png_list.txt'.format(out_dir)
        
        # Write the file paths to the temporary file
        with open(input_list, "w") as file:
            for file_name in matched_files:
                file.write(f"file '{file_name}'\n")
                
        
        # Create the command to generate the MP4 using ffmpeg
        ffmpeg_command = read_commands(input_list, fps, bitrate, out_dir, outfile, command_file)
        
        # Execute command
        subprocess.run(ffmpeg_command)
        
        # Remove the input list file
        os.remove(input_list)
        
        print(f'PROCESS COMPLETE, OUTFILE = {out_dir}/{outfile}.mp4')
        
    return

def resize_images(matched_files: list) -> None:
    """
    Function that calls adjust_image.py to change the image sizes to even.
    
    parameters
    """
    
    print('Resizing images to comply with ffmpeg...')
    
    # command to run the program
    command = [
        "python3",
        "adjust_image.py",
        "-f",
        *matched_files,
        "-m",
        "crop"
    ]
    
    # run the command
    try:
        subprocess.run(command, check=True)
        print("adjust_image.py executed successfully.")
    except subprocess.CalledProcessError as e:
        print("Error executing adjust_image.py:", e)
    
    return

# function to match the times for files with shared patterns
def match_times(matched_files: list, time_array: list) -> list:
    """
    Function that matches times with the pattern matched files
    
    parameters
    ----------
    matched_files: list
        a list of pattern matched files
    time_array: list
        a list of datetime objects matching desired times
    
    returns
    -------
    matched_new: list
        a list of cross-matched files
        
    modifications
    -------------
    2024-04-10 - Benjamin Pieczynski (added docstring)
    """
    print('\nMATCHING TIMES\n.........................')
    
    matched_new = [] # store new matched files
    matched_old = matched_files
    for target_time in time_array:
        print(f'Searching for time {target_time}...')
        for i, file_name in enumerate(matched_old):
            # match found
            if target_time in file_name:
                matched_new.append(file_name)
                del matched_old[i] # remove the matched file
                print(f'FOUND FILE: {file_name}')
                break # exit the loop

    return matched_new

# Function for ips archive searches
def structured_search(main_dir: str, time_array: list) -> list:
    """
    Function for IPS archive search.
    
    parameters
    ----------
    main_dir: str
        main directory
    time_array: list
        list of datetime objects
    
    returns
    -------
    matched_files: list
        a list of files matched in the archives
        
    modifications
    -------------
    2024-04-10 - Benjamin Pieczynski (added docstring)
    """
    months = {'01': 'January', '02': 'February', '03': 'March',
              '04': 'April',   '05': 'May',      '06': 'June',
              '07': 'July',    '08': 'August',   '09': 'September',
              '10': 'October', '11': 'November', '12': 'December'}
    matched_files = []
    p_year    = '' # previous year
    p_month   = '' # previous month
    temp_list = '' # temporary list to store files
    cpath     = '' # current path in use
    for target_time  in time_array:
        year  = target_time[0:4]
        month = months[target_time[4:6]]
        if year == p_year and month == p_month:
            pass # we can reuse the temp_list
        else:
            cpath = os.path.join(main_dir, year, month)

            if os.path.exists(cpath):
                temp_list = os.listdir(os.path.join(cpath))
                for i, file_name in enumerate(temp_list):
                    if target_time in file_name and '.png' in file_name:
                        matched_files.append(os.path.join(cpath,file_name))
                        del temp_list[i]
                        print(f'FOUND FILE {file_name}')
                        break # exit the loop

            else:
                print('Directory does not exist')

    return matched_files

def check_exists(dir: str, targ_file: str) -> bool:
    """
    Checks if the path exists
    
    parameters
    ----------
    path: str
        path to file
    
    returns
    -------
    bool
    """
    files_list = os.listdir(dir)
    print(f'Searching for {targ_file}')
    for file in files_list:
        if targ_file in file:
            return True
        else:
            pass
    return False