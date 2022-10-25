import numpy as np
import os
import sys
# sys.path.append(os.path.join(os.path.abspath(os.path.dirname(os.path.realpath(__file__))), "../"))

import tensorflow as tf
import cv2
from Hand import Hand
class HandsDetector():
    def __init__(self):
        self.__hands=[]
        # Path del modelo pre entrenado
        self.__PATH_SAVED_MODEL = os.path.abspath(os.path.dirname(os.path.realpath(__file__))) + '/saved_model'

        model = tf.saved_model.load(self.__PATH_SAVED_MODEL)
        self.__model = model.signatures['serving_default']


    def handDetection(self, image, boundingboxes=False):
        self.__hands=[]
        width=image.shape[1]
        height=image.shape[0]
        input_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) # Mejora la deteccion
        # input_image = input_image/255.0
        # input_image = (2.0 / 255.0) * np.float32(input_image) - 1.0 # Aplica brillo

        # The input needs to be a tensor, convert it using `tf.convert_to_tensor`.
        input_tensor = tf.convert_to_tensor(input_image)
        # The model expects a batch of images, so add an axis with `tf.newaxis`.
        input_tensor = input_tensor[tf.newaxis,...]

        # Run inference
        output_dict = self.__model(input_tensor)

        output_dict['detection_scores'] = output_dict['detection_scores'][0]
        output_dict['detection_boxes'] = output_dict['detection_boxes'][0]

        count=0#Contador de numero de rostros
        border=(0,0,0,0)
        rostros=[]
        for score in output_dict['detection_scores']:
            """
            Cuando score>= 0.6 se considera como cara
            """
            if score >= 0.4:
                """
                border: lista con coordenadas del rostro en formato (yMin, xMin, yMax, xmax)
                """

                border = (int(output_dict['detection_boxes'][count][0]*height), int(output_dict['detection_boxes'][count][1]*width),
                int(output_dict['detection_boxes'][count][2]*height), int(output_dict['detection_boxes'][count][3]*width)) # yMin,xMin,yMax,xmax
                #Creacion de objeto Rostro
                hand=Hand()
                hand.setCoordenadas(border)
                hand.setAncho(border[3] - border[1])
                hand.setAlto(border[2] - border[0])
                hand.setMinY(border[0])
                hand.setMinX(border[1])
                hand.setMaxY(border[2])
                hand.setMaxX(border[3])


                border=list(border)
                #rostro.setImg(np.asarray(originalImage.crop(border)))
                # hand.setImg(image[border[1]:border[3], border[0]:border[2]])
                aux=image[border[0]:border[2],border[1]:border[3],:]
                aux = np.float32(aux) / 255.0
                hand.setImg(aux)
                self.__hands.append(hand)
                # hand.setImg(image[border[0]:border[2],border[1]:border[3],:])

                """
                Dado a que se nesecita un formato selfie en la red EG y big5 se agrega a la imagen:
                10% en yMin(Top)
                10% en xMin(Left)
                10% en xMax(Rigth)
                40% en yMax(Bottom)
                sidesMargins: tamanio que se agrega a los lados del rostro (10% del ancho del rostro).
                topMargin: tamanio que se agrega arriba del rostro (10% del alto del rostro).
                bottomMargin: tamanio que se agrega abajo del rostro (40% del alto del rostro).
                Las coordenadas se quedan tal cual para ocuparlos en el modulo de AR.
                """
                # sidesMargins = rostro.getAncho()*0.1
                # topMargin = rostro.getAlto()*0.1
                # bottomMargin = rostro.getAlto()*0.4
                #
                # #Para yMin (boder[0]) para formato selfie
                # border[0] = int(border[0]-topMargin) if (border[0]-topMargin)>0 else 0
                #
                # #Para xMin (boder[1]) para formato selfie
                # border[1] = int(border[1]-sidesMargins) if (border[1]-sidesMargins)>0 else 0
                #
                # #Para yMax (boder[2]) para formato selfie
                # border[2] = int(border[2]+bottomMargin) if (border[2]+bottomMargin)<height else height
                #
                # #Para xMax (boder[3]) para formato selfie
                # border[3] = int(border[3]+sidesMargins) if (border[3]+sidesMargins)<width else width
                #
                # #Tamanios de la selfie
                # selfieHeight = border[2]-border[0]
                # selfieWidth = border[3]-border[1]
                #
                # imageP=image[border[0]:border[2],border[1]:border[3],:]

                """
                Redimension de 208x208
                aux: imagen totalmente en negro
                margin: posicion de los margenes
                Primero se redimenciona proporcinalemente la imagen en formato
                selfie para que el lado mas grande tenga un valor de 208 y el otro
                lado se mantenga proporcinalmente. Despues se suma la imagen en
                formato selfie reescalada sobre la imagen en negro (aux) respetando los margenes.
                """
                #Redimensiona 208x208


                # aux=np.zeros((208, 208, 3), dtype=int)
                #
                # if selfieHeight>selfieWidth:
                #     newWidth = int(selfieWidth * 208 / selfieHeight)
                #
                #     #Resize (208,newWidth)
                #     #Formato de cv2.resize (width, height)
                #     selfieImage = cv2.resize(imageP, (newWidth, 208))
                #     margin = int((208-newWidth)/2)
                #     aux[:, margin:margin+newWidth, :] = selfieImage[:,:,:]
                #     #aux=cv2.cvtColor(aux, cv2.COLOR_BGR2RGB)
                #     #aux[margin:margin+newWidth, :, :]=selfieImage[:,:,:]
                #
                # else:
                #     newHeight = int(selfieHeight *208 / selfieWidth)
                #     #Resize (newHeight,208)
                #     selfieImage = cv2.resize(imageP, (208,newHeight))
                #     margin = int((208-newHeight)/2)
                #     aux[margin:margin+newHeight, :, :]=selfieImage[:,:,:]
                    #aux[:, margin:margin+newHeight, :] = selfieImage[:,:,:]

                # Normalizar
                # aux = np.float32(aux) / 255.0
                # rostro.setImg(aux)
                #
                # self.__hands.append(rostro)
                # count+=1
                #print('Rostro detectado')
            else:
                #print('Total de rostros {}'.format(count))
                # hand=Hand()
                print("Hand didn't detect")
                break

        return self.__hands
