from ultralytics import YOLO
obb = YOLO('AI_Model/obb.pt').cuda()
pose = YOLO('AI_Model/pose.pt').cuda()

obb.to(device=0)
pose.to(device=0)