import cv2
import numpy as np
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QThread, pyqtSignal

# worker thread (QThread) for camera
class CameraWorkerThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.set_minimum_size(640, 480)
        self.brightness = 50
        self.contrast = 50
        self.exposure = 50
        self.zoom = 15  # Default 1.0x
        self.auto_awb = True
        self.grayscale = False
        self.ThreadActive = False

    def run(self):
        self.ThreadActive = True
        cap = cv2.VideoCapture(0) # camera source

        if not cap.isOpened():
            print("Cannot open camera")
            self.ThreadActive = False
            return

        actual_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        print(f"Camera resolution: {actual_width}x{actual_height}")

        while self.ThreadActive:
            ret, frame = cap.read()
            if not ret:
                break

            # brightness and contrast adjustments
            brightness_factor = (self.brightness - 50) * 2
            contrast_factor = (self.contrast - 50) / 50.0
            bright_frame = cv2.convertScaleAbs(frame, alpha=1 + contrast_factor, beta=brightness_factor)

            exposure_factor = (self.exposure - 50) / 50.0
            adjusted_image = cv2.convertScaleAbs(bright_frame, alpha=1.0, beta=exposure_factor * 50)

            frame = cv2.flip(adjusted_image, 1)

            display_width = getattr(self, 'display_width', actual_width)  # Set your actual display width
            display_height = getattr(self, 'display_height', actual_height)  # Set your actual display height

            h, w = frame.shape[:2]

            # scaling factor
            scale_w = display_width / w
            scale_h = display_height / h
            scale_factor = min(scale_w, scale_h)

            new_width = int(w * scale_factor)
            new_height = int(h * scale_factor)

            # resize
            fitted_image = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_LINEAR)

            # display canvas dimensions
            canvas = np.zeros((display_height, display_width, 3), dtype=np.uint8)

            # camera frame position
            start_x = (display_width - new_width) // 2
            start_y = (display_height - new_height) // 2

            canvas[start_y:start_y + new_height, start_x:start_x + new_width] = fitted_image

            # Use the fitted image for further processing
            zoomed_image = canvas

            # Auto White Balance
            if getattr(self, 'auto_awb', False):
                # Use center region for more accurate AWB
                h_awb, w_awb = zoomed_image.shape[:2]
                center_region = zoomed_image[h_awb // 4:3 * h_awb // 4, w_awb // 4:3 * w_awb // 4]

                b, g, r = cv2.split(center_region)
                avg_b = cv2.mean(b)[0]
                avg_g = cv2.mean(g)[0]
                avg_r = cv2.mean(r)[0]

                # Calculate scaling factors
                avg_gray = (avg_b + avg_g + avg_r) / 3

                if avg_b > 0 and avg_g > 0 and avg_r > 0:
                    scale_b = avg_gray / avg_b
                    scale_g = avg_gray / avg_g
                    scale_r = avg_gray / avg_r

                    # Apply AWB to entire image
                    b_full, g_full, r_full = cv2.split(zoomed_image)
                    b_full = cv2.convertScaleAbs(b_full, alpha=scale_b)
                    g_full = cv2.convertScaleAbs(g_full, alpha=scale_g)
                    r_full = cv2.convertScaleAbs(r_full, alpha=scale_r)

                    awb_image = cv2.merge([b_full, g_full, r_full])
                else:
                    awb_image = zoomed_image
            else:
                awb_image = zoomed_image

            # Apply grayscale if enabled
            if getattr(self, 'grayscale', False):
                awb_image = cv2.cvtColor(awb_image, cv2.COLOR_BGR2GRAY)
                awb_image = cv2.cvtColor(awb_image, cv2.COLOR_GRAY2BGR)

            # Convert BGR to RGB for Qt display
            color_swapped_image = cv2.cvtColor(awb_image, cv2.COLOR_BGR2RGB)

            # Create Qt image
            qt_image = QImage(color_swapped_image.data,
                              color_swapped_image.shape[1],
                              color_swapped_image.shape[0],
                              color_swapped_image.strides[0],
                              QImage.Format_RGB888)

            # Emit the signal to update the display
            self.change_pixmap_signal.emit(qt_image)

        # Clean up
        cap.release()

    def stop(self):
        self.ThreadActive = False

    def set_brightness(self, value):
        self.brightness = value

    def set_contrast(self, value):
        self.contrast = value

    def set_exposure(self, value):
        self.exposure = value

    def set_zoom(self, value):
        self.zoom = value

    def set_auto_awb(self, enabled: bool):
        self.auto_awb = enabled

    def set_grayscale(self, enabled: bool):
        self.grayscale = enabled

    def set_minimum_size(self, param, param1):
        pass
