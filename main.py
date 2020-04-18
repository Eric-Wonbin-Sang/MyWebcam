import Camera
import pygame

from General import Constants


def main():

    width = Constants.init_screen_width
    height = Constants.init_screen_height

    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    camera = Camera.Camera(name="Camera 1", ip_address="http://192.168.1.10:8080")

    face_counter = 0
    facial_recognition_toggle = False
    rotate_effect_toggle = False
    running = True

    while running:

        screen.fill((0, 0, 0))
        camera.draw_to_screen(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.VIDEORESIZE:
                width_ratio = 16
                height_ratio = 9
                if width != event.w:
                    width = event.w
                    height = int(event.w * height_ratio / width_ratio)
                else:
                    height = event.h
                    width = int(event.h * width_ratio / height_ratio)
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    facial_recognition_toggle = not facial_recognition_toggle
                if event.key == pygame.K_r:
                    rotate_effect_toggle = not rotate_effect_toggle
                    if not rotate_effect_toggle:
                        camera.rotation_degree = 0

        if facial_recognition_toggle:
            if face_counter > 8:
                camera.update_face_list()
                face_counter = 0
            camera.draw_face_rect_list(screen)
            face_counter += 1

        if rotate_effect_toggle:
            camera.rotation_degree += 3

        pygame.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
