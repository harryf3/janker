import apiInteractions
import videogeneration
import requests
import os
import datetime
from tqdm import tqdm

def setupdir(dir):
    trydir = dir
    trynum = 0
    while(os.path.exists(trydir)):
        trydir = f'{dir}{trynum}'
        trynum+=1
    os.makedirs(trydir)
    with open(f'{trydir}/data.txt','w+') as tdtxtfile:
        now = str(datetime.datetime.now())
        tdtxtfile.write(f'{now} {dir} \n')
    return f'{trydir}'


#possible periods hour, day, week, month, year, all
#jankCount max 100
def jank(jankCount=100,timePeriod='day',tts=True):
    targetCount = 0
    targetList = []
    failures = []
    with open("Videos.txt",'w+') as f:
        f.truncate(0)
    with open("targets.txt") as targetTXTfile:
        print("Target Subreddits")
        for line in targetTXTfile:
            rlinet = line.rstrip('\n')
            if('#' not in rlinet):
                targetList.append(rlinet)
                targetCount += 1
    for targetSub in targetList:
        directoryName = setupdir(targetSub)
        urls = apiInteractions.pull(targetSub,jankCount,timePeriod)
        titledic = {}

        print(f'Janking {targetSub}')
        print('Beginning download from reddit')
        progbar = tqdm(total=jankCount)
        with open(f'{directoryName}/data.txt','a') as tdtxtfile:
            for i,url in enumerate(urls):
                tdtxtfile.write(f'{i} {url[0]} {url[1]} \n')
                ext = os.path.splitext(url[0])[1]
                titledic[i] = url[1]
                if('?' in ext):
                    ext = ext.split('?')[0]
                    res = requests.get(url[0])
                    with open(f'{directoryName}/{i}{ext}','wb') as imgf:
                        imgf.write(res.content)

                    audiourl = os.path.splitext(url[0])[0].split('_')[0]+'_audio'+os.path.splitext(url[0])[1]
                    res2 = requests.get(audiourl)
                    
                    if('Access Denied' not in str(res2.content)) and ('AccessDenied' not in str(res2.content)):      
                        with open(f'{directoryName}/{i}_audio{ext}','wb') as imgf:
                            imgf.write(res2.content)
                    progbar.update(i)
                else:
                    res = requests.get(url[0])
                    with open(f'{directoryName}/{i}{ext}','wb') as imgf:
                        imgf.write(res.content)
                    progbar.update(i)
        progbar.close()
        print('Download from reddit complete')

        print('Beginning Clip Generation')

        files = os.listdir(directoryName)
        progbar = tqdm(total=len(files)-1)
        clips = []
        for i,file in enumerate(files):
            if('.txt' not in file and '_audio' not in file):
                num = os.path.splitext(file)[0]
                progbar.update(i)
                try:
                    clips.append(videogeneration.generateClip(f'{directoryName}/{file}',titledic[int(num)],tts=tts))
                except:
                    print(f'Clip generation failed Clip {i} {file} ')
                
        progbar.close()

        textTimePeriod = ''
        if(timePeriod == 'day'):
            textTimePeriod = 'Today'
        elif(timePeriod == 'hour'):
            textTimePeriod = 'This Hour'
        elif(timePeriod == 'week'):
            textTimePeriod = 'This Week'
        elif(timePeriod == 'month'):
            textTimePeriod = 'This Month'
        elif(timePeriod == 'year'):
            textTimePeriod = 'This Year'
        elif(timePeriod == 'all'):
            textTimePeriod = 'Alltime'
        try:
            ymd = str(datetime.datetime.now()).split(' ')[0]
            vidTitle = f'Best of r {targetSub} {textTimePeriod} {ymd}'.title()
            videogeneration.generateVideo(vidTitle,clips)
            with open("Videos.txt",'a') as f:
                f.write(vidTitle)
            print(f'{targetSub} Janking Finished')
        except:
            failures.append(f'{targetSub}')
            print(f'{targetSub} Video Generation Failed')
            
    print('Done')


#jank(50)