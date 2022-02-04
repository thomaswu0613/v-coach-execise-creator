import mediapipe as mp
import cv2
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

def detect_pose_with_draw(frame):
    with mp_pose.Pose(
        model_complexity=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5) as pose:
        frame.flags.writeable = False
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame)
        frame.flags.writeable = True
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        mp_drawing.draw_landmarks(
            frame,
            results.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    return frame, results

class BodyLandMarks():
    def __init__(self,results,mp_pose):
        if not results:
            return
        self.results = results
        self.lm = self.results.pose_landmarks.landmark
        self.mp_pose = mp_pose
    def nose(self):
        a = [self.lm[self.mp_pose.PoseLandmark.NOSE.value].x, self.lm[self.mp_pose.PoseLandmark.NOSE.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_eye_inner(self):
        a = [self.lm[self.mp_pose.PoseLandmark.LEFT_EYE_INNER.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_EYE_INNER.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_eye(self):
        a = [self.lm[self.mp_pose.PoseLandmark.LEFT_EYE.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_EYE.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_eye_outer(self):
        a = [self.lm[self.mp_pose.PoseLandmark.LEFT_EYE_OUTER.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_EYE_OUTER.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_eye_inner(self):
        a = [self.lm[self.mp_pose.PoseLandmark.RIGHT_EYE_INNER.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_EYE_INNER.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_eye(self):
        a = [self.lm[self.mp_pose.PoseLandmark.RIGHT_EYE.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_EYE.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_eye_outer(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_EYE_INNER.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_EYE_OUTER.value].y]
        if all(i <= 1 for i in a): return a
        else: return
    def left_eye_inner(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_EYE_INNER.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_EYE_INNER.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_ear(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_EAR.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_EAR.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_ear(self):
        a = [self.lm[self.mp_pose.PoseLandmark.RIGHT_EAR.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_EAR.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_mouth(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.MOUTH_LEFT.value].x, self.lm[self.mp_pose.PoseLandmark.MOUTH_LEFT.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_mouth(self):
        a = [self.lm[self.mp_pose.PoseLandmark.MOUTH_RIGHT.value].x, self.lm[self.mp_pose.PoseLandmark.MOUTH_RIGHT.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_shoulder(self):
        a = [self.lm[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        if all(i <= 1 for i in a): return a
        else: return
    def right_shoulder(self):
        a = [self.lm[self.mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
        if all(i <= 1 for i in a): return a
        else: return
    def left_elbow(self):
        a = [self.lm[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_elbow(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_wrist(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_WRIST.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_WRIST.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_wrist(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_PINKY(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_PINKY.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_PINKY.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_PINKY(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_PINKY.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_PINKY.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_index(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_INDEX.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_INDEX.value].y]
        if all(i <= 1 for i in a): return a
    def right_index(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_INDEX.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_INDEX.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_thumb(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_THUMB.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_THUMB.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_thumb(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_THUMB.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_THUMB.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_hip(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_HIP.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_HIP.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_hip(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_HIP.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_HIP.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_knee(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_KNEE.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_KNEE.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_knee(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_KNEE.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_ankle(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_ankle(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_ANKLE.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_heel(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_HEEL.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_HEEL.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_heel(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_HEEL.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_HEEL.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def left_foot_index(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].x, self.lm[self.mp_pose.PoseLandmark.LEFT_FOOT_INDEX.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def right_foot_index(self):
        a =  [self.lm[self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x, self.lm[self.mp_pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y]
        if all(i <= 1 for i in a): return a
        else: return None
    def return_all_points(self):
        return [
            self.nose(),
            self.left_eye_inner(),
            self.left_eye(),
            self.left_eye_outer(),
            self.right_eye_inner(),
            self.right_eye(),
            self.right_eye_outer(),
            self.left_ear(),
            self.right_ear(),
            self.left_mouth(),
            self.right_mouth(),
            self.left_shoulder(),
            self.right_shoulder(),
            self.left_elbow(),
            self.right_elbow(),
            self.left_wrist(),
            self.right_wrist(),
            self.left_PINKY(),
            self.right_PINKY(),
            self.left_index(),
            self.right_index(),
            self.left_thumb(),
            self.right_thumb(),
            self.left_hip(),
            self.right_hip(),
            self.left_knee(),
            self.right_knee(),
            self.left_ankle(),
            self.right_ankle(),
            self.left_heel(),
            self.right_heel(),
            self.left_foot_index(),
            self.right_foot_index()
        ]