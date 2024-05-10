import cv2

def main():
    # Open the default camera (index 0)
    cap = cv2.VideoCapture(1)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Check if the frame is captured successfully
        if not ret:
            print("Error: Could not capture frame.")
            break

        # Display the frame
        cv2.imshow('Camera Feed', frame)

        # Check for key press, wait for 1 millisecond
        key = cv2.waitKey(1)

        # If 'q' is pressed, exit the loop
        if key == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
