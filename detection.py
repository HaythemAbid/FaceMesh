import base64

import streamlit as st
import mediapipe as mp
import cv2
import numpy as np
import tempfile
import time
from PIL import Image
from streamlit_lottie import st_lottie
import requests
import json


mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh

DEMO_IMAGE = 'demo.jpg'
DEMO_VIDEO = 'demo.mp4'

st.title("MediaPipe Face Mesh ")

st.markdown(
    """ 
    <style>
    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
        width: 350px
    }
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
        width: 350px
        margin-left: -350px
    }
    </style>
    """,
    unsafe_allow_html=True,
)
main_bg = "bg.jpg"
st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}
    </style>
    """,
    unsafe_allow_html=True
)
st.sidebar.image("Logo-talan.png", use_column_width=True)
st.sidebar.markdown("---")
st.sidebar.subheader('Parameters')
##########################################
# Shrinking images
@st.cache()
def image_resize(image,width=None, height=None, inter = cv2.INTER_AREA):
    dim = None
    (h,w) = image.shape[:2]

    if width is None and height is None:
        return image

    if width is None:
        r = width/float(w)
        dim = (int(w*r), height)
    else:
        r= width/float(w)
        dim= (width, int(h*r))

    #resizing
    resized = cv2.resize(image,dim,interpolation=inter)

    return resized
############################
#lottie files
def load_lottifile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def load_lottieurl(url : str):

    r=  requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

#############################


app_mode = st.sidebar.selectbox('Choose the App Mode',
                                   ['About App','Run on Image','Run on Video']
                                   )

if app_mode == 'About App':
    lottie_hello = load_lottieurl("https://assets2.lottiefiles.com/packages/lf20_yhpx82cd.json")
    st_lottie(
        lottie_hello,
        speed=1,
        reverse=False,
        loop=True,
        quality="low",
        height=None,
        width=None,
        key=None,
    )

    st.subheader("Overview")
    st.text("""
    MediaPipe Face Mesh is a face geometry solution that estimates 468 3D face
    landmarks in real-time even on mobile devices. It employs machine learning
    (ML) to infer the 3D surface geometry, requiring only a single camera input
    without the need for a dedicated depth sensor. Utilizing lightweight model
    architectures together with GPU acceleration throughout the pipeline,
    the solution delivers real-time performance critical for live experiences.
    
    Additionally, the solution is bundled with the Face Geometry module that
    bridges the gap between the face landmark estimation and useful real-time
    augmented reality (AR) applications.
    It establishes a metric 3D space and uses the face landmark screen positions
    to estimate face geometry within that space. The face geometry data consists
    of common 3D geometry primitives,including a face pose transformation matrix 
    and a triangular face mesh. Under the hood,a lightweight statistical analysis
    method called Procrustes Analysis is employed to drive a robust,
    performant and portable logic.
    The analysis runs on CPU and has a minimal speed/memory footprint on top
    of the ML model inference.
    """)

    st.markdown(
        """ 
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
            width: 350px
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
            width: 350px
            margin-left: -350px
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    # to upload video
    ##st.video('')


elif app_mode=='Run on Image' :
    drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=1)

    st.sidebar.markdown('---')
    st.markdown(
        """ 
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
            width: 350px
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
            width: 350px
            margin-left: -350px
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("**Detected Faces**")
    kpi1_text = st.markdown("0")

    max_faces= st.sidebar.number_input('Maximum Number of Faces', value=2, min_value=1)
    st.sidebar.markdown('---')
    detection_confidence = st.sidebar.slider('Min Detection Confidence', min_value=0.0, max_value=1.0, value=0.5)
    st.sidebar.markdown('---')

    img_file_buffer = st.sidebar.file_uploader("Upload an Image", type=["jpg", "jpeg", "png"])
    if img_file_buffer is not None:
        image = np.array(Image.open(img_file_buffer))
    else:
        demo_image = DEMO_IMAGE
        image = np.array(Image.open(demo_image))

    st.sidebar.text('Original Image')
    st.sidebar.image(image)

    face_count = 0

    ## Dashboard

    with mp_face_mesh.FaceMesh(
        static_image_mode = True,
        max_num_faces = max_faces,
        min_detection_confidence = detection_confidence
    ) as face_mesh:
        results = face_mesh.process(image)
        out_image = image.copy()


        ## face landmark drawing

        for face_landmarks in results.multi_face_landmarks:
            face_count += 1

            mp_drawing.draw_landmarks(
                image = out_image,
                landmark_list= face_landmarks,
                connections= mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec= drawing_spec)

            kpi1_text.write(f"<h1 style='text-align : center ; color:red;'>{face_count}</h1>", unsafe_allow_html=True)

        st.subheader('Output Image')
        st.image(out_image,use_column_width=True)

elif app_mode =='Run on Video':

    st.set_option('deprecation.showfileUploaderEncoding', False)

    use_webcam = st.sidebar.button('Use Webcam')
    record = st.sidebar.checkbox("Record Video")

    if record:
        st.checkbox("Recording", value= True)


    st.sidebar.markdown('---')
    st.markdown(
        """ 
        <style>
        [data-testid="stSidebar"][aria-expanded="true"] > div:first-child{
            width: 350px
        }
        [data-testid="stSidebar"][aria-expanded="false"] > div:first-child{
            width: 350px
            margin-left: -350px
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    max_faces = st.sidebar.number_input('Maximum Number of Faces', value=5, min_value=1)
    st.sidebar.markdown('---')
    detection_confidence = st.sidebar.slider('Min Detection Confidence', min_value=0.0, max_value=1.0, value=0.5)
    tracking_confidence = st.sidebar.slider('Min Tracking Confidence', min_value=0.0, max_value=1.0, value=0.5)
    st.sidebar.markdown('---')

    st.markdown("## Output")

    stframe= st.empty()
    video_file_buffer = st.sidebar.file_uploader("Upload a video", type= ['mp4','mov', 'avi', 'asf','m4v'])
    tffile = tempfile.NamedTemporaryFile(delete=False)


    ## we get our input video here
    if not video_file_buffer:
        if use_webcam:
            vid = cv2.VideoCapture(0)
        else:
            vid = cv2.VideoCapture(DEMO_VIDEO)
            tffile.name = DEMO_VIDEO
    else:
        tffile.write(video_file_buffer.read())
        vid = cv2.VideoCapture(tffile.name)

    width = int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps_input = int(vid.get(cv2.CAP_PROP_FPS))


    ## Recording part
    codec = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    out = cv2.VideoWriter('output1.mp4', codec, fps_input, (width,height))

    st.sidebar.text('Input Video')
    st.sidebar.video(tffile.name)
    fps = 0
    i = 0
    drawing_spec = mp_drawing.DrawingSpec(thickness=2, circle_radius=1)

    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        st.markdown("**Frame Rate**")
        kpi1_text = st.markdown("0")
    with kpi2:
        st.markdown("**Detected Faces**")
        kpi2_text = st.markdown("0")
    with kpi3:
        st.markdown("**Image Width**")
        kpi3_text = st.markdown("0")

    st.markdown("<hr/>", unsafe_allow_html=True)

    ## Face Mesh predictor Dashboard

    with mp_face_mesh.FaceMesh(
        max_num_faces = max_faces,
        min_detection_confidence = detection_confidence,
        min_tracking_confidence= tracking_confidence
    ) as face_mesh:
        prevTime = 0

        while vid.isOpened():
            i += 1
            ret, frame = vid.read()
            if not ret:
                continue


            results = face_mesh.process(frame)
            frame.flags.writeable = True

            face_count = 0

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    face_count += 1

                    mp_drawing.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=drawing_spec,
                        connection_drawing_spec= drawing_spec
                    )

            # FPS counter logic
            currTime = time.time()

            fps = 1 / (currTime - prevTime)
            prevTime = currTime

            if record:
                out.write(frame)

            # Dashboard

            kpi1_text.write(f"<h1 style='text-align : center ; color:red;'>{int(fps)}</h1>", unsafe_allow_html=True)
            kpi2_text.write(f"<h1 style='text-align : center ; color:red;'>{face_count}</h1>", unsafe_allow_html=True)
            kpi3_text.write(f"<h1 style='text-align : center ; color:red;'>{width}</h1>", unsafe_allow_html=True)

            frame = cv2.resize(frame,(0,0), fx= 0.8, fy= 0.8)
            frame = image_resize(image= frame, width= 640)
            stframe.image( frame, channels = 'BGR', use_column_width = True)

    st.text(" Video Precessed")
    output_video = open('output.mp4', 'rb')
    out_bytes = output_video.read()
    st.video(out_bytes)

    vid.release()
    out.release()