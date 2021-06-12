import os
from PIL import Image
import math
import sys
import pickle
import warnings


def color_distance(c1, c2):
    (r1, g1, b1) = c1
    (r2, g2, b2) = c2
    return math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)


def get_average_color(image):
    input_image = image.resize((1, 1))
    return input_image.getpixel((0, 0))


def find_file(target_color, average_colors, files):
    min_index = 0
    min_distance = sys.maxsize
    for i in range(len(average_colors)):
        curr_color = average_colors[i]
        distance = color_distance(target_color, curr_color)
        if distance < min_distance:
            min_index = i
            min_distance = distance
    return files[min_index]


def resize_target_image(input_image):
    warnings.filterwarnings("ignore")
    w, h = input_image.size
    # SCALE = int(math.sqrt(178956970) // max(w, h))

    SCALE = int(math.sqrt(37000000) // max(w, h))  # with tile size of 35, under 8mb for disc
    input_image = input_image.resize((w * SCALE, h * SCALE)).convert("RGB")
    w, h = input_image.size
    input_image = input_image.crop((0, 0, w - w % TILE_SIZE, h - h % TILE_SIZE))
    return input_image


# if __name__ == '__main__':
#     if len(sys.argv) < 3:
#         print('Usage: {} <image> <input images directory>\r'.format(sys.argv[0]))
#         exit()

TILE_SIZE = 35

def create_mosaic(server_dir, image_path, avatars_path):
    tiles_dir = avatars_path
    input_image = resize_target_image(Image.open(image_path).copy())
    w, h = input_image.size
    output_image = Image.new("RGB", (w, h))
    data_dir = os.path.join(server_dir, "data")

    files = []
    average_colors = []
    PIK_files = os.path.join(data_dir, "files.dat")
    PIK_average_colors = os.path.join(data_dir, "average_colors.dat")

    if os.path.exists(data_dir) and os.path.exists(PIK_files) and os.path.exists(PIK_average_colors):
        with open(PIK_files, "rb") as f:
            files = pickle.load(f)
        with open(PIK_average_colors, "rb") as f:
            average_colors = pickle.load(f)
    else:
        for root, subFolders, xfiles in os.walk(tiles_dir):
            for filename in xfiles:
                lower_name = filename.lower()
                if lower_name.endswith(".jpg") or lower_name.endswith(".jpeg") or lower_name.endswith(".png"):
                    image = Image.open(os.path.join(root, filename)).resize((TILE_SIZE, TILE_SIZE)).convert("RGB")
                    average_color = get_average_color(image)
                    average_colors.append(average_color)
                    files.append(image)
                    print('Reading {:40.40}'.format(filename), flush=True, end='\r')

    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    with open(PIK_files, "wb") as f:
        pickle.dump(files, f)
    with open(PIK_average_colors, "wb") as f:
        pickle.dump(average_colors, f)

    num_r, num_c = h // TILE_SIZE, w // TILE_SIZE

    count = 0
    total = num_r * num_c
    for r in range(num_r):
        for c in range(num_c):
            x = c * TILE_SIZE
            y = r * TILE_SIZE
            curr_image = input_image.crop((x, y, x + TILE_SIZE, y + TILE_SIZE))
            average_color = get_average_color(curr_image)
            file = find_file(average_color, average_colors, files)
            output_image.paste(file, (x, y, x + TILE_SIZE, y + TILE_SIZE))
            count += 1
            print(f'Generating image: {round(count / total * 100, 2)}', flush=True, end='\r')
    output_dir = os.path.join(server_dir, "output_images")
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    output_image_path = os.path.join(output_dir, 'output_image.jpeg')
    output_image.save(output_image_path)
    return output_image_path

    # for i in range(100):
    #     output_image_path = os.path.join(output_dir, "output_image_{}.jpeg".format(i))
    #     if not os.path.exists(output_image_path):
    #         output_image.save(output_image_path)
    #         print("Photomosaic image created!")
    #         break
