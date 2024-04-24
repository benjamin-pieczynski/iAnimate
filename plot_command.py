#-----------------------------------------------------------------------#
#
# FUNCTION: run_ts_plot
#
# PROGRAMMER: Benjamin Pieczynski - 01/26/2024
#
# PURPOSE:
#       Run ts_plot program with the input commands to generate a 
#       tomography plot of the forecast with a line marking the
#       current time that the animation will show.
#
# INPUTS:
#       mes             str     n,v,b measurement selection
#       instrument      str     selected instrument
#       forecast_date   str     yyyymmddhh format
#       tomo_dir        str     path to tomography files
#       out_dir         str     output directory
#       fname           str     name of the output_file
#       cur_time        str     time to plot vertical line
#       tomo            str     tomography for ts_plot program
#
# OUTPUTS:
#       Creates a time-series plot using the ts_plot program
#
# MODIFICATIONS
# V3.0.0 - added run_ts_plot and run_ts_forecast
#
#-----------------------------------------------------------------------#

import subprocess

def run_ts_forecast(mes, instrument, forecast_date, tomo_dir, 
                    out_dir, fname, cur_time) -> str:
    command = f'ts_plot -{mes} -i "{instrument}" -f {forecast_date}'\
              f' -t "ips" -td {tomo_dir} -od {out_dir} -ct {cur_time}'
    print('running command:', command)
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f'rm {out_dir}/Ea*', shell=True, check=True)
    subprocess.run(f'mv {out_dir}/e3* {out_dir}/{fname}', shell=True, check=True)
    return command

def run_ts_plot(mes, instrument, forecast_date, time_range,
                tomo, tomo_dir, out_dir, fname, 
                cur_time) -> str:
    command = f'ts_plot -{mes} -i "{instrument}" -f {forecast_date}'\
              f' -tr {time_range} -t {tomo} -td {tomo_dir} -od {out_dir} -ct {cur_time}'
    print('running command:', command)
    subprocess.run(command, shell=True, check=True)
    subprocess.run(f'rm {out_dir}/Ea*', shell=True, check=True)
    subprocess.run(f'mv {out_dir}/e3* {out_dir}/{fname}', shell=True, check=True)
    return command