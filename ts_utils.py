#----------------------------------------------------------------------#
# 
# MODULE: ts_utils.py
#
# PROGRAMMER: Benjamin Pieczynski - 01/26/2024
#
# PURPOSE:
#    Create time array of forecast times that will be used to make
#    the time series plots with ts_plot.
#
# MODIFICATIONS:
#   v3.1.0 - ported to png_animator
#
#----------------------------------------------------------------------#

from datetime import datetime, timedelta

def utc_days_difference(time1_str, time2_str):
    '''IN:
        time1_str (str): earliest time
        time2_str (str): latest time
        
       OUT:
        difference (float): days difference in time'''
    # Convert strings to datetime objects
    time1 = datetime.strptime(time1_str, '%Y%m%d%H')
    time2 = datetime.strptime(time2_str, '%Y%m%d%H')

    # Calculate the difference
    time_difference = time2 - time1

    # Convert the difference to days
    difference = time_difference.total_seconds() / 86400

    return difference

# convert a time to a datetime object in UT
def convert_to_ut_obj(time_string):
    '''INOUT:
            time_string     str->datetime_obj YYYYMMDDHH'''
    return datetime.strptime(time_string, "%Y%m%d%H")

# Format the result datetime as a string in "YYYYMMDDHH" format
def convert_to_str(dt_obj):
    '''INOUT:
            dt_obj    datetime_obj->str YYYYMMDDHH'''
    return dt_obj.strftime('%Y%m%d%H')
    
# make the array of forecast times
def make_ts_time_array(forecast_time, past, future, h):
    '''INPUTS: 
            forecast_time   str     YYYYMMDDHH
            past            float   days into the past
            future          float   days into the future
            h               float   time step in hours
            
       OUTPUTS:
            time_array      str     array of time strings'''

    # convert forecast time to datetime object
    ref_time = convert_to_ut_obj(forecast_time)
    
    # get start and stop times
    start_time = ref_time-timedelta(days=past  )
    end_time   = ref_time+timedelta(days=future)
    
    # build the time array
    time_array = []
    ct = start_time
    while ct <= end_time:
        string = convert_to_str(ct)
        time_array.append(string)#string[:9] + string[9:12])
        ct = ct+timedelta(hours=h)
    return time_array