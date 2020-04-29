import cv2
import os

class DBBuilder:
    def __init__(self, dir_path, images_path='./images', ann_filename='annotations.txt', overwrite=False, plates_delimiter=' | '):
        self.file = open(os.path.join(dir_path, ann_filename), 'a')
        self.plates_delimiter = plates_delimiter
        self.image_path = images_path


    def write_line(self, image, image_path, bboxes, nplates):
        line = image_path + ' '
        
        first_plate = True
        for bbox, nplate in zip(bboxes, nplates):
            if first_plate:
                line += ' {} {} {} {} {}'.format(bbox[0], bbox[1], bbox[2], bbox[3], nplate)
                first_plate = False
            else:
                line += '{}{} {} {} {} {}'.format(self.plates_delimiter, bbox[0], bbox[1], bbox[2], bbox[3], nplate)

        line = line+'\n'
        print('writing: {}'.format(line))
        self.file.write(line)

        self.save_image(image, image_path)

    def save_image(self, image, image_path):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        cv2.imwrite(image_path, image_rgb)