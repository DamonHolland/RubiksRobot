import tkinter as tk
from tkinter import ttk
import serial
import serial.tools.list_ports
import cv2 as opencv
import MotorControler.RubiksSerialTools as SerTool
from ai import KociembaSolver
from ai.AISolver import AISolver
from ai.RubiksMoves import MoveDecoder, perform_move
from cv.ComputerVisionStatic import ComputerVisionStatic
from model.RubiksCube import RubiksCube
from model.RubiksVisualizer import RubiksVisualizer
from PIL import Image, ImageTk


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


class RobotGUI:
    def __init__(self):
        # Create Rubiks Solving Components
        self.ser = serial.Serial()
        self.ser.baudrate = 9600
        self.cube = RubiksCube()
        self.ai_solver = AISolver("../ai/models/10_Model")
        default_top_cam = "0"
        default_bot_cam = "0"
        self.cv_static = ComputerVisionStatic("../cv/saved_pixels.txt", int(default_top_cam), int(default_top_cam))
        self.visualizer = RubiksVisualizer(self.cube)

        self.available_cams = get_available_cams()
        self.available_coms = get_available_com_ports()

        # Create GUI Root
        self.root = tk.Tk()
        self.root.title('Rubiks Robot GUI')
        self.root.geometry("1000x800")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.iconphoto(False, tk.PhotoImage(file='gui.png'))

        # Configure Style
        style = ttk.Style()
        style.theme_use("clam")
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)
        self.root.columnconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=1)


        # Create Field Labels
        self.com_port_label = tk.Label(self.root, text="COM Port: ")
        self.cam_top_label = tk.Label(self.root, text="Top Camera: ")
        self.cam_bottom_label = tk.Label(self.root, text="Bottom Camera: ")
        self.light_level_label = tk.Label(self.root, text="Light Level: ")
        self.motor_speed_level = tk.Label(self.root, text="Motor Speed: ")
        self.ai_timeout_label = tk.Label(self.root, text="AI Timeout: ")
        self.scramble_count_label = tk.Label(self.root, text="Scramble Count: ")

        # Create GUI Components
        self.com_option_selected = tk.StringVar()  # COM Port
        self.com_option_selected.trace("w", self.on_serial_change)
        self.com_option_selected.set(self.available_coms[0])
        self.com_menu = tk.OptionMenu(self.root, self.com_option_selected, *self.available_coms)
        self.top_cam_selected = tk.StringVar()  # Camera top
        self.top_cam_selected.set(default_top_cam)
        self.top_cam_selected.trace("w", self.on_top_cam_change)
        self.top_cam_menu = tk.OptionMenu(self.root, self.top_cam_selected, *self.available_cams)
        self.bottom_cam_selected = tk.StringVar()  # Camera bottom
        self.bottom_cam_selected.set(default_bot_cam)
        self.bottom_cam_selected.trace("w", self.on_bottom_cam_change)
        self.bottom_cam_menu = tk.OptionMenu(self.root, self.bottom_cam_selected, *self.available_cams)  # Light Level
        self.light_level_slider = tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL, length=200)
        self.light_level_slider.bind("<ButtonRelease-1>", self.on_light_change)
        self.motor_speed_slider = tk.Scale(self.root, from_=200, to=80, orient=tk.HORIZONTAL, length=200)  # Motor Level
        self.motor_speed_slider.set(120)
        self.solve_button = tk.Button(self.root, text="Solve", command=self.on_solve, width=15, height=4)
        self.scramble_button = tk.Button(self.root, text="Scramble", command=self.on_scramble, width=15, height=4)
        self.ai_timeout_level = tk.Scale(self.root, from_=0, to=30, orient=tk.HORIZONTAL, length=200)  # AI Timeout
        self.scramble_count_level = tk.Scale(self.root, from_=1, to=100, orient=tk.HORIZONTAL, length=200)  # Scramble
        self.scramble_count_level.set(30)
        self.video_feed = tk.Label()  # Video Feed

        # Add Components to the GUI
        self.video_feed.grid(row=0, column=0, columnspan=4)  # Video Feed
        self.com_port_label.grid(row=1, column=0, sticky=tk.W)  # COM Port
        self.com_menu.grid(row=1, column=1, sticky=tk.W)
        self.cam_top_label.grid(row=2, column=0, sticky=tk.W)  # Camera top
        self.top_cam_menu.grid(row=2, column=1, sticky=tk.W)
        self.cam_bottom_label.grid(row=3, column=0, sticky=tk.W)  # Camera bottom
        self.bottom_cam_menu.grid(row=3, column=1, sticky=tk.W)
        self.light_level_label.grid(row=4, column=0, sticky=tk.W)  # Light Level
        self.light_level_slider.grid(row=4, column=1, sticky=tk.W)
        self.motor_speed_level.grid(row=5, column=0, sticky=tk.W)  # Motor Speed
        self.motor_speed_slider.grid(row=5, column=1, sticky=tk.W)
        self.ai_timeout_label.grid(row=6, column=0, sticky=tk.W)  # AI Timeout
        self.ai_timeout_level.grid(row=6, column=1, sticky=tk.W)
        self.scramble_count_label.grid(row=7, column=0, sticky=tk.W)  # Scramble Count
        self.scramble_count_level.grid(row=7, column=1, sticky=tk.W)
        self.solve_button.grid(row=8, column=0)  # Solve Button
        self.scramble_button.grid(row=8, column=1, sticky=tk.W)  # Scramble Button

        # Add main events
        self.root.after(0, self.scan_cube)  # Scan Cube Event

        # Run GUI
        self.root.mainloop()

    def scan_cube(self):
        if cube_state := self.cv_static.scan_cube():
            merged = opencv.hconcat([self.cv_static.frame_top, self.cv_static.frame_bot])
            merged = opencv.cvtColor(merged, opencv.COLOR_BGR2RGBA)
            merged = Image.fromarray(merged).resize((1000, 500))
            merged = ImageTk.PhotoImage(image=merged)
            self.video_feed.config(image=merged)
            self.cube.faces = cube_state
            self.root.update()
        self.root.after(0, self.scan_cube)

    def on_serial_change(self, *_args):
        if self.ser: self.ser.close()
        # Set up serial
        self.ser.port = self.com_option_selected.get()
        try:
            self.ser.open()
            print(f"Switched to port {self.ser.port}")
        except serial.serialutil.SerialException:
            print("Failed to open Serial")
            self.ser.close()

    def on_top_cam_change(self, *_args):
        cam = int(self.top_cam_selected.get())
        print(f"Switching top camera to: {str(cam)}")
        self.cv_static.set_top_cam(cam)

    def on_bottom_cam_change(self, *_args):
        cam = int(self.bottom_cam_selected.get())
        print(f"Switching bottom camera to: {str(cam)}")
        self.cv_static.set_bottom_cam(cam)

    def on_light_change(self, *_args):
        SerTool.send_serial(self.ser, f"lights {self.light_level_slider.get()}")

    def on_solve(self):
        self.scan_cube()
        if self.cube.is_solved(): return
        if not KociembaSolver.solve_kociemba(self.cube):
            print("Unsolvable Configuration")
            return
        # Use AI To Calculate Solve
        solve_moves = self.ai_solver.solve(self.cube, int(self.ai_timeout_level.get()))
        if not solve_moves:
            print("Unsolvable Configuration")
            return
        for move in solve_moves: perform_move(self.cube, move)
        solve_moves = [MoveDecoder[i] for i in solve_moves]
        SerTool.send_serial(self.ser, SerTool.parse_moves_simplify(solve_moves, str(self.motor_speed_slider.get())))

    def on_scramble(self):
        test_cube = RubiksCube()
        scramble = test_cube.scramble(int(self.scramble_count_level.get()))
        scramble = [MoveDecoder[i] for i in scramble]
        SerTool.send_serial(self.ser, SerTool.parse_moves_strict(scramble, str(self.motor_speed_slider.get())))

    def on_close(self):
        self.ser.close()
        self.cv_static.terminate_cameras()
        self.visualizer.stop()
        self.root.destroy()


if __name__ == "__main__":
    gui = RobotGUI()
