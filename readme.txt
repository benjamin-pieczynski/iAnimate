%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

READ ME FILE | PROGRAM: iAnimate | 2024-04-19

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

PROGRAM WRITTEN BY: BENJAMIN PIECZYNSKI

---------------------------------------------------------------------------------------------

PROGRAM LOCATION: /usr/lib/ianimate

***Copy command: cp /home/soft/bpieczynski/soft/pyth/png_animation/ .

MAIN FILE: image_animator.py

---------------------------------------------------------------------------------------------

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

	COMPLETE VERSION - image_animator.py | Current Version 3.1.0

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

The latest animation program that combines LIST MODE, FORECAST MODE, STANDARD MODE, 
RANGE MODE, TIME-SERIES MODE, and GUI MODE all into one complete program.

HOW TO RUN THE COMPLETE VERSION:

	python3 /path_to_program/image_animator.py *args
	***not dependencies must be installed or you must be using the python environment

	or simply just use - iAnimate *args 
	which can be done anywhere in leela

---------------------------------------------------------------------------------------------

MODE SELECTION

---------------------------------------------------------------------------------------------

[0] - MANUAL MODE

	USAGE: iAnimate 0

	Command Line Interface that directs the user through each step of the process. Allows 
	the user to utilize LIST MODE, AUTOMATIC MODE, RANGE MODE, STANDARD MODE, and
	FORECAST MODE. ***TIME-SERIES MODE is not yet supported via CLI.

[1] - FORECAST MODE
	
	USAGE: iAnimate 1 -vf {MP4, GIF}

	Mode that interfaces with IPS to build forecast animations using the past and future
	parameters within the parameter file. The forecast is built in reference to the current
	time.

	REQUIRED: -vf
	OPTIONAL: -if -sd -p -pf -cf -h -of -ss -od -rs
	MP4_ARGS: -br -fp 
	GIF_ARGS: -de -lp

[2] - RANGE MODE

	USAGE: iAnimate 2 -st {YYYY-mm-dd-HH:MM} -et {YYYY-mm-dd-HH:MM} -vf {MP4, GIF} 
					  -of {outfile}
	
	Select images using a time range. This is used when you can utilize time stamps within
	the files to sort the images (as long as they are formatted yyyymmddhh in the file name).

	REQUIRED: -st -et -vf -of
	OPTIONAL: -if -sd -p -pf -cf -ss -od -rs
	MP4_ARGS: -br -fp 
	GIF_ARGS: -de -lp

[3] - LIST MODE

	USAGE: iAnimate 3 -lf {list_file_path} -vf {MP4, GIF} -of {outfile}

	The user can provide a list of files in a text file to generate the animation with. It 
	is possible to use the search directory argument (-sd) so that one can only provide the
	file name in the file. This will join the search directory and image strings to locate
	the images. One can use -sd 0 to provide the full path to the files within the listfile
	as opposed to using a search directory.
	***Note that the files will be in order of listfile position.

	REQUIRED: -lf -vf -of
	OPTIONAL: -if -sd -pf -cf -od -rs
	MP4_ARGS: -br -fp 
	GIF_ARGS: -de -lp

[4] - STANDARD MODE

	USAGE: iAnimate 4 -vf {MP4, GIF} -of {outfile}

	The standard functionality of the iAnimate program. Searches for all files within a given
	directory and makes an animation. Using the pattern argument (-p), one can search for 
	patterns within the directory.

	REQUIRED: -vf -of
	OPTIONAL: -if -sd -p -pf -cf -od -rs
	MP4_ARGS: -br -fp 
	GIF_ARGS: -de -lp

[5] - TIME-SERIES MODE

	USAGE: iAnimate 5 -m {d, v, b brbt} -i {ts_plot instrument} -t {ips, smei, stereo, enlil} 
					-f {yyyymmddhh} -sd {tomography_path} -vf {MP4, GIF}

	Uses ts_plot to build an animation of the time-series plots. The standard usage utilizes
	the default parameter file to create a forecast range for a given forecast time. To set
	the plot bounds, one can use the ts_range argument (-tr) of format yyyymmddhh_yyyymmddhh.
	The program automatically uses -tr and -f to build the start and stop times for the line
	animation, however start_time (-st) and end_time (-et) in yyyymmddhh format can be used
	as an additional start and stop option for controlling the line position.

	REQUIRED: -m -i -t -f -sd -vf
	OPTIONAL: -tr -st -et -ss -pf -cf -od
	MP4_ARGS: -br -fp 
	GIF_ARGS: -de -lp

[6] - GRAPHIC USER INTERFACE MODE

	USAGE: iAnimate 6

	Activates a GUI for the animation process. Here the user submits the options within the
	GUI itself. The same principles for all previous modes apply when filling out each
	option (especially the TIME-SERIES mode).

	NO REQUIREMENT OR OPTIONALS

---------------------------------------------------------------------------------------------

	COMMAND LINE ARGUMENTS

---------------------------------------------------------------------------------------------

usage: iAnimate [-h] [-sd SEARCH_DIRECTORY] [-m {d,v,b brbt}] [-i {ace0,aceb,bepi,bpb,celias,
       dscovr,jupiter,mars,mercury,orbiter,orbiterb,parker,stereo_mag,stereoa,stereob,venus,
	   wind}] [-t TOMOGRAPHY] [-p PATTERN] [-vf {MP4,GIF}] [-if IMAGE_FORMAT] 
	   [-pf PARAMETER_FILE] [-cf COMMAND_FILE] [-st START_TIME] [-et END_TIME] 
	   [-ss STEP_SIZE] [-f FORECAST_TIME] [-tr TS_RANGE] [-lf LIST_FILE] [-od OUT_DIRECTORY] 
	   [-of OUTFILE] [-br BITRATE] [-fp FPS] [-de DELAY] [-lp LOOP] [-rs] [-v]
        {0,1,2,3,4,5,6}

   {0,1,2,3,4,5,6}       REQUIRED Select the program mode
  -h, --help            show this help message and exit
  -sd SEARCH_DIRECTORY, --search_directory SEARCH_DIRECTORY
                        Directory where images are stored (DEFAULT: current). Enter 0 to 
						specify none.
  -m {d,v,b brbt}, --measurement {d,v,b brbt}
                        ts_plot option for measurement (d, v, b brbt)
  -i {ace0,aceb,bepi,bpb,celias,dscovr,jupiter,mars,mercury,orbiter,orbiterb,parker,
      stereo_mag,stereoa,stereob,venus,wind}, --instrument {ace0,aceb,bepi,bpb,celias,
	  dscovr,jupiter,mars,mercury,orbiter,orbiterb,parker,stereo_mag,stereoa,stereob,
	  venus,wind}
                        ts_plot option for the comparison instrument when using time-series 
						mode. See ts_plot -il for the instrument list. (time-series only)
  -t TOMOGRAPHY, --tomography TOMOGRAPHY
                        Name of the type of tomography (ips/smei/stereo/enlil) 
						(time-series only)
  -p PATTERN, --pattern PATTERN
                        Search pattern format:(pattern1*pattern2*patternN). Default=0 for 
						no pattern.
  -vf {MP4,GIF}, --video_format {MP4,GIF}
                        Video export format (MP4 or GIF). MP4 by default.
  -if IMAGE_FORMAT, --image_format IMAGE_FORMAT
                        Input image format (default = .png)
  -pf PARAMETER_FILE, --parameter_file PARAMETER_FILE
                        Path to parameter file.
  -cf COMMAND_FILE, --command_file COMMAND_FILE
                        Path to command file.
  -st START_TIME, --start_time START_TIME
                        Search start time. Format: YYYY-mm-dd-HH:MM 
						(yyyymmddhh for time-series)
  -et END_TIME, --end_time END_TIME
                        Search end time. Format: YYYY-mm-dd-HH:MM
						(yyyymmddhh for time-series)
  -ss STEP_SIZE, --step_size STEP_SIZE
                        Step size in hours. For forecast mode it must be a multiple of 6. 
						(Parameter file has default)
  -f FORECAST_TIME, --forecast_time FORECAST_TIME
                        Forecast time for ts_plot yyyymmddhh (time-series only)
  -tr TS_RANGE, --ts_range TS_RANGE
                        Time range option in ts_plot, format yyyymmddhh_yyyymmddhh 
						(time-series only)
  -lf LIST_FILE, --list_file LIST_FILE
                        Path to .txt extension list_file.
  -od OUT_DIRECTORY, --out_directory OUT_DIRECTORY
                        Output directory (DEFAULT: None). You must specify the output 
						directory. Use cwd to specify current directory.
  -of OUTFILE, --outfile OUTFILE
                        Specified outfile. DEFAULT=animation ***DO NOT INCLUDE EXTENSION
  -br BITRATE, --bitrate BITRATE
                        Specific bitrate, in K. DEFAULT=parameter file value. (MP4 only)
  -fp FPS, --fps FPS    Frames per second (FPS=100/N). DEFAULT=parameter file value. 
  						(MP4 only)
  -de DELAY, --delay DELAY
                        Delay = value / 100 seconds. DEFAULT=parameter file value. 
						(GIF only)
  -lp LOOP, --loop LOOP
                        Repeat number for GIFS (Default is 0 for infinite)
  -rs, --bResize        Option to resize input images if ffmpeg returns an error 
  						(dimensions must be even)
  -v, --version         Display current program version number

---------------------------------------------------------------------------------------------

	COMMAND FILES 

	Only contain one line with a comma separating each argument(\ indicated new line for
	saved space)

	ffmpeg, -f, concat, -safe, 0, -r, fps, -i, input_list, -vf, \ 
	scale='trunc(2*floor(iw/2))':'trunc(2*floor(ih/2))', -c:v, libx264, \ 
	-c:a, aac, -b:v, bitrate, -strict, experimental, -pix_fmt, yuv420p, outfile

	fps, bitrate, outfile: must be included and are defined through command line arguments
	or other user inputs.

---------------------------------------------------------------------------------------------

	PARAMETER FILE - IMPORTANT

	You must edit the animator.parm file to get the correct paths for the automatic
	program.

	Description of each parameter in the .parm file

	version:    str     displays the current program version number

	user_limit: int     specifying the limit of RANGE MODE created animations (for IPS)

	past:       float   (days) in the past that FORECAST MODE will use as the START_TIME

	future:     float   (days) in the future that FORECAST MODE will use as the END_TIME

	store_dir:  str     storing the path to the directory FORECAST animations are saved

	user_dir:   str     storing the path to the directory RANGE animations are saved

	log_path:   str     path to the directory where the log file will be created

	log_file:   str     name of the logfile

	fps:        int     Frames Per Second for MP4 files

	bitrate:    int     resolution of MP4 files

	delay:      int     FPS = 100 /N (similar parameter for GIF file)

	loop:       int     how often the program will loop

---------------------------------------------------------------------------------------------

LIST_FILE

ls *.png >> list.txt

	img_1.png
	img_2.png
	...
	img_N.png

	***note images can include full path (-sd 0) or only file name (requires -sd /your/path)

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
