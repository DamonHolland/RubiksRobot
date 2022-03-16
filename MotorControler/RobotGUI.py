import tkinter
import serial
import serial.tools.list_ports
import cv2 as opencv


def get_available_com_ports():
    return [str(port).split(" ")[0] for port in serial.tools.list_ports.comports()]


def get_available_cams():
    available_cams = []
    for i in range(5):
        temp_camera = opencv.VideoCapture(i)
        if temp_camera.isOpened():
            available_cams.append(str(i))
            temp_camera.release()
            continue
        return available_cams


def run_gui():
    # Create GUI Root
    root = tkinter.Tk()
    root.title('Rubiks Robot GUI')
    root.geometry("400x400")

    # Create Field Labels
    com_port_label = tkinter.Label(root, text="COM Port: ")
    cam_top_label = tkinter.Label(root, text="Top Camera: ")
    cam_bottom_label = tkinter.Label(root, text="Bottom Camera: ")

    # Create GUI Components
    com_option_selected = tkinter.StringVar()
    com_option_selected.set(get_available_com_ports()[0])
    com_menu = tkinter.OptionMenu(root, com_option_selected, *get_available_com_ports())

    top_cam_option_selected = tkinter.StringVar()
    top_cam_option_selected.set(get_available_cams()[0])
    top_cam_menu = tkinter.OptionMenu(root, top_cam_option_selected, *get_available_cams())

    bottom_cam_option_selected = tkinter.StringVar()
    bottom_cam_option_selected.set(get_available_cams()[0])
    bottom_cam_menu = tkinter.OptionMenu(root, bottom_cam_option_selected, *get_available_cams())

    # Add Components to the GUI
    com_port_label.grid(row=0, column=0)
    com_menu.grid(row=0, column=1)
    cam_top_label.grid(row=1, column=0)
    top_cam_menu.grid(row=1, column=1)
    cam_bottom_label.grid(row=2, column=0)
    bottom_cam_menu.grid(row=2, column=1)

    # Run GUI
    root.mainloop()


if __name__ == "__main__":
    run_gui()
