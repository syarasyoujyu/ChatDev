'''
DOCSTRING
Main application file for the drawing app with forecasting.
Creates the main window and integrates the drawing canvas and prediction model.
'''
import tkinter as tk
from drawing_canvas import DrawingCanvas
from prediction_model import predict_drawing
class MainWindow(tk.Tk):
    """
    Main application window for the drawing app with forecasting functionality.
    """
    def __init__(self):
        """
        Initializes the main window with a drawing canvas, predict button, and prediction label.
        Binds mouse events to the canvas for drawing.
        """
        super().__init__()
        self.title("Drawing App with Forecasting")
        self.drawing_canvas = DrawingCanvas(self)
        self.drawing_canvas.pack(expand=True, fill="both")
        self.predict_button = tk.Button(self, text="Predict", command=self.predict)
        self.predict_button.pack()
        self.prediction_label = tk.Label(self, text="Prediction:")
        self.prediction_label.pack()
        self.drawing_data = []  # Store drawing points/lines
        self.drawing_canvas.bind("<B1-Motion>", self.record_drawing)
        self.drawing_canvas.bind("<ButtonRelease-1>", self.stop_recording)
        self.is_drawing = False
        self.prediction_lines = [] # Store prediction line IDs for deletion
    def record_drawing(self, event):
        """
        Records the drawing coordinates when the left mouse button is pressed and moved.
        Args:
            event: The mouse event containing the x and y coordinates.
        """
        if not self.is_drawing:
            self.drawing_data = []  # Restart if not drawing
            self.is_drawing = True
            self.delete_prediction() # Delete previous predictions
        x, y = event.x, event.y
        self.drawing_data.append((x, y))
        if len(self.drawing_data) > 1:
            x0, y0 = self.drawing_data[-2]
            self.drawing_canvas.create_line(x0, y0, x, y, fill="black", width=2)
    def stop_recording(self, event):
        """
        Stops recording the drawing when the left mouse button is released.
        Args:
            event: The mouse event.
        """
        self.is_drawing = False
    def predict(self):
        """
        Initiates the prediction process by calling the prediction model and displaying the result.
        """
        if not self.drawing_data:
            self.prediction_label.config(text="Prediction: No drawing to predict!")
            return
        predicted_points = predict_drawing(self.drawing_data)
        if not predicted_points:
             self.prediction_label.config(text="Prediction: Not enough data to predict!")
             return
        self.delete_prediction() # Delete previous predictions
        # Draw the predicted line on the canvas
        for i in range(len(predicted_points) - 1):
            x0, y0 = predicted_points[i]
            x1, y1 = predicted_points[i+1]
            line_id = self.drawing_canvas.create_line(x0, y0, x1, y1, fill="red", width=2, dash=(4, 4))
            self.prediction_lines.append(line_id) # Store the ID to delete later
        self.prediction_label.config(text="Prediction: Polynomial continuation")
    def delete_prediction(self):
        """
        Deletes the previously drawn prediction lines from the canvas.
        """
        # Delete the prediction lines from the canvas
        for line_id in self.prediction_lines:
            self.drawing_canvas.delete(line_id)
        self.prediction_lines = []
if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()