import os
import cv2
import time
import uuid

IMAGE_PATH = "CollectedImages"

labels = ['Hello', 'Yes', 'No', 'Thanks', 'ILoveYou', 'Please']

number_of_image = 5

for label in labels:
    img_path = os.path.join(IMAGE_PATH, label)
    os.makedirs(img_path, exist_ok=True)

    # Open camera
    cap = cv2.VideoCapture(0)

    print(f"Collecting images from {label}")
    time.sleep(3)

    for imgnum in range(number_of_image):
        ret, frame = cap.read()
        imagename = os.path.join(
                IMAGE_PATH,
                label,
                label + '.' + '{}.jpg'.format(str(uuid.uuid1()))
            )

        cv2.imwrite(imagename, frame)
        cv2.imshow('frame', frame)
        time.sleep(2)

        if cv2.waitKey(1) & 0xFF==ord('q'):
            break


    cap.release()