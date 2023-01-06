
import os
import pyaudio
import wave
from pathlib import Path
import streamlit as st
import speech_recognition as sr


def Intro():
    st.title("Anti-Social Behaviour Detecion")
    st.subheader(f"This project aims at identifying activites against social norms.\n"
                 f"It covers 3 major aspects:\n"
                 f"1. Weapon Detection\n"
                 f"2. Hate Speech Recognition\n"
                 f"3. Violence Detection")
    #st.subheader("It covers 3 major aspects:")

def Weap_detection():
    st.title("WEAPON DETECTION")
    st.subheader("This Weapon Detection Project takes the input as image/video and outputs image/video with weapon bounded in a rectangle with confidence score.")
    
    uploaded_file = st.file_uploader("Choose a file")
    print("#"*20)
    print(uploaded_file)
    print("#"*20)
    
    if uploaded_file!=None:
        file_details = {"File Name":uploaded_file.name,
                        "File Type":uploaded_file.type,
                        "File Size":uploaded_file.size}
        st.write(file_details)
        if uploaded_file.type == 'video/mp4':
            st.video(uploaded_file)
        else:
            st.image(uploaded_file,width=500)
        
    if st.button('DETECT'):
        app_dir = os.path.abspath(os.path.dirname(__file__))
        print(app_dir)
        weapon_path = os.path.join(app_dir, 'yolo', 'weapon.ipynb')
        yolov5_dir = os.path.join(app_dir, 'yolo', 'yolov5')

        uploads_dir = os.path.join(app_dir, 'instance', 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)

        save_path = Path(uploads_dir, uploaded_file.name)

        with open(save_path, mode = 'wb') as w:
            print("**************  file Opened")
            w.write(uploaded_file.getbuffer())
            print("**************  file written")
            if st.success("Output"):
                print("**************  output found")
                
                os.chdir(yolov5_dir)
                os.system('python detect.py --weights runs/train/exp/weights/best.pt --img 640 --conf 0.25 --source ../../instance/uploads')
                print("**************  ran weapon")

                runs_detect_dir = os.path.join(yolov5_dir, 'runs', 'detect')
                exp_dir = (max([os.path.join(runs_detect_dir,d) for d in os.listdir(runs_detect_dir)], key=os.path.getmtime))
                print(exp_dir)
                

                if exp_dir:
                    output_paths = os.path.join(exp_dir)
                    print(output_paths)
                    output_path = (max([os.path.join(output_paths,d) for d in os.listdir(output_paths)], key=os.path.getmtime))
                    print(output_path)
                    
                    if output_path and os.path.exists(output_path):
                        with open(output_path, 'rb') as f:
                            output_data = f.read()
                            if output_path.endswith('.mp4'):
                                st.video(output_data,format="video/mp4")
                            else: 
                                st.image(output_data)
                            f.close()
        os.remove(save_path)

def Speech_reco():
    st.title("HATE SPEECH RECOGNITION")
    st.subheader("This project takes input as audio and display a list of abusive word in the audio.")
    
    if st.button('RECORD'):
        with st.spinner(f'Recording for 10 seconds ....'):
            record()
        st.success("Recording Completed")

    app_dir = os.path.abspath(os.path.dirname(__file__))
    uploads_dir = os.path.join(app_dir,'recordings')
        
    if st.button('PLAY'):
        try:
            audio_file = open(os.path.join(uploads_dir,"record.wav"),'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format = 'audio/wav')
        except:
            st.write("Please record sound first")
            
    if st.button('DETECT'):
        # app_dir = os.path.abspath(os.path.dirname(__file__))
        # uploads_dir = os.path.join(app_dir,'recordings')
        hate_words = audio_input(os.path.join(uploads_dir,"record.wav"))
        if hate_words != []:
            st.subheader("Hate Speech Detected")
            st.write(hate_words)
        else:
            st.subheader("No hate speech detected")

def audio_input(source='record.wav'):
    speech_recognizer = sr.Recognizer()
    knowledgebase = []
    app_dir = os.path.abspath(os.path.dirname(__file__))
    kb_dir = os.path.join(app_dir,'Hate_Speech_Detection')
    os.chdir(kb_dir)
    with open(r'knowledgebase.txt') as f:
        for index, line in enumerate(f):
            word = line.strip().lower()
            knowledgebase.append(word)
    with sr.AudioFile(source) as source_file:
        print("Recognizing...")
        audio = speech_recognizer.record(source_file)
        text = speech_recognizer.recognize_google(audio)
        print(text)
        #return(text)
        hate_words = []
        for word in knowledgebase:
            if word in text:
                hate_words.append(word)
        return(hate_words)

def record():    
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    
    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT,
                    channels = CHANNELS,
                    rate = RATE,
                    input = True,
                    frames_per_buffer = CHUNK)
    
    print("start recording...")
    
    frames = []
    seconds = 10
    for i in range(0, int(RATE/CHUNK*seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
        
    print("recording stopped!!")
    
    stream.stop_stream()
    stream.close()
    p.terminate()
    
    app_dir = os.path.abspath(os.path.dirname(__file__))
    uploads_dir = os.path.join(app_dir,'recordings')
    os.makedirs(uploads_dir, exist_ok=True)

    w = wave.open(os.path.join(uploads_dir,"record.wav"),'wb')
    w.setnchannels(CHANNELS)
    w.setsampwidth(p.get_sample_size(FORMAT))
    w.setframerate(RATE)
    w.writeframes(b''.join(frames))
    w.close()
    
def Vio_detection():
    st.title("VIOLENCE DETECTION")
    st.subheader("This Violence Detection Project takes the input as image/video and outputs image/video with any sort of violence bounded in a rectangle with confidence score.")
    load_file = st.file_uploader("Choose a file")
    
    print("#"*20)
    print(load_file)
    print("#"*20)
    
    if load_file!=None:
        file_details = {"File Name":load_file.name,
                        "File Type":load_file.type,
                        "File Size":load_file.size}
        st.write(file_details)
        if load_file.type == 'video/mp4':
            st.video(load_file)
        else:
            st.image(load_file,width=500)
        
    if st.button('DETECT'):
        app_dir = os.path.abspath(os.path.dirname(__file__))
        violence_path = os.path.join(app_dir, 'yolovo', 'violence.ipynb')
        yolov5_dir = os.path.join(app_dir, 'yolovo', 'yolov5')

        load_dir = os.path.join(app_dir, 'instancetwo', 'uploadstwo')
        os.makedirs(load_dir, exist_ok=True)

        save_path = Path(load_dir, load_file.name)

        with open(save_path, mode = 'wb') as w:
            print("**************  file Opened")
            w.write(load_file.getbuffer())
            print("**************  file written")
            if st.success("Output"):
                print("**************  output found")
                print(violence_path)
                print(os.path.isfile(violence_path))

                os.chdir(yolov5_dir)
                os.system('python detect.py --weights runs/train/exp/weights/best.pt --img 640 --conf 0.25 --source ../../instancetwo/uploadstwo')
                print("**************  ran weapon")

                runs_detect_dir = os.path.join(yolov5_dir, 'runs', 'detect')
                exp_dir = (max([os.path.join(runs_detect_dir,d) for d in os.listdir(runs_detect_dir)], key=os.path.getmtime))
                print(exp_dir)
                

                if exp_dir:
                    output_paths = os.path.join(exp_dir)
                    print(output_paths)
                    output_path = (max([os.path.join(output_paths,d) for d in os.listdir(output_paths)], key=os.path.getmtime))
                    print(output_path)
        
                    if output_path and os.path.exists(output_path):
                        with open(output_path, 'rb') as f:
                            output_data = f.read()
                            if output_path.endswith('.mp4'):
                                st.video(output_data)
                            else:
                                st.image(output_data)
                            f.close()
        os.remove(save_path)


st.sidebar.title("App Mode")
app_mode = st.sidebar.selectbox("Choose the Activity",["About","Weapon Detection","Hate Speech Recognition","Violence Detection"])

if app_mode == "About":
    Intro()
    
if app_mode == "Weapon Detection":
    Weap_detection()
    
if app_mode == "Hate Speech Recognition":
    Speech_reco()
    
if app_mode == "Violence Detection":
    Vio_detection()

