import face_recognition 
import cv2 
import numpy as np
import csv
import os
from datetime import datetime

# taking input from the webcam
# using the videocapture method from opencv and parameter is zero as we are taking value from default webcam
video_capture = cv2.VideoCapture(0)

#We have photos in a separate folder named photos where we store all the photos of the students
# Calling this folder photos inside the program and creating variables for all these values


#In this testcase we have four people and their encoding data stored with their names_encoding
# For more convienence we need to automate this by using for loop using OS package(with which we can access 100's of files)

popSmoke_image = face_recognition.load_image_file("photos/popSmoke.jpg")
popSmoke_encoding = face_recogniton.face_encodings(popSmoke_image)[0]


gunna_image = face_recognition.load_image_file("photos/gunna.jpg")
gunna_encoding = face_recogniton.face_encodings(gunna_image)[0]


sadmona_image = face_recognition.load_image_file("photos/sadmona.jpg")
sadmona_encoding = face_recogniton.face_encodings(sadmona_image)[0]


daBaby_image = face_recognition.load_image_file("photos/daBaby.jpg")
daBaby_encoding = face_recogniton.face_encodings(daBaby_image)[0]


known_face_encoding =[
    popSmoke_encoding,
    gunna_encoding,
    sadmona_encoding,
    daBaby_encoding
]


# list of facenames

known_face_names = [
    "popSmoke",
    "gunna", 
    "sadmona",
    "daBaby"
]

students = known_face_names.copy()

# We have created these four variiables. face_locations is used to store the face locations if there are any faces coming from the cam. face_locations for coordinates , _encodings fro our data, _names if the face is there in our names
face_locations = []
face_encodings = []
face_names = []
s = True


# Now capture exact date and time 
now = datetime.now()
current_date = now.strftime("%Y-%m-%d")

# Lets create a csv file and open a writer class instance. 'w+' method for write method.lnwriter is the class writer instance using which we write the data into the csv file
f = open(current_date + '.csv', 'w+', newline='')
lnwriter = csv.writer(f)

# using read data we are extracting the video data. The method return two values we are not interested in the first value so we tyake second value which is the actual video input. Then we are decreasing the size, converting into rgb format because cv2 uses bgr format and face_recognition uses rgb format
while True:
    _,frame = video_capture.read()
    small_frame = cv2.resize(frame,(0,0), fx=0.25, fy=0.25)
    rgb_small_frame = small_frame[:,:,::-1]


# Main algo
    if s:
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame,face_locations)
        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encoding,face_encoding)
            name=""
            face_distance = face_recognition.face_distance(known_face_encoding,face_encoding)
            best_match_index = np.argmin(face_distance)
            if matches[best_match_index]:
                name = known_faces_names[best_match_index]

            face_names.append(name)
            if name in known_faces_names:
                font = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (10,100)
                fontScale              = 1.5
                fontColor              = (255,0,0)
                thickness              = 3
                lineType               = 2
 
                cv2.putText(frame,name+' Present', 
                    bottomLeftCornerOfText, 
                    font, 
                    fontScale,
                    fontColor,
                    thickness,
                    lineType)
 
                if name in students:
                    students.remove(name)
                    print(students)
                    current_time = now.strftime("%H-%M-%S")
                    lnwriter.writerow([name,current_time])
    cv2.imshow("attendence system",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
 
video_capture.release()
cv2.destroyAllWindows()
f.close()