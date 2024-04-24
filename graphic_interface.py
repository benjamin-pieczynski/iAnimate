#-------------------------------------------------------------------
# MODULE: graphic_interface.py
# BY: Benjamin Pieczynski (UCSD A&A: bpieczynsk@ucsd.edu)
# DATE: 2024-04-09T13:14
#
# PURPOSE:
#   A new version of the animator program that utilizes the package 
#   tkinter to build a GUI for users to build animations with. This 
#   is a part of the version 3.0.0 update to the ips_animator 
#   program. The program is not renamed to iAnimate.py.
#
# FUNCTIONS:
#   run_gui
#
#-------------------------------------------------------------------

# imports
#import customtkinter as ctk
import tkinter as tk
from datetime import datetime, timedelta, timezone

# user imports
from defaults import *
from operations import read_params
from automatic import automatic_mode

# GUI class
class App(tk.Tk):
    """
    A class to build the GUI. Uses tkinter package for building
    the interface. Does not take in any attributes. Sets default
    values using the animator.parm file.
    """
    # initializing GUI
    def __init__(self):
        print('\nInitializing GUI\n')
        super().__init__()
        
        # setting appearance
        self.geometry('680x280')
        self.title(f'iAnimate - {version}')
        
        # class defaults
        self.large_font = ('Arial', 20, 'bold')
        self.normal_font_bold = ('Arial', 12, 'bold')
        self.normal_font = ('Arial', 12)
        self.italic_font = ('Arial', 10, 'italic')
        
        # create title label
        self.title_label = tk.Label(self, text="iAnimate", font=self.large_font)

        # search directory
        self.search_dir_label = tk.Label(self, text="Search Directory (blank = cwd)", 
                                     font=self.normal_font_bold)
        self.search_directory = tk.Entry(self, width=30, bg='light cyan', 
                                    font=self.normal_font)
        
        # Video Format Choice
        self.vf_label = tk.Label(self, text="Video Format", font=self.normal_font_bold)
        self.video_format = tk.StringVar(value='MP4')
        self.vf_option_1 = tk.Radiobutton(self, text='MP4', 
                                          variable=self.video_format, value='MP4',
                                          font=self.normal_font)
        self.vf_option_2 = tk.Radiobutton(self, text='GIF', 
                                          variable=self.video_format, value='GIF',
                                          font=self.normal_font)
        
        # Image Format Choice
        self.img_format_label = tk.Label(self, text="Image Format", font=self.normal_font_bold)
        self.img_format = tk.Entry(self, width=10, bg='light cyan', font=self.normal_font)
        
        # Search Choice
        self.search_label = tk.Label(self, text="Search Mode", font=self.normal_font_bold)
        self.search_choice = tk.StringVar(value='4')
        self.sc_1 = tk.Radiobutton(self, text='MATCHING IMAGES', variable=self.search_choice,
                                   value='4', font=self.normal_font)
        self.sc_2 = tk.Radiobutton(self, text='TIME RANGE', variable=self.search_choice,
                                   value='2', font=self.normal_font)
        self.sc_3 = tk.Radiobutton(self, text='LIST FILE', variable=self.search_choice,
                                   value='3', font=self.normal_font)
        self.sc_4 = tk.Radiobutton(self, text='TIME-SERIES', variable=self.search_choice,
                                   value='5', font=self.normal_font)       

        # Output options
        self.out_dir_label = tk.Label(self, text='Out Directory', font=self.normal_font_bold)
        self.out_directory = tk.Entry(self, width=30, bg='light cyan', font=self.normal_font)
        self.outfile_label = tk.Label(self, text='Output File (no .ext)', font=self.normal_font_bold)
        self.outfile = tk.Entry(self, width=30, bg='light cyan', font=self.normal_font)
        
        # resize option
        self.bResize = tk.BooleanVar(value=False)
        self.resize_checkbutton = tk.Checkbutton(self, text='Resize Images',
                                                 var=self.bResize,
                                                 onvalue=True, offvalue=False, 
                                                 height=1, width=15,
                                                 font=self.normal_font)
        
        # creating generator button
        self.generator_button = tk.Button(self, text='Generate', 
                                          font=self.normal_font_bold, 
                                          padx=50, pady=21, bg='beige', 
                                          command=self.generate_animation)

        # build grid
        self.title_label.grid(row=0, column=1, columnspan=4, sticky='w')
        self.search_dir_label.grid(row=1, column=0, pady=(10,0))
        self.search_directory.grid(row=2, column=0)
        self.vf_label.grid(row=1, column=2, columnspan=2, pady=(10,0))
        self.vf_option_1.grid(row=2, column=2, padx=5, pady=2)
        self.vf_option_2.grid(row=2, column=3, padx=5, pady=2)
        self.img_format_label.grid(row=3, column=2, columnspan=2, pady=(10,0))
        self.img_format.grid(row=4, column=2, columnspan=2)
        self.search_label.grid(row=1, column=4, padx=5, pady=(10,0))
        self.sc_1.grid(row=2, column=4, sticky='W', padx=5, pady=2)
        self.sc_2.grid(row=3, column=4, sticky='W', padx=5, pady=2)
        self.sc_3.grid(row=4, column=4, sticky='W', padx=5, pady=2)
        self.sc_4.grid(row=5, column=4, sticky='W', padx=5, pady=2)
        self.out_dir_label.grid(row=3, column=0, pady=(10,0))
        self.out_directory.grid(row=4, column=0)
        self.outfile_label.grid(row=5, column=0, pady=(10,0))
        self.outfile.grid(row=6, column=0)
        self.resize_checkbutton.grid(row=6, column=1, columnspan=3)
        self.generator_button.grid(row=6, column=4, columnspan=1)

        # set initial variables
        print('setting inital parameters...')
        self.parmfile = default_param
        self.cmd_file = default_command
        params = read_params(default_param) # grab the initial parameters
        self.search_directory.insert(0, cwd)
        self.out_directory.insert(0, cwd)
        self.img_format.insert(0,params['img_format'])
        self.outfile.insert(0,'my_animation')
        self.fps = int(params['fps'])
        self.bitrate = int(params['bitrate'])
        self.delay = int(params['delay'])
        self.loop = int(params['loop'])
        self.future = float(params['future'])
        self.past = float(params['past'])
        self.h = int(params['time_step'])
        self.logfile = os.path.join(params['log_path'], params['log_file'])
        
        print('SUCCESS: GUI initialized\n')
        return
    
    # data processing functions
    def run_ianimate(self) -> None:
        """
        Runs the iAnimate program using all class created variables.
        Called from the format_widget which handles the video format.
        """
        # parameter and command files
        self.args['parameter_file'] = default_param
        print(f'Parameter File: {self.args['parameter_file']}')
        
        # MP4
        if self.args['video_format'] == 'MP4':
            # set GIF parameters to none
            self.args['loop'] = None
            self.args['delay'] = None
            
            # set mp4 parameters
            self.cmd_file = self.cmd_entry.get()
            self.args['command_file'] = self.cmd_file
            print(f'Command File: {self.cmd_file}')
            self.args['bitrate'] = int(self.bitrate_entry.get())
            self.args['fps'] = int(self.fps_entry.get())
            print(f'bitrate = {self.args['bitrate']} kbs, FPS = {self.args['fps']}')
            print('closing MP4 widget...')
            print('starting program...\n')
            
            # run the program
            automatic_mode(self.args)
            self.mp4_window.destroy()
            
        # GIF
        else:
            # set MP4 parameters to none
            self.args['fps'] = None
            self.args['bitrate'] = None
            self.args['command_file'] = self.cmd_file
            print(f'Command File: {self.cmd_file}')
            
            # set GIF parameters
            self.args['loop'] = self.loop_entry.get()
            print(f'loop = {self.args['loop']}')
            self.args['delay'] = self.delay_entry.get()
            print(f'delay = {self.args['delay']}')
            print('closing gif widget...')
            print('starting program...\n')

            # run the program
            automatic_mode(self.args)
            self.gif_window.destroy()

        return
    
    def process_list_data(self) -> None:
        """
        Processes inputs in the standard GUI
        """
        print('getting list widget data...')

        # get pattern
        self.args['pattern'] = None
        print(f'Pattern = {self.args['pattern']}')
        
        # get list file
        self.args['list_file'] = self.list.get()
        print(f'List File = {self.args['list_file']}')
        
        if self.args['video_format'] == 'MP4':
            print('opening mp4 widget')
            self.mp4_widget()
        else:
            self.gif_widget()
        print('closing range widget...')
        self.standard_window.destroy()
        return  
    
    def process_standard_data(self) -> None:
        """
        Processes inputs in the standard GUI
        """
        print('getting standard widget data...')

        # get pattern
        self.args['pattern'] = self.pattern.get()
        print(f'Pattern = {self.args['pattern']}')
        
        # set list_file to none
        self.args['list_file'] = None
        print(f'List File = None')
        
        if self.args['video_format'] == 'MP4':
            print('opening mp4 widget')
            self.mp4_widget()
        else:
            self.gif_widget()
        print('closing standard widget...')
        self.standard_window.destroy()
        return        

    def process_range_data(self) -> None:
        """
        Helper function to process the range data and close the range window
        """
        print('getting range widget data...')

        # get pattern
        self.args['pattern'] = self.pattern.get()
        print(f'Pattern = {self.args['pattern']}')
        
        # get start time
        self.args['start_time'] = self.start_time.get()
        print(f'Start Time = {self.args['start_time']}')
        
        # get end time
        self.args['end_time'] = self.end_time.get()
        print(f'End Time = {self.args['end_time']}')
        
        # get time step
        self.args['step_size'] = self.step_size.get()
        print(f'h = {self.args['step_size']} hours')
        
        # set list_file to none
        self.args['list_file'] = None
        print(f'List File = None')
        
        if self.args['video_format'] == 'MP4':
            print('opening mp4 widget')
            self.mp4_widget()
        else:
            self.gif_widget()
        print('closing range widget...')
        self.range_window.destroy()
        return
    
    def process_ts_data(self) -> None:
        """
        Helper function to process the time-series data and close the
        time-series window
        """
        print('getting range widget data...')

        # get pattern
        self.args['pattern'] = '0'
        
        # get forecast time
        self.args['forecast_time'] = self.forecast_time.get()
        if self.args['forecast_time'] == '':
            self.args['forecast_time'] = None
        print(f'Forecast Time = {self.args['forecast_time']}')
        
        # get time range
        self.args['ts_range'] = self.time_range.get()
        if self.args['ts_range'] == '':
            self.args['ts_range'] = None
        print(f'Time Range = {self.args['ts_range']}')
        
        # get start time
        self.args['start_time'] = self.start_time.get()
        if self.args['start_time'] == '':
            self.args['start_time'] = None
        print(f'Start Time = {self.args['start_time']}')
        
        # get end time
        self.args['end_time'] = self.end_time.get()
        if self.args['end_time'] == '':
            self.args['end_time'] = None
        print(f'End Time = {self.args['end_time']}')
        
        # get time step
        self.args['step_size'] = self.step_size.get()
        print(f'h = {self.args['step_size']} hours')
        
        # get measurement
        self.args['measurement'] = self.measurement.get()
        print(f'Measurement = {self.args['measurement']}')
        
        # get instrument
        self.args['instrument'] = self.instrument.get()
        print(f'Instrument = {self.args['instrument']}')
        
        # get tomography
        self.args['tomography'] = self.tomography.get()
        print(f'Tomography = {self.args['tomography']}')

        # set initial argument for bRemove
        self.args['bRemove'] = False
        
        # set list_file to none
        self.args['list_file'] = None
        print(f'List File = None')
        
        if self.args['video_format'] == 'MP4':
            print('opening mp4 widget')
            self.mp4_widget()
        else:
            self.gif_widget()
        print('closing time-series widget...')
        self.ts_window.destroy()
        return
    
        # additional windows
    def gif_widget(self) -> None:
        """
        Top level window to submit video parameters for gif
        """
        print('opening video format widget (gif)...')
        self.gif_window = tk.Toplevel(self)
        self.gif_window.title('iAnimator - GIF Settings')
        self.gif_window.geometry('680x280')
        
        # set title label
        gif_title = tk.Label(self.gif_window, text='GIF Settings', font=self.large_font)
        
        # fps submission
        delay_label = tk.Label(self.gif_window, text="delay (value / 100 s)", font=self.normal_font)
        self.delay_entry = tk.Entry(self.gif_window, width=6, bg='light cyan', 
                                  font=self.normal_font)
        
        # bitrate submission
        loop_label = tk.Label(self.gif_window, text='loop (0 = infinite)', font=self.normal_font)
        self.loop_entry = tk.Entry(self.gif_window, width=7, bg='light cyan',
                                      font=self.normal_font)
        
        # submit button
        submit_button = tk.Button(self.gif_window, text="SUBMIT", bg='beige',
                                  padx=30, pady=10, font=self.normal_font_bold,
                                  command=self.run_ianimate)
        
        # set grid
        gif_title.grid(row=0, column=1, columnspan=2, sticky='W')
        delay_label.grid(row=1, column=0, padx=5, pady=(10,0))
        self.delay_entry.grid(row=1, column=1, padx=5, pady=(10,0), sticky='W')
        loop_label.grid(row=2, column=0, padx=5, pady=(10,0))
        self.loop_entry.grid(row=2, column=1, padx=5, pady=(10,0), sticky='W')
        submit_button.grid(row=7, column=0, columnspan=2, pady=(20,0))

        # set defaults
        self.loop_entry.insert(0, str(self.loop))
        self.delay_entry.insert(0, str(self.delay))
        return
    
    # additional windows
    def mp4_widget(self) -> None:
        """
        Top level window to submit video parameters
        """
        print('opening video format widget')
        self.mp4_window = tk.Toplevel(self)
        self.mp4_window.title('iAnimator - MP4 Settings')
        self.mp4_window.geometry('680x280')
        
        # set title label
        mp4_title = tk.Label(self.mp4_window, text='MP4 Settings', font=self.large_font)
        
        # fps submission
        fps_label = tk.Label(self.mp4_window, text="fps", font=self.normal_font)
        self.fps_entry = tk.Entry(self.mp4_window, width=6, bg='light cyan', 
                                  font=self.normal_font)
        
        # bitrate submission
        bitrate_label = tk.Label(self.mp4_window, text='bitrate (kbs)', font=self.normal_font)
        self.bitrate_entry = tk.Entry(self.mp4_window, width=7, bg='light cyan',
                                      font=self.normal_font)
        
        # command file submission
        cmd_label = tk.Label(self.mp4_window, text='command file path', font=self.normal_font)
        self.cmd_entry = tk.Entry(self.mp4_window, width=30, bg='light cyan',
                                  font=self.normal_font)
        
        # submit button
        submit_button = tk.Button(self.mp4_window, text="SUBMIT", bg='beige',
                                  padx=30, pady=10, font=self.normal_font_bold,
                                  command=self.run_ianimate)
        
        # set grid
        mp4_title.grid(row=0, column=1, columnspan=2, sticky='W')
        fps_label.grid(row=1, column=0, padx=5, pady=(10,0))
        self.fps_entry.grid(row=1, column=1, padx=5, pady=(10,0), sticky='W')
        bitrate_label.grid(row=2, column=0, padx=5, pady=(10,0))
        self.bitrate_entry.grid(row=2, column=1, padx=5, pady=(10,0), sticky='W')
        cmd_label.grid(row=3, column=0, padx=5, pady=(10,0))
        self.cmd_entry.grid(row=3, column=1, padx=5, pady=(10,0), sticky='W')
        submit_button.grid(row=7, column=0, columnspan=2, pady=(20,0))

        # set defaults
        self.fps_entry.insert(0, str(self.fps))
        self.bitrate_entry.insert(0, str(self.bitrate))
        self.cmd_entry.insert(0, self.cmd_file)
        return

    def range_widget(self) -> None:
        """
        Top level window to submit parameters for the range mode
        selection.
        """
        self.range_window = tk.Toplevel(self)
        self.range_window.title('iAnimator - Range Mode')
        #self.range_window.grab_set() # sets window to modal
        self.range_window.geometry('620x300')
        
        # set title label
        range_title = tk.Label(self.range_window, text='RANGE MODE', font=self.large_font)
        
        # pattern submission
        pattern_label = tk.Label(self.range_window, 
                                 text="pattern (0 = none)", 
                                 font=self.normal_font)
        pattern_description = tk.Label(self.range_window, text='pattern1*pattern2*patternN',
                                       font=self.italic_font)
        self.pattern = tk.Entry(self.range_window, width=40, bg='light cyan', 
                                font=self.normal_font)
        
        # time submission
        start_label = tk.Label(self.range_window, text="start time", 
                               font=self.normal_font)
        entry_format_1 = tk.Label(self.range_window, text="(YYYY-mm-dd-HH:MM)",
                                  font=self.italic_font)
        self.start_time = tk.Entry(self.range_window, width=20, bg='light cyan', 
                                   font=self.normal_font)
        end_label = tk.Label(self.range_window, text="end time", 
                             font=self.normal_font)
        entry_format_2 = tk.Label(self.range_window, text="(YYYY-mm-dd-HH:MM)",
                                  font=self.italic_font)       
        self.end_time = tk.Entry(self.range_window, width=20, bg='light cyan', 
                                 font=self.normal_font)
        h_label = tk.Label(self.range_window, text="time step(hours)", 
                           font=self.normal_font)
        self.step_size = tk.Entry(self.range_window, width=8, bg='light cyan', 
                                  font=self.normal_font)
        
        # submit button
        submit_button = tk.Button(self.range_window, text="SUBMIT", bg='beige',
                                  padx=30, pady=10, font=self.normal_font_bold,
                                  command=self.process_range_data)
        
        # set grid
        range_title.grid(row=0, column=1, columnspan=2, sticky='W')
        pattern_label.grid(row=1, column=0, padx=5, pady=(10,0), sticky='E')
        pattern_description.grid(row=2, column=0, padx=5)
        self.pattern.grid(row=1, column=1, padx=5, pady=(10,0), sticky='W')
        start_label.grid(row=3, column=0, padx=5, pady=(10,0), sticky='E')
        entry_format_1.grid(row=4, column=0, padx=5)
        self.start_time.grid(row=3, column=1, padx=5, pady=(10,0), sticky='W')
        end_label.grid(row=5, column=0, padx=5, pady=(10,0), sticky='E')
        entry_format_2.grid(row=6, column=0, padx=5)
        self.end_time.grid(row=5, column=1, padx=5, pady=(10,0), sticky='W')
        h_label.grid(row=7, column=0, padx=5, pady=(10,0), sticky='E')
        self.step_size.grid(row=7, column=1, padx=5, pady=(10,0), sticky='W')
        submit_button.grid(row=8, column=0, columnspan=2, pady=10)

        # set defaults
        self.pattern.insert(0, '0')
        self.start_time.insert(0, self.args['start_time'])
        self.end_time.insert(0, self.args['end_time'])
        self.step_size.insert(0, self.args['step_size'])
        return
    
    def standard_widget(self) -> None:
        """
        Top level window to submit parameters for the range mode
        selection.
        """
        self.standard_window = tk.Toplevel(self)
        self.standard_window.title('iAnimator - Standard Mode')
        self.standard_window.geometry('600x150')
        
        # set title label
        standard_title = tk.Label(self.standard_window, text='STANDARD MODE', font=self.large_font)
        
        # pattern submission
        pattern_label = tk.Label(self.standard_window, 
                                 text="pattern (0 = none)", 
                                 font=self.normal_font)
        pattern_description = tk.Label(self.standard_window, text='pattern1*pattern2*patternN',
                                       font=self.italic_font)
        self.pattern = tk.Entry(self.standard_window, width=40, bg='light cyan', 
                                font=self.normal_font)
        
        # submit button
        submit_button = tk.Button(self.standard_window, text="SUBMIT", bg='beige',
                                  padx=30, pady=10, font=self.normal_font_bold,
                                  command=self.process_standard_data)
        
        # set grid
        standard_title.grid(row=0, column=1, columnspan=2, sticky='W')
        pattern_label.grid(row=1, column=0, padx=5, pady=(10,0), sticky='E')
        pattern_description.grid(row=2, column=0, padx=5)
        self.pattern.grid(row=1, column=1, padx=5, pady=(10,0), sticky='W')
        submit_button.grid(row=3, column=0, columnspan=2)

        # set defaults
        self.pattern.insert(0, '0')
        return
    
    def list_widget(self) -> None:
        """
        Top level window to submit parameters for the list file mode
        selection.
        """
        self.list_window = tk.Toplevel(self)
        self.list_window.title('iAnimator - List Mode')
        self.list_window.geometry('600x150')
        
        # set title label
        standard_title = tk.Label(self.list_window, text='LIST MODE', font=self.large_font)
        
        # pattern submission
        list_label = tk.Label(self.list_window, 
                                 text="list-file path", 
                                 font=self.normal_font)
        self.list = tk.Entry(self.list_window, width=40, bg='light cyan', 
                                font=self.normal_font)
        
        # submit button
        submit_button = tk.Button(self.list_window, text="SUBMIT", bg='beige',
                                  padx=30, pady=10, font=self.normal_font_bold,
                                  command=self.process_list_data)
        
        # set grid
        standard_title.grid(row=0, column=1, columnspan=2, sticky='W')
        list_label.grid(row=1, column=0, padx=5, pady=(10,0), sticky='E')
        self.list.grid(row=1, column=1, padx=5, pady=(10,0), sticky='W')
        submit_button.grid(row=3, column=0, columnspan=2, pady=20)
        return
    
    def ts_widget(self) -> None:
        """
        Top level window to submit parameters for the range mode
        selection.
        """
        self.ts_window = tk.Toplevel(self)
        self.ts_window.title('iAnimator - Time-Series Mode')
        #self.range_window.grab_set() # sets window to modal
        self.ts_window.geometry('600x550')
        
        # set title label
        ts_title = tk.Label(self.ts_window, text='TIME-SERIES MODE', font=self.large_font)
        
        # time submission
        forecast_label = tk.Label(self.ts_window, text="forecast time", 
                                  font=self.normal_font)
        entry_format_1 = tk.Label(self.ts_window, text="(YYYYmmddHH)",
                                  font=self.italic_font)
        self.forecast_time = tk.Entry(self.ts_window, width=20, bg='light cyan', 
                                      font=self.normal_font)
        tr_label = tk.Label(self.ts_window, text="time range", 
                                  font=self.normal_font)
        entry_format_2 = tk.Label(self.ts_window, text="(YYYYmmddHH_YYYYmmddHH)",
                                  font=self.italic_font)
        self.time_range = tk.Entry(self.ts_window, width=20, bg='light cyan', 
                                   font=self.normal_font)
        start_label = tk.Label(self.ts_window, text="start time", 
                               font=self.normal_font)
        entry_format_3 = tk.Label(self.ts_window, text="(YYYYmmddHH)",
                                  font=self.italic_font)
        self.start_time = tk.Entry(self.ts_window, width=20, bg='light cyan', 
                                   font=self.normal_font)
        end_label = tk.Label(self.ts_window, text="end time", 
                             font=self.normal_font)
        entry_format_4 = tk.Label(self.ts_window, text="(YYYYmmddHH)",
                                  font=self.italic_font)       
        self.end_time = tk.Entry(self.ts_window, width=20, bg='light cyan', 
                                 font=self.normal_font)
        h_label = tk.Label(self.ts_window, text="time step(hours)", 
                           font=self.normal_font)
        self.step_size = tk.Entry(self.ts_window, width=8, bg='light cyan', 
                                  font=self.normal_font)
        measurement_label = tk.Label(self.ts_window, text="measurement", 
                                     font=self.normal_font)
        entry_format_5 = tk.Label(self.ts_window, text="(d, v, b brbt)", 
                                  font=self.italic_font)
        self.measurement = tk.Entry(self.ts_window, width=8, bg='light cyan')
        instrument_label = tk.Label(self.ts_window, text="instrument", font=self.normal_font)
        self.instrument  = tk.Entry(self.ts_window, width=8, bg='light cyan')
        tomography_label = tk.Label(self.ts_window, text="tomography", font=self.normal_font)
        self.tomography  = tk.Entry(self.ts_window, width=8, bg='light cyan')
        
        # submit button
        submit_button = tk.Button(self.ts_window, text="SUBMIT", bg='beige',
                                  padx=30, pady=10, font=self.normal_font_bold,
                                  command=self.process_ts_data)
        
        # set grid
        ts_title.grid(row=0, column=1, columnspan=2, sticky='W')
        forecast_label.grid(row=1, column=0, padx=5, pady=(10,0), sticky='E')
        entry_format_1.grid(row=2, column=0, padx=5)
        self.forecast_time.grid(row=1, column=1, padx=5, pady=(10,0), sticky='W')
        tr_label.grid(row=3, column=0, padx=5, pady=(10,0), sticky='E')
        entry_format_2.grid(row=4, column=0, padx=5)
        self.time_range.grid(row=3, column=1, padx=5, pady=(10,0), sticky='W')
        start_label.grid(row=5, column=0, padx=5, pady=(10,0), sticky='E')
        entry_format_3.grid(row=6, column=0, padx=5)
        self.start_time.grid(row=5, column=1, padx=5, pady=(10,0), sticky='W')
        end_label.grid(row=7, column=0, padx=5, pady=(10,0), sticky='E')
        entry_format_4.grid(row=8, column=0, padx=5)
        self.end_time.grid(row=7, column=1, padx=5, pady=(10,0), sticky='W')
        h_label.grid(row=9, column=0, padx=5, pady=(10,0), sticky='E')
        self.step_size.grid(row=9, column=1, padx=5, pady=(10,0), sticky='W')
        measurement_label.grid(row=10, column=0, padx=5, pady=(10,0), sticky='E')
        entry_format_5.grid(row=11, column=0, padx=5)
        self.measurement.grid(row=10, column=1, padx=5, pady=(10,0), sticky='W')
        instrument_label.grid(row=12, column=0, padx=5, pady=(10,0), sticky='E')
        self.instrument.grid(row=12, column=1, padx=5, pady=(10,0), sticky='W')
        tomography_label.grid(row=13, column=0, padx=5, pady=(10,0), sticky='E')
        self.tomography.grid(row=13, column=1, padx=5, pady=(10,0), sticky='W')
        submit_button.grid(row=14, column=0, columnspan=2, pady=10)

        # set defaults
        self.measurement.insert(0, 'd')
        self.instrument.insert(0, 'ace0')
        self.tomography.insert(0, 'ips')
        self.step_size.insert(0, '6')
        return
    
    def generate_animation(self) -> None:
        """
        Triggers the animation program to run. Checks the values of each
        parameter to ensure the program can run.
        """
        
        print('Generate Button Pressed\ntriggering animation program...')
        print('user selected variables...\n')
        
        # initializing dictionary
        self.args = {}

        # grab current time and round it to the nearest hour
        # saves a nf (non-formatted time) and a formatted time
        current_time = datetime.now(timezone.utc)
        if current_time.minute >= 30:
            current_time = current_time + timedelta(hours=1)
            self.current_time_nf = current_time.replace(minute=0, second=0, microsecond=0)
        else:
            self.current_time_nf = current_time.replace(minute=0, second=0, microsecond=0)
        self.current_time = self.current_time_nf.strftime('%Y-%m-%d-%H:%M')
        print(f'Reference Time = {self.current_time}')

        # store starting and ending times
        st = (self.current_time_nf - timedelta(self.past)).strftime('%Y-%m-%d-%H:%M')
        et = (self.current_time_nf + timedelta(self.future)).strftime('%Y-%m-%d-%H:%M')
        self.args['start_time'] = st
        self.args['end_time'] = et
        self.args['step_size'] = self.h

        # store command file early
        self.cmd_file = default_command
        
        # store search directory
        search_directory = self.search_directory.get()
        self.args['search_directory'] = search_directory
        print(f'Search Directory = {search_directory}')
        
        # store out directory
        out_dir = self.out_directory.get()
        self.args['out_directory'] = out_dir
        print(f'Output Directory = {out_dir}')
        
        # store outfile
        outfile = self.outfile.get()
        self.args['outfile'] = outfile
        print(f'Outfile = {outfile}')
        
        # store search choice
        search_choice = int(self.search_choice.get())
        self.args['mode'] = search_choice
        print(f'Search Choice = {search_choice}')
        
        # store video format
        video_format = self.video_format.get()
        self.args['video_format'] = video_format
        print(f'Vide Format = {video_format}')
        
        # store image format
        image_format = self.img_format.get()
        self.args['image_format'] = image_format
        print(f'Image Format = {image_format}')
        
        # store resize bool
        bResize = self.bResize.get()
        self.args['bResize'] = bResize
        print(f'Resize = {bResize}')

        # initialize range mode
        if search_choice == 2:
            print('opening range widget...')
            self.range_widget()
        elif search_choice == 3:
            print('opening list widget...')
            self.list_widget()
        elif search_choice == 4:
            print('opening standard widget...')
            self.standard_widget()
        elif search_choice == 5:
            print('opening time-series window')
            self.ts_widget()
        
    
def gui_mode():

    # start GUI
    app = App()
    app.mainloop()

    return