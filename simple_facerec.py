import face_recognition
import cv2
import os
import glob
import numpy as np

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        # Yüksek hız için çerçeve boyutlandırılması yapılmaktadır.
        self.frame_resizing = 0.5

    def load_encoding_images(self, images_path):

        # Resimler Yüklenir.
        images_path = glob.glob(os.path.join(images_path, "*.*"))

        print("{} encoding images found.".format(len(images_path)))

        # Resimleri isimleriyle birlikte kaydedilir.
        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Dosya yolu ilk dosyadan alınır.
            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            # Encoding işlemi yapılır.
            img_encoding = face_recognition.face_encodings(rgb_img)[0]

            # Dosya adı ve dosya ile kaydedilir.
            self.known_face_encodings.append(img_encoding)
            self.known_face_names.append(filename)
        print("Encoding images loaded")

    def detect_known_faces(self, frame):
        
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)

        # Opencv için renklerin rgb ayrıştırması için dönüştür.
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:

            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = ""

            if any(matches):
                face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = self.known_face_names[best_match_index]
            if name:
                face_names.append(name)

        # numpy dizisine dönüştür.
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names
