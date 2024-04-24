#----------------------------------------------------------------------------------------
# Module : defaults
#----------------------------------------------------------------------------------------
#
# Programmer : Benjamin Pieczynski
# 01/25/2024
#
#----------------------------------------------------------------------------------------
#
# This module is used by the main Image Animator program to store global variables.
# This essentially acts as a header file. This also includes all descriptions and 
# helper descriptions of the code.
#
# Modification History
# 2024-04-11 - Benjamin Pieczynski (added -rs option, changed command and parameter
#              file names)
# 2024-04-12 - Benjamin Pieczynski (change flag for video format to -vf, added -if)
# 2024-04-18 - Benjamin Pieczynski (multiple flags added for time-series)
#
#---------------------------------------------------------------------------------------
# imports
import os
import argparse
#----------------------------------------------------------------------------------------


# Global variables #
version         = 'v3.1.0'
prog_name       = 'iAnimate'
fullname        = f'{prog_name} - {version}'
programmer      = 'Benjamin Pieczynski'
release_date    = '01-25-2024'
cwd             = os.getcwd() # current working directory
default_param   = './parameters/default.parm'
default_command = './commands/default.command'
def_of          = 'animation' # default output file

description = '''
                 PROGRAM: {}
                 VERSION: {}
                 
                 BY: {} - {}
                 
                 This program builds IPS animations using either a MANUAL
                 or AUTOMATIC mode. While the program is meant for IPS
                 animations, there is some compatibility for sending
                 images (png format) to the program through list
                 directives.
                 
                 [0] - MANUAL MODE: use the interactive part
                     of the program.
                     
                 [1] - FORECAST MODE: Mode with IPS to build
                     forecast animations.
                     | REQUIRED: -vf |
                     | OPTIONAL: -if -sd -p -pf -cf -h -of -ss |
                     
                 [2] - RANGE MODE: Select a time range for the
                     selection of images to be compiled into
                     an animation.
                     | REQUIRED: -vf -st -et -of |
                     | OPTIONAL: -if -sd -p -pf -cf -ss |
                     
                 [3] - LIST MODE: Use a .txt file to read in
                     different file paths. You do not have
                     to include a search directory, or you
                     can and include only file names.
                     | REQUIRED: -vf -lf -of |
                     | OPTIONAL: -if -sd -pf -cf |
                     
                 [4] - STANDARD MODE:
                     select all images within a directory to
                     build an animation. You can filter with
                     a pattern.
                     | REQUIRED: -vf -of |
                     | OPTIONAL: -if -sd -p -pf -cf |
                     
                 [5] - TS PLOT MODE: An IPS setting used to
                     include ts plot in the creation of animations.
                     Effectively creates a time series animation.
                     | REQUIRED: -vf -od -of -sd -m -f -t
                     | OPTIONAL: -tr -st -et -if -od -pf -cf -ss -y
                     
                 [6] - GUI MODE: Activates a GUI interface for
                     building the animation.
                     
               ***You can override parameter file arguments with
               -od -ss MP4 -br -fp GIF -de -lp
                 '''.format(prog_name, version, programmer, release_date)
                 
parser = argparse.ArgumentParser(prog=prog_name, description = description, 
                                 formatter_class=argparse.RawDescriptionHelpFormatter)

# Help information
mode_help      = """REQUIRED Select the program mode"""
vhelp          = '''Display current program version number'''
sd_help        = '''Directory where images are stored (DEFAULT: current). Enter 0 to specify none.'''
pattern_help   = '''Search pattern format:(pattern1*pattern2*patternN)). Default=0 for
                    no pattern.'''
vformat_help   = '''Video export format (MP4 or GIF). MP4 by default.'''
iformat_help   = '''Input image format (default = .png)'''
parameter_help = '''Path to parameter file.'''
command_help   = '''Path to command file.'''
st_help        = '''Search start time. Format: YYYY-mm-dd-HH:MM'''
et_help        = '''Search end time. Format: YYYY-mm-dd-HH:MM'''
h_help         = '''Step size in hours. For forecast mode it must be a multiple of 6.
                    (Parameter file has default)'''
list_help      = '''Path to .txt extension list_file.'''
od_help        = '''Output directory (DEFAULT: None). You must specify the output directory. 
                    Use cwd to specify current directory.'''
of_help        = '''Specified outfile. DEFAULT=animation .DO NOT INCLUDE EXTENSION'''
bit_help       = '''Specific bitrate, in K. DEFAULT=parameter file value. (MP4 only)'''
fps_help       = '''Frames per second (FPS=100/N). DEFAULT=parameter file value. (MP4 only)'''
delay_help     = '''Delay = value / 100 seconds. DEFAULT=parameter file value. (GIF only)'''
loop_help      = '''Repeat number for GIFS (Default is 0 for infinite)'''
resize_help    = '''Option to resize input images if ffmpeg returns an error 
                    (dimensions must be even)'''
mes_help       = '''ts_plot option for measurement (d, v, b brbt)'''
instr_help     = '''ts_plot option for the comparison instrument when using time-series 
                    mode. See ts_plot -il for the instrument list. (time-series only)'''
tomo_help      = '''Name of the type of tomography (ips/smei/stereo/enlil) (time-series only)'''
tr_help        = '''Time range option in ts_plot, format yyyymmddhh_yyyymmddhh (time-series only)'''
ft_help        = '''Forecast time for ts_plot yyyymmddhh (time-series only)'''
bR_help        = '''Argument to remove temporary directory (time-series only)'''

# options for ts_plot
ts_instruments = ['ace0', 
                  'aceb', 
                  'bepi', 
                  'bpb', 
                  'celias', 
                  'dscovr', 
                  'jupiter', 
                  'mars', 
                  'mercury',
                  'orbiter', 
                  'orbiterb', 
                  'parker', 
                  'stereo_mag', 
                  'stereoa', 
                  'stereob',
                  'venus',
                  'wind']

# adding parse options
parser.add_argument("mode",         type=int, choices=[0, 1, 2, 3, 4, 5, 6],   help=mode_help     )
parser.add_argument('-sd', '--search_directory',     default=cwd,              help=sd_help       )
parser.add_argument('-m',  '--measurement',          default=None,             help=mes_help,
                    choices=['d', 'v', 'b brbt'])
parser.add_argument('-i',  '--instrument',           default=None,             help=instr_help,
                    choices=ts_instruments)
parser.add_argument('-t',  '--tomography',           default=None,             help=tomo_help)
parser.add_argument('-p',  '--pattern',              default='0',              help=pattern_help  )
parser.add_argument('-vf', '--video_format',         default='MP4',            help=vformat_help, 
                    choices=['MP4', 'GIF'])
parser.add_argument('-if', '--image_format',         default='.png',           help=iformat_help  )
parser.add_argument('-pf', '--parameter_file',       default=default_param,    help=parameter_help)
parser.add_argument('-cf', '--command_file',         default=default_command,  help=command_help  )
parser.add_argument('-st', '--start_time',           default=None,             help=st_help       )
parser.add_argument('-et', '--end_time',             default=None,             help=et_help       )
parser.add_argument('-ss', '--step_size', type=float, default=None,            help=h_help        )
parser.add_argument('-f',  '--forecast_time',        default=None,             help=ft_help       )
parser.add_argument('-tr', '--ts_range',             default=None,             help=tr_help       )
parser.add_argument('-lf', '--list_file',            default=None,             help=list_help     )
parser.add_argument('-od', '--out_directory',        default=None,              help=od_help       )
parser.add_argument('-of', '--outfile',              default=def_of,           help=of_help       )
parser.add_argument('-br', '--bitrate',    type=int, default=None,             help=bit_help      )
parser.add_argument('-fp', '--fps',        type=int, default=None,             help=fps_help      )
parser.add_argument('-de', '--delay',      type=int, default=None,             help=delay_help    )
parser.add_argument('-lp', '--loop',       type=int, default=None,             help=loop_help     )
parser.add_argument('-rs', '--bResize',    action='store_true',                help=resize_help   )
parser.add_argument('-br', '--bRemove',    action='store_true',                help=bR_help       )
parser.add_argument('-v',  '--version',    action='version', version=fullname, help=vhelp         )