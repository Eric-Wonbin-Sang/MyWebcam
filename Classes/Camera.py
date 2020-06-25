import requests
import cv2
import pygame

from General import Constants


class Camera:

    def __init__(self, name, ip_address):

        self.name = name
        self.ip_address = ip_address

        self.video_capture = cv2.VideoCapture(self.ip_address + "//video")

        self.rotation_degree = 0

        self.cascade_classifier = cv2.CascadeClassifier(Constants.cascade_classifier_xml)
        self.face_list = []

    def get_curr_frame(self, ret_type="pygame"):
        try:
            if ret_type == "pygame":
                return cv_image_to_pygame(
                    cv2.cvtColor(self.video_capture.read()[1], cv2.COLOR_BGR2RGB)
                )
            elif ret_type == "cv":
                return self.video_capture.read()[1]
            else:
                print("Camera.get_curr_frame - Unknown ret_type requested")
        except requests.exceptions.Timeout:
            return None     # camera is disconnected from the network

    def draw_to_screen(self, screen):
        screen_width, screen_height = screen.get_size()

        size_ratio = screen_width / Constants.init_screen_width
        image = pygame.transform.rotozoom(self.get_curr_frame(), self.rotation_degree, size_ratio)

        screen_center_coord = [point/2 for point in screen.get_size()]
        image_center_coord = [point/2 for point in image.get_size()]

        x = screen_center_coord[0] - image_center_coord[0] + 0
        y = screen_center_coord[1] - image_center_coord[1] + 0

        print(x, y)

        screen.blit(image, (x, y))

    def update_face_list(self):
        self.face_list = self.cascade_classifier.detectMultiScale(
            cv2.cvtColor(self.get_curr_frame("cv"), cv2.COLOR_BGR2GRAY),
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

    def draw_face_rect_list(self, screen):

        for (x, y, w, h) in self.face_list:

            red = 255
            blue = 0
            green = 0
            filled = 4

            screen_width, screen_height = screen.get_size()

            width_ratio = screen_width / Constants.init_screen_width
            height_ratio = screen_height / Constants.init_screen_height

            x, y, w, h = x * width_ratio, y * height_ratio, w * width_ratio, h * height_ratio

            # screen_center_coord = [point / 2 for point in screen.get_size()]
            # x = screen_center_coord[0] - x
            # y = screen_center_coord[1] - y

            pygame.draw.rect(screen, [red, blue, green], [x, y, w, h], filled)


def cv_image_to_pygame(image):
    return pygame.image.frombuffer(image.tostring(), image.shape[1::-1], "RGB")
