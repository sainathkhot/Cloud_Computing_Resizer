from flask import Flask, request, send_file
import cv2 as cv
from PIL import Image, ImageSequence
import numpy as np
import io
import tempfile
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/resize', methods=['POST'])
def resize_media():
    file = request.files['file']
    percentage = int(request.form['percentage'])
    ext = file.filename.split(".")[-1]
    upscale = request.form['upscale'] == 'true'
    downscale = request.form['downscale'] == 'true'
    if (upscale):
        percentage = percentage + 100
        Interpolation = cv.INTER_CUBIC
    else:
        Interpolation = cv.INTER_AREA
    print("\n\nfile : ", file, "\npercentage : ", percentage,"\nExtentsion : ",ext,"\nInterpolation : ", Interpolation)
    if file.filename.lower().endswith((".jpeg", ".jpg", ".png")):
        mime_type = f"image/{ext}"
        resized_file = resize_image(file, percentage, Interpolation)
        return send_file(
            resized_file,
            mimetype=mime_type,
            as_attachment=True,
            download_name=file.filename)
    elif file.filename.lower().endswith((".mp4", ".mov", ".avi", ".mkv", ".3gp")):
        resized_file = resize_video(file, percentage, upscale , downscale)
        mime_type = f"video/{ext}"
        return send_file(
            resized_file,
            mimetype=mime_type,
            as_attachment=True,
            download_name=file.filename)
    elif file.filename.lower().endswith(".gif"):
        resized_file = resize_gif(file, percentage, Interpolation)
        return send_file(
            resized_file,
            mimetype='image/gif',
            as_attachment=True,
            download_name=file.filename)
    else:
        return 'Unsupported file format', 400

def resize_image(input_stream, percentage, Interpolation):
    ext = input_stream.filename.split(".")[-1]
    img = cv.imdecode(np.frombuffer(input_stream.read(), np.uint8), cv.IMREAD_UNCHANGED)
    new_width = int(img.shape[1] * (percentage / 100.0))
    new_height = int(img.shape[0] * (percentage / 100.0))
    resized_frame = cv.resize(img, (new_width, new_height),  interpolation=Interpolation)
    print("\nOld Height : ",img.shape[0],"\nOld Width : ", img.shape[1])
    print("New Height : ",new_height,"\nNew Width : ", new_width)
    _, buffer = cv.imencode('.'+ext, resized_frame)
    print("The image resized successfully")
    return io.BytesIO(buffer)


def resize_video(input_stream, percentage, upscale, downscale):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(input_stream.read())
    temp_file.close()
    cap = cv.VideoCapture(temp_file.name)
    fps = cap.get(cv.CAP_PROP_FPS)
    
    if upscale:
        resize_factor = 1 + percentage / 100
        new_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH) * resize_factor)
        new_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT) * resize_factor)
    
    elif downscale:
        resize_factor = 1 - percentage / 100
        new_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH) * resize_factor)
        new_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT) * resize_factor)
    
    else:
        new_width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
        new_height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))

    print("Resized factors : ", resize_factor, "\nH : ", new_height,"\nW", new_width)
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    output_stream = io.BytesIO()
    out = cv.VideoWriter(temp_file.name + "_resized.mp4", fourcc, fps, (new_width, new_height))
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        resized_frame = cv.resize(frame, (new_width, new_height))
        out.write(resized_frame)
    
    print("File : ", temp_file.name)
    cap.release()
    out.release()
    
    # If the input video has audio, write the resized video with audio
    if cap.get(cv.CAP_PROP_FOURCC) != 0:
        output_stream.write(open(temp_file.name + "_resized.mp4", 'rb').read())
    else:
        # If the input video has no audio, write only the video frames
        video_frames = io.BytesIO()
        video_frames.write(open(temp_file.name + "_resized.mp4", 'rb').read())
        video_frames.seek(0)
        output_stream.write(video_frames.read())
    
    output_stream.seek(0)
    
    # os.remove(temp_file.name + "_resized.mp4")
    # os.remove(temp_file.name)
    
    return output_stream



def resize_gif(input_stream, percentage, Interpolation):
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(input_stream.read())
    temp_file.close()
    frames = []
    img = Image.open(temp_file.name)
    for frame in ImageSequence.Iterator(img):
        frame = frame.convert("RGBA")
        frame = cv.cvtColor(np.array(frame), cv.COLOR_RGBA2BGRA)
        width, height = frame.shape[1], frame.shape[0]
        new_width = int(width * (percentage / 100.0))
        new_height = int(height * (percentage / 100.0))
        resized_frame = cv.resize(frame, (new_width, new_height), interpolation=Interpolation)
        frames.append(resized_frame)
    frames_pil = [Image.fromarray(cv.cvtColor(frame, cv.COLOR_BGRA2RGBA)) for frame in frames]
    frames_pil[0].save(temp_file.name,format="gif", save_all=True, append_images=frames_pil[1:], loop=0)
    print("The GIF resized successfully")
    return temp_file.name

if __name__ == '__main__':
    app.run(debug=True)