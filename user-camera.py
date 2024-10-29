import cv2, time
import uuid

def main() -> None:    

    video_stream = cv2.VideoCapture(0) #Open user camera

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
                w_filename = f"screenshots/device/{w_filename}-screenshot{w_count}.jpg"
                cv2.imwrite(w_filename, frame)
                print(f"Screenshot taken and saved as '{w_filename}'")
                
            if cv2.waitKey(1) & 0xFF == ord('q'):# Exit on 'q' key press
                print("Exit")
                break

    video_stream.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    main()