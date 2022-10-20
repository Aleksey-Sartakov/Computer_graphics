import cv2
import numpy as np


# An instance of image
class Image:
    # Get file data by file name and create 3 copies of image in R, G and B spectra
    def __init__(self, img_name: str):
        """

        :param img_name: file name in format: "name.jpg(jpeg, png, ...)"
        """
        self._name = img_name
        self._img = cv2.imread(self._name)
        self._height = self._img.shape[0]
        self._width = self._img.shape[1]
        self._b, self._g, self._r = cv2.split(self._img)

    # Create an RGB-copy with blur effect of original image
    def blur(self):
        # Задание матрицы ядра свертки
        convolution_core = np.array(([1, 1, 1], [1, 1, 1], [1, 1, 1]))

        new_merge_img = self._convolution_rgb(convolution_core)
        cv2.imwrite(f'blured_{self._name}', new_merge_img)

    # Create an RGB-copy with sharpen effect of original image
    def sharpen(self):
        convolution_core = np.array(([-1, -1, -1], [-1, 9, -1], [-1, -1, -1]))

        new_merge_img = self._convolution_rgb(convolution_core)
        cv2.imwrite(f'sharpened_{self._name}', new_merge_img)

    # Create an RGB-copy with edge_detection effect of original image
    def edge_detection(self):
        convolution_core = np.array(([0, 4, 0], [4, -16, 4], [0, 4, 0]))

        new_merge_img = self._convolution_rgb(convolution_core)
        cv2.imwrite(f'edge_detected_{self._name}', new_merge_img)

    # Create an RGB-copy with sobel_y_edge_detection effect of original image
    def sobel_edge_detection_y(self):
        convolution_core = np.array(([-1, 0, 1], [-2, 0, 2], [-1, 0, 1]))

        new_merge_img = self._convolution_rgb(convolution_core)
        cv2.imwrite(f'sobel_edge_detected_y_{self._name}', new_merge_img)

    def negative(self):
        convolution_core = np.array(([0, 0, 0], [0, -1, 0], [0, 0, 0]))

        new_merge_img = self._convolution_rgb(convolution_core, 255)
        cv2.imwrite(f'negative_{self._name}', new_merge_img)

    def emboss(self):
        convolution_core = np.array(([-2, -1, 0], [-1, 0, 1], [0, 1, 2]))

        new_merge_img = self._convolution_rgb(convolution_core, 128)
        cv2.imwrite(f'emboss_{self._name}', new_merge_img)

    # Performs a convolution according to the core of AHSL-image
    def _convolution_ahsl(self, core: np.ndarray, img: np.ndarray, new_img: np.ndarray, offset: int):
        """

        :param core: convolution matrix
        :param img: image pixel matrix in AHSL
        :param new_img: image pixel matrix in AHSL, which will be generated according to the core and the original image
        """
        core_sum = core.sum()
        for y in range(1, self._height - 2):
            for x in range(1, self._width - 2):
                data = (core[0, 0] * img[y - 1, x - 1] + core[0, 1] * img[y - 1, x] + core[0, 2] * img[y - 1, x + 1] +
                        core[1, 0] * img[    y, x - 1] + core[1, 1] * img[    y, x] + core[1, 2] * img[    y, x + 1] +
                        core[2, 0] * img[y + 1, x - 1] + core[2, 1] * img[y + 1, x] + core[2, 2] * img[y + 1, x + 1] +
                        offset)
                if data < 0:
                    new_img[y - 1, x - 1] = 0
                else:
                    new_img[y - 1, x - 1] = data / core_sum if core_sum > 0 else data

    # Performs a convolution according to the core of RGB-image
    def _convolution_rgb(self, core: np.ndarray, offset=0) -> np.ndarray:
        """

        :param core: matrix for convolution
        :return: processed RGB-image
        """
        # Длина и ширина нового изображения меньше исходного на 2, потому что первый ряд
        # и первый столбец, последний ряд и последний столбец не могут быть свернуты
        new_img_r = np.zeros((self._height - 2, self._width - 2))
        new_img_g = np.zeros((self._height - 2, self._width - 2))
        new_img_b = np.zeros((self._height - 2, self._width - 2))

        # Осуществление свертки для каждого спектра
        self._convolution_ahsl(core, self._r, new_img_r, offset)
        self._convolution_ahsl(core, self._g, new_img_g, offset)
        self._convolution_ahsl(core, self._b, new_img_b, offset)

        return cv2.merge([new_img_b, new_img_g, new_img_r])


if __name__ == "__main__":
    my_image = Image("Notre-Dame_Guillotine.jpg")
    my_image.sobel_edge_detection_y()
