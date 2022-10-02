import ttsparse
import moviepy.editor as mp
import os
import random

#write_videofile(f'{number}.mp4',fps=24,codec='mpeg4',audio=True)

def generateClip(url,title,tts):
    number,ext = os.path.splitext(url)
    print(title)
    if(ext != '.mp4' and ext != '.mov' and tts):
        text = ttsparse.parse(url)
    else:
        text = ''
    text = text.strip()
    if(text != '' and ext != '.mp4' and ext != '.mov'):
        ttsparse.tts(text,f'{number}.mp3')
        audioclip = mp.AudioFileClip(f'{number}.mp3')
        if(ext == '.gif'):
            clip = mp.VideoFileClip(url).resize(height=720).loop(n=4).set_audio(audioclip)
            clip=clip.set_duration(audioclip.duration)
        else:
            clip = mp.ImageClip(url,duration=audioclip.duration).resize(height=720).set_audio(audioclip)
        if(clip.duration <= 4):
            clip.set_duration(4)
        #clip = clip.resize((720,480))
        
        if(clip.w>=1280):
            clip = clip.resize((1280,720))
        return clip
    elif(text == '' and ext != '.mp4' and ext != '.mov' and title != ''):
        ttsparse.tts(title,f'{number}.mp3')
        audioclip = mp.AudioFileClip(f'{number}.mp3')
        if(ext == '.gif'):
            clip = mp.VideoFileClip(url).resize(height=720).loop(n=4)
            clip=clip.set_duration(audioclip.duration)
        else:
            clip = mp.ImageClip(url,duration=audioclip.duration).resize(height=720).set_audio(audioclip)
        if(clip.duration <= 5):
            clip.set_duration(5)
        if(clip.w>=1280):
            clip = clip.resize((1280,720))
        return clip
    elif(text == '' and ext != '.mp4' and ext != '.mov' and title == ''):
        if(ext == '.gif'):
            clip = mp.VideoFileClip(url).resize(height=720).loop(n=4)
            clip=clip.set_duration(5)
        else:
            clip = mp.ImageClip(url,duration=5).resize(height=720)
        #if(clip.duration <= 5):
        #    clip.set_duration(5)
        if(clip.w>=1280):
            clip = clip.resize((1280,720))
        return clip
    else:
        if(os.path.exists(f'{number}_audio.mp4')):
            audioclip = mp.AudioFileClip(f'{number}_audio.mp4')
            clip = mp.VideoFileClip(url).resize(height=720).set_audio(audioclip)
        else:
            clip = mp.VideoFileClip(url).resize(height=720)
        if(clip.w>=1280):
            clip = clip.resize((1280,720))
        return clip

def generateVideo(name,clipArray,music=False):
    video = mp.concatenate(clipArray, method='compose')
    if(music):
        sound = mp.AudioFileClip(random.choice(['cr.mp3','dog.mp3']))
        originalVideoDur = video.duration
        if(video.audio):
            video = video.set_audio(mp.CompositeAudioClip([sound,video.audio]))
        else:
            video = video.set_audio(sound)
        video = video.set_duration(originalVideoDur)
    video=video.resize((1280,720))
    if(video.duration >= 900):
        video = video.set_duration(900)
    video.write_videofile(f'{name}.mp4',audio=True,codec='mpeg4',fps=24)