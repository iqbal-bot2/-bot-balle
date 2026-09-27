import gradio as gr
import cv2
def suivre_balle(video):
    cap = cv2.VideoCapture(video)
    ret, frame = cap.read()
    if not ret:
        return "Video invalide"
    h, w = frame.shape[:2]
    tracker = cv2.TrackerCSRT_create()
    bbox = (w//2 - 60, h//2 - 60, 120, 120)
    tracker.init(frame, bbox)
    last_x = bbox[0]
    while True:
        ret, frame = cap.read()
        if not ret: break
        ok, box = tracker.update(frame)
        if ok: last_x = box[0]
    cap.release()
    if last_x < w/3:
        return "BALLE A GAUCHE"
    elif last_x < 2*w/3:
        return "BALLE AU MILIEU"
    else:
        return "BALLE A DROITE"
demo = gr.Interface(fn=suivre_balle, inputs=gr.Video(), outputs="text", title="Bot Suivi Balle")
demo.launch(server_name="0.0.0.0", server_port=10000)
