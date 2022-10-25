import cv2
import mediapipe as mp



def get_bbox_coordinates(handLadmark, image_shape):
    """
    Get bounding box coordinates for a hand landmark.
    Args:
        handLadmark: A HandLandmark object.
        image_shape: A tuple of the form (height, width).
    Returns:
        A tuple of the form (xmin, ymin, xmax, ymax).
    """
    all_x, all_y = [], [] # store all x and y points in list
    offset = 35
    for hnd in mp_hands.HandLandmark:
        all_x.append(int(handLadmark.landmark[hnd].x * image_shape[1])) # multiply x by image width
        all_y.append(int(handLadmark.landmark[hnd].y * image_shape[0])) # multiply y by image height

    return max(min(all_x)-offset,0), max(min(all_y)-offset, 0), min(max(all_x)+offset, image_shape[1]), min(max(all_y)+offset, image_shape[0]) # return as (xmin, ymin, xmax, ymax)



mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
mp_drawing_styles = mp.solutions.drawing_styles
# For static images:
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.5)

cap = cv2.VideoCapture(0)
while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    # Draw the hand annotations on the image.
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            bbox = get_bbox_coordinates(hand_landmarks, image.shape)
        cv2.rectangle(image,(bbox[0],bbox[1]),(bbox[2],bbox[3]),(0,255,0),2)

        # mp_drawing.draw_landmarks(
        #     image,
        #     hand_landmarks,
        #     mp_hands.HAND_CONNECTIONS,
        #     mp_drawing_styles.get_default_hand_landmarks_style(),
        #     mp_drawing_styles.get_default_hand_connections_style())

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
    if cv2.waitKey(25) & 0xFF == ord('q'):
      break

cap.release()
cv2.destroyAllWindows()
