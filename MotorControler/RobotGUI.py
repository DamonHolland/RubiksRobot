import tkinter as tk
import serial
import serial.tools.list_ports
import cv2 as opencv


def get_available_com_ports():
    return [str(port).split(" ")[0] for port in serial.tools.list_ports.comports()]


def get_available_cams():
    max_cams = 5
    available_cams = []
    for i in range(max_cams):
        temp_camera = opencv.VideoCapture(i)
        if temp_camera.isOpened():
            available_cams.append(str(i))
            temp_camera.release()
            continue
        return available_cams


def solve_action():
    print("Solve")


def scramble_action():
    print("Scramble")


def run_gui():
    # Create GUI Root
    root = tk.Tk()
    root.title('Rubiks Robot GUI')
    root.geometry("400x260")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.resizable(False, False)

    # Create Field Labels
    com_port_label = tk.Label(root, text="COM Port: ")
    cam_top_label = tk.Label(root, text="Top Camera: ")
    cam_bottom_label = tk.Label(root, text="Bottom Camera: ")
    light_level_label = tk.Label(root, text="Light Level: ")
    motor_speed_level = tk.Label(root, text="Motor Speed: ")

    # Create GUI Components
    com_option_selected = tk.StringVar()
    com_option_selected.set(get_available_com_ports()[0])
    com_menu = tk.OptionMenu(root, com_option_selected, *get_available_com_ports())

    top_cam_option_selected = tk.StringVar()
    top_cam_option_selected.set(get_available_cams()[0])
    top_cam_menu = tk.OptionMenu(root, top_cam_option_selected, *get_available_cams())

    bottom_cam_option_selected = tk.StringVar()
    bottom_cam_option_selected.set(get_available_cams()[0])
    bottom_cam_menu = tk.OptionMenu(root, bottom_cam_option_selected, *get_available_cams())

    light_level_slider = tk.Scale(root, from_=0, to=255, orient=tk.HORIZONTAL, length=200)
    motor_speed_slider = tk.Scale(root, from_=200, to=80, orient=tk.HORIZONTAL, length=200)

    solve_button = tk.Button(root, text="Solve", command=solve_action, width=15, height=4)
    scramble_button = tk.Button(root, text="Scramble", command=scramble_action, width=15, height=4)

    # Add Components to the GUI
    com_port_label.grid(row=0, column=0, sticky=tk.W)
    com_menu.grid(row=0, column=1, sticky=tk.W)

    cam_top_label.grid(row=1, column=0, sticky=tk.W)
    top_cam_menu.grid(row=1, column=1, sticky=tk.W)

    cam_bottom_label.grid(row=2, column=0, sticky=tk.W)
    bottom_cam_menu.grid(row=2, column=1, sticky=tk.W)

    light_level_label.grid(row=4, column=0, sticky=tk.W)
    light_level_slider.grid(row=4, column=1, sticky=tk.W)

    motor_speed_level.grid(row=5, column=0, sticky=tk.W)
    motor_speed_slider.grid(row=5, column=1, sticky=tk.W)

    solve_button.grid(row=8, column=0)
    scramble_button.grid(row=8, column=1)

    # Run GUI
    root.mainloop()


if __name__ == "__main__":
    run_gui()
