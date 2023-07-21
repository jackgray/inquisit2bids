#! /bin/env python3

# Rename files from inquisit aliens task

from hashlib import new
import os
import glob
import shutil
import filedate
import pytz
from filedate.Utils import Name
from datetime import datetime
from datetime import date as date_fmt
from datetime import timedelta as td
import sys

import pandas as pd

est = pytz.timezone('US/Eastern')
gmt = pytz.timezone('GMT')


if len(sys.argv[1]) > 0:
    basepath = sys.argv[1]
else:
    print("No path specified in command line arg. Using the directory of this script.")
    basepath = os.getcwd()

def rename(path):
    dupecount = 0
    dupecount2 = 0
    new_path = os.path.join(path, 'aliens')
    print("newpath: ", new_path)
    try:
        shutil.rmtree(new_path)
        os.mkdir(new_path)
    except:
        print("Failed")
        pass

    print("Renaming files in path ", path)
    
    for root, dirs, files in os.walk(path):
        
        print(root)
        for file in files:
            # print(file)
            fileparts = file.split('.')[0].split('_')
            # print(fileparts)
            # print(fileparts)
            ses = 'null'
            if fileparts[3] == 'quicktutorial1':
                date_ = fileparts[-1]
                dateparts = date_.split('iqdat')[0].split('-')
                print('DATEPARTS: ', dateparts)
                # dt = datetime(int(dateparts[0]), int(dateparts[1]), int(dateparts[2]), 0, 0, 0, 0)
                dt = datetime(int(dateparts[0]), int(dateparts[1]), int(dateparts[2]), int(dateparts[3]), int(dateparts[4]), int(dateparts[5]), int(dateparts[6]))
                print('dateparts:', dateparts)
                print('dt: ', dt)
                # datestring = ''.join(dateparts[0:3])
                # print('datestring: ', datestring)
                training_or_tutorial = fileparts[3]
                summary_or_raw = fileparts[4]
                subj = fileparts[5].strip()
                
                # prev_ses = ses
                ses = ''.join(dateparts).split('.')[0]
                print('ses :', ses)
                task = fileparts[0][0:6]
                # acq = '-'.join(fileparts[0:5]) # for including payoff and rocket
                acq = fileparts[0][6:]
                
                # modify date created to match real date created
                print("Correcting 'date created' metadata... (", dt, ")")
                File_Date = filedate.File(os.path.join(root,file))
                File_Date.set(modified = dt)                
                          
            # if sexdiff in the name, skip
            elif len(fileparts) == 8: 
                print(fileparts)
                continue
            else:
                continue
            
            # New file name in BIDS format
            bidsfile = '_'.join(['sub-' + subj, 'ses-' + ses, 'task-' + task, 'acq-' + acq, summary_or_raw + '.tsv'])   
            dstpath = os.path.join(new_path, 'sub-'+subj, 'ses-'+ses)
            print('dstPath: ', dstpath)
            try:    
                os.makedirs(dstpath)
            except Exception as e:
                print(e)
                pass
            try:
                shutil.copy2(os.path.join(root, file), os.path.join(dstpath, bidsfile))
            except:
                print("Failed to copy:")
                print(bidsfile)
    
    # rename dates into ordered session number
    for sub in os.listdir(new_path):
        if 'sub-summary' in sub or 'sub-raw' in sub or 'sub-test' in sub:
            shutil.rmtree(os.path.join(new_path,sub))
            continue
        print()
        print()
        print('New Subject ', sub)
        dt = False
        # print('\n')
        # print(sub)
        count = 0
        days = 0    
        
        for ses in sorted(os.listdir(os.path.join(new_path, sub))):
            print()
            print('ses2: ', ses)
            datestring = ses.split('-')[-1]
            print('datestring: ', datestring)
            # try:
            #     prev_dt = dt
            # except:
            #     pass
            if dt != False:
                prev_dt = dt
                dt = datetime(int(datestring[0:4]), int(datestring[4:6]), int(datestring[6:8])  , int(datestring[8:10]), int(datestring[10:12]), int(datestring[12:14]), int(datestring[14:17]))
                dtgmt = gmt.localize(dt)
                dt = dtgmt.astimezone(est)
                if dt.hour < 6:
                    print("Before 5am = day before")
                    olddt=dt
                    dt = dt - td(days=1)
                    print(olddt, '--->', dt)
                time_since = (dt - prev_dt)
                days_since = date_fmt(dt.year,dt.month,dt.day) - date_fmt(prev_dt.year, prev_dt.month, prev_dt.day) #time_since.days
                days = days_since.days
                print('time since = ', dt, ' - ', prev_dt, ' = ', time_since)
                print('days: ', days)
                hours = time_since.seconds / 3600
                # if days>1 and hours > 20:
                #     print("More than 20 hours since last task. Decreasing days_since by 1: ", days, '-->', days-1)
                #     days = days-1
                if days == 0:
                    print("HOURS SINCE: ", hours)
                    # dupecount += 1
                    if hours > 12:
                        print("changing days to 1 because hours > 12: ", hours)
                        days = 1
                    else:
                        dupecount2 += 1
                        days = 0
                

            else:
                print('First session')
                days = 1
                dt = datetime(int(datestring[0:4]), int(datestring[4:6]), int(datestring[6:8]), int(datestring[8:10]), int(datestring[10:12]), int(datestring[12:14]), int(datestring[14:17]))   
                dtgmt = gmt.localize(dt)
                dt = dtgmt.astimezone(est)
                if dt.hour < 6:
                    print("Before 5am = day before")
                    olddt=dt
                    dt = dt - td(days=1)
                    print(olddt, '--->', dt)
                    
            try:
                filepath = os.path.join(new_path, sub, ses, '*summary*')
                file = glob.glob(filepath)[0]   
                data = pd.read_csv(file, sep='\t')                                           
                date_arr = data['startdate'][0].split('-')
            except Exception as e:
                filepath = os.path.join(new_path,sub, ses, '*raw*')
                file = glob.glob(filepath)[0]
                data = pd.read_csv(file, sep='\t')  
                date_arr = data['date'][0].split('-')
                print(e)
    
            # curr_date = date_fmt(int(date_arr[0]), int(date_arr[1]), int(date_arr[2]))
                
                # Sometimes subjects try to complete the task after midnight for the day before or before midnight for the next day
                # if int(datestring[8:10]) < 2:
                #     date_arr = [int(datestring[0:4]), int(datestring[4:6]), int(datestring[6:8])]
                #     curr_date = date_fmt(int(date_arr[0]), int(date_arr[1]), int(date_arr[2])) - td(days=1)

                  # At this stage the previous date and current date should not be the same. Flag duplicate for later
                # if curr_date == prev_date: 
                #     duplicate = True
                #     os.chmod(file, 0o777)
                #     shutil.rmtree(os.path.join(new_path, sub, ses))
                #     # print('removing file', file)
                #     # os.remove(file)
                #     continue
                # else:
                #     duplicate = False
              
            # else:
            #     try:
            #         filepath = os.path.join(new_path, sub, ses, '*summary*')
            #         file = glob.glob(filepath)[0] 
            #         data = pd.read_csv(file, sep='\t')  
            #         date_arr = data['startdate'][0].split('-')  
            #     except:
            #         filepath = os.path.join(new_path,sub, ses, '*raw*')
            #         file = glob.glob(filepath)[0]
            #         data = pd.read_csv(file, sep='\t')  
            #         date_arr = data['date'][0].split('-')
            #     curr_date = date_fmt(int(date_arr[0]), int(date_arr[1]), int(date_arr[2])) 
            #     prev_date = curr_date 
            #     duplicate = False
                        
            # if days is < 1 then there is a session that was completed on the same day
            if days < 1:
                # time_since = 1
                shutil.rmtree(os.path.join(new_path,sub,ses))
                dupecount+=1
                continue
            count += int(days)
            countstr = str(count)
            print('countstr: ', countstr)
            prev_count = count
            # if '.' in os.path.join(new_path, sub, ses):
            #     print()
            #     print("/n/n/n/n/n/n/n/n/n/n/n")
            #     print('DUPLICATE SESSION')
            #     print("/n/n/n/n/n/n/n/n/n/n/n")
            #     # os.remove(file)
                
                # countstr = '300'
                # count += 1 #int(time_since)
                # countstr = str(count)
                # datestring.split('.')[0]
                # time_since = 1
                
                # countstr = countstr + 'a'
            
            # print('dt:', dt,  'since: ', days_since, ' | ', countstr)

            
            if len(countstr) < 2:
                countstr = '0' + str(count)
            newses = '-'.join(['ses', countstr])
            print('newses: ', newses)
            os.rename(os.path.join(new_path, sub, ses), os.path.join(new_path, sub, newses))
            for file in os.listdir(os.path.join(new_path, sub, newses)):
                # print('Replacing date string ', datestring, 'with count ', countstr)
                newfile = file.replace(datestring, countstr)
                # print('newfile: ', newfile)
                os.rename(os.path.join(new_path, sub, newses, file), os.path.join(new_path, sub, newses, newfile))
        print('duplicate count: ', dupecount, dupecount2)

rename(basepath)
