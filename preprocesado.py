import cv2
import os
import pandas as pd
dir_path = 'D:\\CIC\\LSM\\DactiolologiaLSM\\videosPersonas\\limpios\\'
image_path = 'D:\\CIC\\LSM\\DactiolologiaLSM\\images\\'
df = pd.DataFrame()
imageNames = []
targets = []
# df['ImageName'] = namesTrain
# df['Target'] = classesTrain
personNum = 3
for persona in os.listdir(dir_path):
	print(persona)
	if persona == 'persona3':
		videoPath = dir_path+persona+'\\'
		for videoName in os.listdir(videoPath):
			letter = videoName.split('_')[0]
			hand = (videoName.split('_')[1]).split('.')[0]
			# if letter != 'a':
			# 	continue
			print(videoName, letter, hand)
			capture = cv2.VideoCapture(videoPath+videoName)
			frameNr = 0
			while (True):
				success, frame = capture.read()
				if success:
					imageName = letter + str(frameNr)+'_'+hand+'_'+str(personNum)+'.jpg'
					imageNames.append(imageName)
					imageName = image_path + imageName

					targets.append(letter)
					if hand == "izq":
						if persona != 'persona3':
							cv2.imwrite(imageName, cv2.flip(frame, 1))
						else:
							cv2.imwrite(imageName, frame)

					else:
						if persona == 'persona3':
							cv2.imwrite(imageName, cv2.flip(frame, 1))
						else:
							cv2.imwrite(imageName, frame)
				else:
					break
				frameNr += 1
			capture.release()
		# break
	# personNum +=1

df['ImageName'] = imageNames
df['Target'] = targets
if os.path.exists('D:\\CIC\\LSM\\DactiolologiaLSM\\DactiolologiaDataset.csv'):
	print('Escribiendo un nuevo DactiolologiaDataset')
	df_global = pd.read_csv('D:\\CIC\\LSM\\DactiolologiaLSM\\DactiolologiaDataset.csv')
	df_global = pd.concat([df_global, df], ignore_index = True)
	df_global.reset_index()
	df_global.to_csv('D:\\CIC\\LSM\\DactiolologiaLSM\\DactiolologiaDataset.csv', index=False)
else:
	print('Escribiendo un DactiolologiaDataset de la persona', personNum)	
	df.to_csv('D:\\CIC\\LSM\\DactiolologiaLSM\\DactiolologiaDatasetPerson'+str(personNum)+'.csv', index=False)

# videoNames = ['avisame', 'bien', 'buenosDias', 'comoEstas', 'duda', 'examen', 'hola', 'mal', 'mandar', 'whatsapp']
# maxFrames = 0
# maxPersona = 0
# maxSign = ''
# for p in range(persona):
# 	# print('---Persona', p+1)
# 	for video in videoNames:
# 		# cap = cv2.VideoCapture(dire + str(p+1) + '\\' + video + ".mp4")
# 		# length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# 		# print(video, 'contiene ', length, 'frames')
# 		# if length > maxFrames:
# 		# 	maxFrames = length
# 		# 	maxPersona = p+1
# 		# 	maxSign = video
# 		print('Name: ','persona' + str(p+1) + '\\' + video + ".mp4")




# print('\n>>>Max frames=',maxFrames)
# print('>>>Persona=',maxPersona)
# print('>>>Sign=',maxSign)
