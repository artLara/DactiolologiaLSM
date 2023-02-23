import cv2
import mediapipe as mp
import numpy as np
from Hand import Hand
class HandsDetector():
    def __init__(self):
        self.__hands=[]
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_hands = mp.solutions.hands
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.handsize = 200
        self.x = None
        self.y = None
        self.bbox = None
        self.landmarks = None
        # For static images:
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5)

    def getLandmarks(self):
        return self.x + self.y

    def get_coord_lists(self, handLadmark, image_shape):
        all_x, all_y = [], [] # store all x and y points in list
        for hnd in self.mp_hands.HandLandmark:
            all_x.append(handLadmark.landmark[hnd].x * image_shape[1])
            all_y.append(handLadmark.landmark[hnd].y * image_shape[0])

        return all_x, all_y

    def getLandmarksNorm(self):
        """
        Mueve X y Y respecto al bounding box, despues lo normaliza respecto al ancho
        y largo del bounding box
        """
        x = []
        y = []
        for i in range(len(self.x)):
            aux = (self.x[i] - self.bbox[0])/(self.bbox[2]-self.bbox[0])
            x.append(aux)
            aux = (self.y[i] - self.bbox[1])/(self.bbox[3]-self.bbox[1])
            y.append(aux)

        return np.asarray([x+y])

    def get_bbox_coordinates(self, handLadmark, image_shape):
        """
        Get bounding box coordinates for a hand landmark.
        Args:
            handLadmark: A HandLandmark object.
            image_shape: A tuple of the form (height, width).
        Returns:
            A tuple of the form (xmin, ymin, xmax, ymax).
        """
        all_x, all_y = [], [] # store all x and y points in list
        offset = 50
        for hnd in self.mp_hands.HandLandmark:
            all_x.append(int(handLadmark.landmark[hnd].x * image_shape[1])) # multiply x by image width
            all_y.append(int(handLadmark.landmark[hnd].y * image_shape[0])) # multiply y by image height

        return max(min(all_x)-offset,0), max(min(all_y)-offset-15, 0), min(max(all_x)+offset, image_shape[1]), min(max(all_y)+offset+15, image_shape[0]) # return as (xmin, ymin, xmax, ymax)

    def handDetection(self, image, boundingboxes=False):
        self.__hands=[]
        hand=Hand()
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        results = self.hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        b = False
        if results.multi_hand_landmarks:
            bbox=(0,0,0,0)
            for hand_landmarks in results.multi_hand_landmarks:
                # print(hand_landmarks)
                bbox = self.get_bbox_coordinates(hand_landmarks, image.shape)
                self.bbox = self.get_bbox_coordinates(hand_landmarks, image.shape)
                self.x, self.y = self.get_coord_lists(hand_landmarks, image.shape)
                self.mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS,
                    self.mp_drawing_styles.get_default_hand_landmarks_style(),
                    self.mp_drawing_styles.get_default_hand_connections_style())
            # for world in results.multi_hand_world_landmarks:
                # print(world)

            # cv2.rectangle(image,(bbox[0],bbox[1]),(bbox[2],bbox[3]),(0,255,0),2)
            hand.setCoordenadas(bbox)
            hand.setAncho(bbox[2] - bbox[0])
            hand.setAlto(bbox[3] - bbox[1])
            hand.setMinX(bbox[0])
            hand.setMinY(bbox[1])
            hand.setMaxX(bbox[2])
            hand.setMaxY(bbox[3])
            hand.setLandMarks(self.getLandmarksNorm())
            hand.setLandMarksRaw(np.asarray([self.x+self.y]))
            # bbox=list(bbox)
            # aux=np.zeros((self.handsize, self.handsize), dtype=int)
            # handImage=image_gray[bbox[1]:bbox[3], bbox[0]:bbox[2]]
            # selfieWidth = bbox[2] - bbox[0]
            # selfieHeight = bbox[3] - bbox[1]
            # if selfieHeight>selfieWidth:
            #     newWidth = int(selfieWidth * self.handsize / selfieHeight)
            #
            #     #Resize (208,newWidth)
            #     #Formato de cv2.resize (width, height)
            #     handImage = cv2.resize(handImage, (newWidth, self.handsize))
            #     margin = int((self.handsize-newWidth)/2)
            #     aux[:, margin:margin+newWidth] = handImage[:,:]
            #     #aux=cv2.cvtColor(aux, cv2.COLOR_BGR2RGB)
            #     #aux[margin:margin+newWidth, :, :]=selfieImage[:,:,:]
            #
            # else:
            #     newHeight = int(selfieHeight *self.handsize / selfieWidth)
            #     #Resize (newHeight,208)
            #     handImage = cv2.resize(handImage, (self.handsize,newHeight))
            #     margin = int((self.handsize-newHeight)/2)
            #     aux[margin:margin+newHeight, :]=handImage[:,:]
            # aux = np.float32(aux) / 255.0
            # # hand.setImg(aux)
            # l = []
            # l.append(aux)
            # l=np.asarray(l)
            # hand.setImg(l)
            b = True
            # for hand_landmarks in results.multi_hand_landmarks:
            #     self.bbox = self.get_bbox_coordinates(hand_landmarks, image.shape)
            #     self.x, self.y = self.get_coord_lists(hand_landmarks, image.shape)
            #     self.mp_drawing.draw_landmarks(
            #         image,
            #         hand_landmarks,
            #         self.mp_hands.HAND_CONNECTIONS,
            #         self.mp_drawing_styles.get_default_hand_landmarks_style(),
            #         self.mp_drawing_styles.get_default_hand_connections_style())

            # print(l.shape)

            # self.__hands.append(hand)
        else:
            print('Mano no detectada')


        return hand, b, image
