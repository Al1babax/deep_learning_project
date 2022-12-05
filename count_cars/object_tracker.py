import torch

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')  # or yolov5n - yolov5x6, custom

# Images
img = 'https://ultralytics.com/images/zidane.jpg'  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(img)

# Results
# results.print()  # or .show(), .save(), .crop(), .pandas(), etc.

results = results.pandas().xyxy[0]  # img1 predictions (pandas)

# Results
for i in range(len(results)):
    print(results.iloc[i].values)
