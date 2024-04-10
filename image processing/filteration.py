import cv2
import numpy as np

def extract_and_center_hsl(image_path, hue_value, saturation_value, lightness_value):
    try:
        # Load the image
        image = cv2.imread(image_path)

        # Convert the image to HSL color space
        hsl = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)

        # Define the color range with tolerance for HSL values
        lower_color = np.array([hue_value - 5, saturation_value - 15, lightness_value - 15])  # Adjusted tolerance
        upper_color = np.array([hue_value + 5, saturation_value + 15, lightness_value + 15])

        # Create a mask for the specified color
        mask = cv2.inRange(hsl, lower_color, upper_color)

        # Apply morphological operations to refine the mask
        kernel = np.ones((3, 3), np.uint8)  # Example kernel for erosion and dilation
        eroded_mask = cv2.erode(mask, kernel, iterations=1)
        dilated_mask = cv2.dilate(eroded_mask, kernel, iterations=1)

        # Find contours (connected regions of the same color)
        contours, _ = cv2.findContours(dilated_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Check if any contours were found
        if contours:
            # Find the largest contour (assumed to be the main object)
            largest_contour = max(contours, key=cv2.contourArea)

            # Calculate the center of the largest contour
            M = cv2.moments(largest_contour)
            center_x = int(M["m10"] / M["m00"])
            center_y = int(M["m01"] / M["m00"])

            # Find the minimum enclosing circle (MEC) for better fit
            (x, y), radius = cv2.minEnclosingCircle(largest_contour)
            radius = int(radius)  # Convert to integer

            # Ensure circle doesn't overlap color (add 1px buffer)
            adjusted_radius = radius + 1

            # Draw the circle on a copy of the image for visualization
            image_copy = image.copy()
            cv2.circle(image_copy, (center_x, center_y), adjusted_radius, (0, 255, 0), 2)  # Green circle

            return center_x, center_y, adjusted_radius, image_with_circle
        else:
            return -1, -1, -1, None
    except cv2.error as e:
        print(f"Error: {e}")
        return None, None, None, None

# Example usage
image_path = "C:/Users/Aditya/OneDrive - YA/Desktop/q.jpg"  # Replace with your image path
hue = 0
saturation = 57
lightness = 56

center_x, center_y, radius, image_with_circle = extract_and_center_hsl(image_path, hue, saturation, lightness)

if image_with_circle is not None:
    cv2.imshow("Image with Circle", image_with_circle)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("Color not found or error occurred.")
