'''
DOCSTRING
Defines the DrawingCanvas class, a custom Tkinter Canvas widget for drawing.
'''
import tkinter as tk
class DrawingCanvas(tk.Canvas):
    """
    A custom Tkinter Canvas widget for drawing.
    """
    def __init__(self, parent, **kwargs):
        """
        Initializes the DrawingCanvas with a white background.
        Args:
            parent: The parent widget.
            **kwargs: Additional keyword arguments to pass to the tk.Canvas constructor.
        """
        super().__init__(parent, **kwargs, bg="white")