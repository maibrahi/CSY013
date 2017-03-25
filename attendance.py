from PIL import Image
import math

class Attendance:

    def get_sheet_pixels(self, filename):
        image = Image.open(filename).convert('L')
        pixels = image.load()
        width, height = image.size
        pixel_map = [[0 for x in range(width)] for y in range(height)]
        for row in range(height):
            for col in range(width):
                pixel = pixels[col, row]
                pixel_map[row][col] = pixel
        return pixel_map

    def get_attendance(self, students_on_sheet, pixel_map):
        attendance = []
        total_cols = 11
        total_rows = 14

        image = Image.open("att4.png").convert('L')
        picture = Image.new( image.mode, image.size)
        picture_new = picture.load()

        rows = len(pixel_map)
        cols = len(pixel_map[0])
        base_col = math.ceil((cols//total_cols)*7.2)
        base_row = math.ceil((rows//total_rows)*3.1)
        col_len = cols//total_cols
        row_len = rows//total_rows
        box_area = math.ceil((row_len*0.6)*(col_len*0.8))
        box_threshold = box_area*(3/100)
        pixel_threshold = 100
        for student in range(students_on_sheet):
            coloured_pixels = 0
            student_number = student%10

            for row in range(math.ceil(row_len*.7)):
                for col in range(math.ceil(col_len*2.8)):
                    row_index = base_row + (row_len*student_number) + row
                    col_index = base_col+col
                    current_pixel = pixel_map[row_index][col_index]
                    picture_new[col, row] = (current_pixel)
                    if(current_pixel < pixel_threshold):
                        coloured_pixels += 1

            if(coloured_pixels >= box_threshold):
                print(str(coloured_pixels) + " coloured pixels. Threshold is: " + str(box_threshold))
                attendance.append(1)
            else:
                print(str(coloured_pixels) + " coloured pixels. Threshold is: " + str(box_threshold))
                attendance.append(0)
            picture.save('box1' + str(student) + '.png')
        return attendance

    def get_attendance_list(self, sheets, total_students):
        attendance_list = []
        students_on_sheet = []
        students_on_page = 10

        for i in range(total_students//students_on_page):
            students_on_sheet.append(students_on_page)
        students_on_sheet.append(total_students%students_on_page)

        current_sheet = 0

        for sheet in range(len(sheets)):
            pixel_map = self.get_sheet_pixels(sheets[sheet])
            sheet_attendance = self.get_attendance(students_on_sheet[current_sheet], pixel_map)
            current_sheet += 1
            attendance_list.extend(sheet_attendance)
        return attendance_list

################################ USE CASE ##############################
# a = Attendance()
# sheet_list = ["test2.jpg", "test2.jpg", "test2.jpg"]
# attendance_list = a.get_attendance_list(sheet_list, 27)
# print(attendance_list)
