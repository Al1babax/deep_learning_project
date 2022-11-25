from pynput.mouse import Listener
import tkinter as tk
from functools import partial


class DrawShapes(tk.Canvas):
    def __init__(self, **kwargs):
        # setup
        master = tk.Tk()
        master.attributes('-alpha', 0.2)
        master.configure(bg="black", cursor="cross")
        master.attributes('-fullscreen', True)
        master.bind('<Escape>', lambda e: master.quit())
        master.wm_attributes("-transparentcolor", "black")
        super().__init__(master, **kwargs)
        self.pack(fill=tk.BOTH, expand=tk.YES)

        # draw canvas
        image = self.create_rectangle(0, 0, 10000, 10000, width=5, fill='gray')

        # setup tags for canvas
        self.tag_bind(image, '<Button-1>', self.on_click)
        self.tag_bind(image, '<Button1-Motion>', self.on_motion)
        self.tag_bind(image, '<ButtonRelease-1>', self.on_release)

        # to only draw one rectangle
        self.draw_recs = 0

        # coordinates to save
        self.coordinates = [[], []]

    def on_click(self, event):
        """fires when user clicks on the background ... creates a new rectangle"""
        self.start = event.x, event.y
        self.coordinates[0] = (event.x, event.y)
        # print(event)
        # print(type(event))
        if self.draw_recs == 0:
            self.current = self.create_rectangle(*self.start, *self.start, width=5, fill='black')
            self.tag_bind(self.current, '<Button-1>', partial(self.on_click_rectangle, self.current))
            self.tag_bind(self.current, '<Button1-Motion>', self.on_motion)
            self.draw_recs = 1

    def on_click_rectangle(self, tag, event):
        """fires when the user clicks on a rectangle ... edits the clicked on rectangle"""
        self.current = tag
        x1, y1, x2, y2 = self.coords(tag)
        if abs(event.x - x1) < abs(event.x - x2):
            # opposing side was grabbed; swap the anchor and mobile side
            x1, x2 = x2, x1
        if abs(event.y - y1) < abs(event.y - y2):
            y1, y2 = y2, y1
        self.start = x1, y1

    def on_motion(self, event):
        """fires when the user drags the mouse ... resizes currently active rectangle"""
        self.coords(self.current, *self.start, event.x, event.y)
        self.coordinates[1] = (event.x, event.y)

    def on_release(self, event):
        """fires when the user releases the mouse ... saves the current rectangle"""
        self.master.destroy()


def region(queue="", DEBUG=False):
    coordinates = [
        (0, 0),
        (0, 0)
    ]

    def on_move(x, y):
        pass

    def on_click(x, y, button, pressed):
        if pressed and str(button) == "Button.left":
            # print(x, y, button, pressed)

            if coordinates[0] == (0, 0):
                coordinates[0] = (x, y)
            else:
                coordinates[1] = (x, y)
                listener.stop()

    with Listener(on_move=on_move, on_click=on_click) as listener:
        listener.join()
        if not DEBUG:
            queue.put(coordinates)


def main(queue=""):
    c = DrawShapes()
    c.pack()
    c.mainloop()
    if type(queue) != str:
        queue.put(c.coordinates)
    else:
        print(c.coordinates)


if __name__ == '__main__':
    main()
