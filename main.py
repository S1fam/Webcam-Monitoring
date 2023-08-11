import glob
import cv2
import time
from emailing import send_email
from clean import delete_content
from threading import Thread


video = cv2.VideoCapture(0)  # 0 - use main camera, 1 - secondary camera
time.sleep(1)

first_frame = None  # to be able to save first frame, we will compare it to the next ones
status_list = []
count = 1

while True:
    status = 0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # we convert frame to grayscale
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)  # gray frame gets blurred
    # cv2.imshow("My video", gray_frame_gau)

    if first_frame is None:  # after saving first one will no longer be None
        first_frame = gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    # if value is more than 30 we asign 255
    thresh_frame = cv2.threshold(delta_frame, 115, 255, cv2.THRESH_BINARY)[1]
    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("My video", dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        x, y, w, h = cv2.boundingRect(contour)
        # x+w will give us the other x, y+h the other y
        rect = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0))  # green rectangle

        if rect.any():
            status = 1
            cv2.imwrite(f"images/image{count}.png", frame)
            count = count + 1
            all_images = glob.glob("images/*.png")
            index = int(len(all_images) / 2)
            image_with_object = all_images[index]
            time.sleep(0.25)

    status_list.append(status)
    status_list = status_list[-2:]

    if status_list[0] == 1 and status_list[1] == 0:  # when object exits
        email_thread = Thread(target=send_email, args=(image_with_object, ))
        email_thread.daemon = True
        clean_thread = Thread(target=delete_content, args=(f"images", ))
        clean_thread.daemon = True

        email_thread.start()
        time.sleep(1)
        clean_thread.start()
        count = 1

    cv2.imshow("Video", frame)
    key = cv2.waitKey(1)

    if key == ord("q"):
        break

video.release()
