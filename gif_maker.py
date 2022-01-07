import glob
from PIL import Image

def make_gif(png_folder):
    frames = [Image.open(image) for image in glob.glob(f"{png_folder}/*.PNG")]
    frame_one = frames[0]
    frame_one.save("my__timetable.gif", format="GIF", append_images=frames,
               save_all=True, duration= 600, loop=0) #framerate determined by duration 
    
if __name__ == "__main__":
    make_gif("G:\My Drive\Personal portfolio\Coding 101\Hacknroll2022")
