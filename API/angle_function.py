import math

def line_angle(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    return math.atan2(dy, dx)

def CenterAndAngle(obb_points,pose_points):
  dec = []

  for obb_point in obb_points:

    # Find Top Mid point
    xmidtop = int((obb_point[0][0] + obb_point[1][0]) / 2)
    ymidtop = int((obb_point[0][1] + obb_point[1][1]) / 2)

    # Find Bottom Mid point
    xmidbot = int((obb_point[2][0] + obb_point[3][0]) / 2)
    ymidbot = int((obb_point[2][1] + obb_point[3][1]) / 2)

    # Find Center point
    xmidmid = int((xmidtop + xmidbot) / 2)
    ymidmid = int((ymidtop + ymidbot) / 2)

    closest_point = {}
    for pose_point in pose_points:
      X = int (abs(pose_point[0][0]-xmidmid))
      Y = int (abs(pose_point[0][1]-ymidmid))
      D = X+Y
      closest_point.update({D:pose_point})

    min_D = min(closest_point.keys())
    pose_point = closest_point[min_D]

    # Calculate ManHattan Distance From POSE Head
    p1 = int (abs(pose_point[0][0]-obb_point[0][0]))
    q1 = int (abs(pose_point[0][1]-obb_point[0][1]))
    p2 = int (abs(pose_point[0][0]-obb_point[3][0]))
    q2 = int (abs(pose_point[0][1]-obb_point[3][1]))
    d1 = p1+q1
    d2 = p2+q2

    if d1<d2:
      cx = xmidtop
      cy = ymidtop

    else:
      cx = xmidbot
      cy = ymidbot

    angle_redious = line_angle(xmidmid, ymidmid, cx, cy)

    angle = -1*(math.degrees(angle_redious))

    if angle<0:
      angle = 360+angle
    
    dec.append({"Center": {"X": xmidmid,"Y": ymidmid},"Angle": "{:.2f}".format(angle)})
    
  return dec