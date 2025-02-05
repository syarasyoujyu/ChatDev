'''
DOCSTRING
Defines the PredictionModel class and predict_drawing function.
Predicts a straight line continuation based on the last two points.
'''
import numpy as np
def predict_drawing(drawing_data, prediction_length=20):
    """
    Predicts the continuation of a drawing using a polynomial fit.
    The input drawing data is normalized to a range between 0 and 1
    before fitting the polynomial, and the predicted points are scaled
    back to the original coordinate system.
    Args:
        drawing_data (list): A list of (x, y) tuples representing the drawing points.
        prediction_length (int): The number of points to predict.
    Returns:
        list: A list of (x, y) tuples representing the predicted points, or an empty list
              if prediction is not possible.
    """
    if len(drawing_data) < 3:  # Need at least 3 points for a quadratic fit
        return []
    x_coords, y_coords = zip(*drawing_data)
    x_coords = np.array(x_coords)
    y_coords = np.array(y_coords)
    # Normalize the x and y coordinates
    min_x, max_x = np.min(x_coords), np.max(x_coords)
    min_y, max_y = np.min(y_coords), np.max(y_coords)
    if max_x == min_x or max_y == min_y: # check edge case, where points are almost on the same position
        return []
    x_coords_normalized = (x_coords - min_x) / (max_x - min_x)
    y_coords_normalized = (y_coords - min_y) / (max_y - min_y)
    # Fit a 2nd degree polynomial (quadratic) to the *normalized* data
    try:
        poly_x = np.poly1d(np.polyfit(range(len(x_coords_normalized)), x_coords_normalized, 2))
        poly_y = np.poly1d(np.polyfit(range(len(y_coords_normalized)), y_coords_normalized, 2))
    except np.linalg.LinAlgError:
        # Handle cases where the fit fails (e.g., nearly straight line)
        return []
    predicted_points = []
    start_index = len(x_coords_normalized)  # Start prediction from the end of the drawing
    for i in range(1, prediction_length + 1):
        next_x_normalized = poly_x(start_index + i)
        next_y_normalized = poly_y(start_index + i)
        # Scale the predicted points *back* to the original coordinate system
        next_x = next_x_normalized * (max_x - min_x) + min_x
        next_y = next_y_normalized * (max_y - min_y) + min_y
        predicted_points.append((next_x, next_y))
    return predicted_points