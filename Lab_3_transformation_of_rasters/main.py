import cv2
import numpy as np
import tkinter
import math
from tkinter import font
from tkinter.filedialog import askopenfilename


class Image:
    # Получение информации о файле по указанному пути
    def __init__(self, path_to_image: str):
        """
        :param path_to_image: full path to file
        """
        self._name = path_to_image.split("/")[-1]
        self._img = cv2.imdecode(np.fromfile(path_to_image, dtype=np.uint8), cv2.IMREAD_COLOR)
        self._height = self._img.shape[0]
        self._width = self._img.shape[1]
        self._points = []

    # Билинейная фильтрация
    def bilinear_filtering(self) -> np.ndarray:
        """
        :return: новое преобразованное изображение
        """
        # Проверка количества указанных пользователем точек
        if len(self._points) < 6:
            return self._img

        trans_mat = self._create_transformation_matrix()

        new_img = np.zeros(self._img.shape, np.uint8)

        # Вычисление обратной матрицы
        inverse_trans_mat = np.linalg.inv(trans_mat[:, :2])
        # Вычисление нового значение для каждого пикселя создаваемого изображения
        for i in range(self._height):
            for j in range(self._width):
                x, y = inverse_trans_mat.dot(np.array([[i], [j]]) - trans_mat[:, 2:])

                x, y = x[0], y[0]

                if 0 <= x < self._height and 0 <= y < self._width:
                    # Проверка невыхода округленных вверх значений координат за границы изображения
                    ceil_x = math.ceil(x) if math.ceil(x) < self._height else math.floor(x)
                    ceil_y = math.ceil(y) if math.ceil(y) < self._width else math.floor(y)

                    color1 = np.array(self._img[math.floor(x), math.floor(y)])
                    color2 = np.array(self._img[ceil_x, math.floor(y)])
                    color3 = np.array(self._img[math.floor(x), ceil_y])
                    color4 = np.array(self._img[ceil_x, ceil_y])

                    new_img[i, j] = (((ceil_x - x) * color1 + (x - math.floor(x)) * color2) * (ceil_y - y) +
                                     ((ceil_x - x) * color3 + (x - math.floor(x)) * color4) * (y - math.floor(y)))

        return new_img

    # Простейший алгоритм трансформации
    def simple_transform(self) -> np.ndarray:
        """
        :return: новое преобразованное изображение
        """
        # Проверка количества указанных пользователем точек
        if len(self._points) < 6:
            return self._img

        trans_mat = self._create_transformation_matrix()

        new_img = np.zeros(self._img.shape, np.uint8)

        # Вычисление обратной матрицы
        inverse_trans_mat = np.linalg.inv(trans_mat[:, :2])
        # Вычисление нового значение для каждого пикселя создаваемого изображения
        for i in range(self._height):
            for j in range(self._width):
                x, y = inverse_trans_mat.dot(np.array([[i], [j]]) - trans_mat[:, 2:])

                x, y = round(x[0]), round(y[0])

                if 0 <= x < self._height and 0 <= y < self._width:
                    new_img[i, j] = self._img[x, y]

        return new_img

    # Вывод изображения на экран с возможностью отмечать на нем точки. По нажатию Enter изображение будет закрыто
    def show(self):
        cv2.namedWindow(self._name)
        cv2.setMouseCallback(self._name, self._draw_point)
        while True:
            cv2.imshow(self._name, self._img)
            if cv2.waitKey(20) == 13:
                break
        cv2.destroyAllWindows()

    # Генерация матрицы трансформации по 6 заданным точкам
    def _create_transformation_matrix(self) -> np.ndarray:
        """
        :return: Матрица трансофрмации 3х3
        """
        # Матрица точек, заданных на исходном изображении (3 точки)
        input_points = np.array([[self._points[0][0], self._points[1][0], self._points[2][0]],
                                 [self._points[0][1], self._points[1][1], self._points[2][1]],
                                 [                 1,                  1,                  1]])
        # Матрица, состоящая из 3 точек соответствия
        output_points = np.array([[self._points[3]], [self._points[4]], [self._points[5]]], np.float32)
        transpose_output_points = np.array((output_points[0].T, output_points[1].T, output_points[2].T), np.float32)

        column1 = (transpose_output_points[0] * np.linalg.det(input_points[1:, 1:]) -
                   transpose_output_points[1] * np.linalg.det(np.hstack((input_points[1:, :1],
                                                                         input_points[1:, 2:]))) +
                   transpose_output_points[2] * np.linalg.det(input_points[1:, :2]))
        column2 = (transpose_output_points[0] * np.linalg.det(np.vstack((input_points[:1, 1:],
                                                                         input_points[2:, 1:]))) -
                   transpose_output_points[1] * np.linalg.det(np.array([[input_points[0, 0], input_points[0, 2]],
                                                                        [input_points[2, 0], input_points[2, 2]]])) +
                   transpose_output_points[2] * np.linalg.det(np.vstack((input_points[:1, :2],
                                                                         input_points[2:, :2])))) * -1
        column3 = (transpose_output_points[0] * np.linalg.det(input_points[:2, 1:]) -
                   transpose_output_points[1] * np.linalg.det(np.hstack((input_points[:2, :1],
                                                                         input_points[:2, 2:]))) +
                   transpose_output_points[2] * np.linalg.det(input_points[:2, :2]))

        return np.hstack((column1, column2, column3)) / np.linalg.det(input_points)

    # Рисование точки на изображении по нажатии лкм
    def _draw_point(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self._points.append([x, y])
            cv2.circle(self._img, (x, y), 5, (255, 255, 0), -1)


class App(tkinter.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.master.title("Transform image")

        self.window_height = 200
        self.window_width = 300
        self.pack(fill=tkinter.BOTH, expand=True)
        self.center_window()

        clear_button = tkinter.Button(self, text="Open", command=self._open_image, justify="center",
                                      activebackground="sky blue",
                                      font=font.Font(family="Verdana", size=24, weight="bold"),
                                      fg="red", bg="light gray", bd=5,
                                      relief="groove", overrelief="raised")
        clear_button.pack(expand=True)

    # Выбор файла, хранящегося в локальной системе в одном из трех заданных форматов, и работа с ним
    def _open_image(self):
        f_types = [("Images", '*.jpeg;*.jpg;*.png')]
        file_path = askopenfilename(filetypes=f_types)

        img = Image(file_path)
        img.show()

        self._create_new_image(img)

    # Создание нового изображения по исходному с использованием указанной функции трансформации, его показ на экране,
    # и запись в файл
    def _create_new_image(self, image: Image):
        # Указание необходимой функции трансформации
        new_img = image.bilinear_filtering()

        cv2.imwrite("Transformed.jpg", new_img)
        cv2.namedWindow("Transformed image")
        cv2.imshow("Transformed image", new_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Выравнивание окан приложения по центру экрана
    def center_window(self):
        sw = self.parent.winfo_screenwidth()
        sh = self.parent.winfo_screenheight()

        x = (sw - self.window_width) / 2
        y = (sh - self.window_height) / 2

        self.parent.geometry('%dx%d+%d+%d' % (self.window_width, self.window_height, x, y))


if __name__ == '__main__':
    root = tkinter.Tk()
    app = App(root)
    root.mainloop()
