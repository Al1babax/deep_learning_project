from pynput.mouse import Listener


def region(queue):
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
        queue.put(coordinates)
