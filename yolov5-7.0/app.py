import os
from flask import Flask, request, jsonify, send_from_directory
import torch
from models.common import DetectMultiBackend
from utils.general import non_max_suppression, scale_boxes
from utils.augmentations import letterbox
import cv2
import numpy as np
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = DetectMultiBackend('runs/train/exp3/weights/best.pt', device=device)  # Load your trained model

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'E:\\yolov5Englishpath\\cnn_learn\\yolov5-7.0\\results'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

def draw_boxes(img, pred, names):
    """ Draw bounding boxes on the image """
    img_shape = img.shape  # Original image shape
    print(f"Original image shape: {img_shape}")  # Debugging
    for det in pred:
        if len(det):
            print(f"Detection shape: {det.shape}")  # Debugging
            # Rescale boxes from img_size to original size
            img_shape = (img_shape[1], img_shape[0])  # (width, height)
            print(f"Rescaled image shape: {img_shape}")  # Debugging
            det[:, :4] = scale_boxes((640, 640), det[:, :4], img_shape).round()

            for *xyxy, conf, cls in reversed(det):
                label = f'{names[int(cls)]} {conf:.2f}'
                xyxy = [int(x) for x in xyxy]
                # Draw rectangle and label
                cv2.rectangle(img, (xyxy[0], xyxy[1]), (xyxy[2], xyxy[3]), (0, 255, 0), 2)
                cv2.putText(img, label, (xyxy[0], xyxy[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return img


@app.route('/upload/image', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})

    file = request.files['file']

    if file.filename == '':
        return jsonify({'error': 'No selected file'})

    filename = file.filename
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    img = cv2.imread(filepath)

    # Process image and run YOLOv5 model
    img = letterbox(img, 640, stride=32, auto=True)[0]  # Resize image
    img0 = img.copy()  # Save original image
    img = img.transpose((2, 0, 1))[::-1]  # Convert to CHW and BGR format
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).to(device)  # Ensure tensor is on GPU
    img = img.float()
    img /= 255.0  # Normalize
    if img.ndimension() == 3:
        img = img.unsqueeze(0)

    pred = model(img, augment=False, visualize=False)
    pred = non_max_suppression(pred, 0.25, 0.45, None, False, max_det=1000)

    results = []
    names = model.names  # Class names

    # # Draw bounding boxes on the image
    # img0 = draw_boxes(img0, pred, names)
    #
    # for det in pred:  # Detection results per image
    #     if len(det):
    #         for *xyxy, conf, cls in reversed(det):
    #             results.append({
    #                 'bbox': [int(x) for x in xyxy],
    #                 'confidence': float(conf),
    #                 'class': int(cls)
    #             })
    #
    # detection_image_url = f'/results/{filename}'
    # cv2.imwrite(os.path.join(RESULT_FOLDER, filename), img0)  # Save annotated image
    #
    # return jsonify({'results': results, 'image_url': detection_image_url})
    # 计算每张图像中检测到的小麦数量
    wheat_count = 0
    img0 = draw_boxes(img0, pred, names)

    for det in pred:
        if len(det):
            wheat_count += len(det)

    detection_image_url = f'/results/{filename}'
    cv2.imwrite(os.path.join(RESULT_FOLDER, filename), img0)

    return jsonify({
        'image_url': detection_image_url,
        'wheat_count': wheat_count
    })


@app.route('/results/data/<filename>')
def get_result_data(filename):
    data_file = os.path.join(UPLOAD_FOLDER, f"{filename.split('.')[0]}.json")
    if os.path.exists(data_file):
        return send_from_directory(directory=os.path.dirname(data_file), filename=os.path.basename(data_file))
    else:
        return jsonify({'error': 'Data file not found'}), 404

@app.route('/results/<filename>')
def get_result_image(filename):
    return send_from_directory(RESULT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
