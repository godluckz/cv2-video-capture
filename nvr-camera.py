import cv2, time
from urllib.parse import quote_plus
from os import environ
import uuid

def main() -> None:

    w_username = environ.get("CAMERA_USERNAME")
    w_password = environ.get("CAMERA_PASSWORD")

    if not w_username or not w_password:
        print("Username or Password is missing")
        return
    

    w_user_camera_ip = input("Camera IP to view: ") #Get user input
    
    w_port = 554    
    if w_user_camera_ip:
        w_cam_ip = w_user_camera_ip
    else:
        w_cam_ip = environ.get("CAMERA_IP")

    if not w_cam_ip: 
        print("Camera IP is missing.")

    w_password_encoded = quote_plus(w_password)

    w_camera_url = f"rtsp://{w_username}:{w_password_encoded}@{w_cam_ip}:{w_port}/Streaming/Channels/101" #Done for hikvision NVR, if not working for you, change to adapt to your camera

    video_stream = cv2.VideoCapture(w_camera_url,cv2.CAP_FFMPEG)

    w_timeout = time.time() + 10

    if not video_stream.isOpened():
        print("fail to open camera.")
    else:
        print("camera is open")
        w_count: int = 0
        while time.time() < w_timeout:
            ret, frame = video_stream.read()
            
            cv2.imshow("Camera feed",frame)
                        
            if cv2.waitKey(1) & 0xFF == ord('s'):# Check for 's' key press to take a screenshot
                w_count += 1
                w_filename = uuid.uuid5(namespace=uuid.NAMESPACE_OID, name=f"screenshot{w_count}")
                w_filename = f"screenshots/nvr/{w_filename}-screenshot{w_count}.jpg"
                cv2.imwrite(w_filename, frame)
                print(f"Screenshot taken and saved as '{w_filename}'")
            
            if cv2.waitKey(1) & 0xFF == ord('q'):# Exit on 'q' key press
                print("Exit")
                break

    video_stream.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()