import cv2 as cv
import numpy as np

# 1. Define the custom Crop Layer required by HED
class CropLayer(object):
    def __init__(self, params, blobs):
        self.xstart = 0
        self.xend = 0
        self.ystart = 0
        self.yend = 0

    def getMemoryShapes(self, inputs):
        inputShape, targetShape = inputs[0], inputs[1]
        batchSize, numChannels = inputShape[0], inputShape[1]
        height, width = targetShape[2], targetShape[3]

        self.ystart = int((inputShape[2] - targetShape[2]) / 2)
        self.xstart = int((inputShape[3] - targetShape[3]) / 2)

        self.yend = self.ystart + height
        self.xend = self.xstart + width

        return [[batchSize, numChannels, height, width]]

    def forward(self, inputs):
        return [inputs[0][:, :, self.ystart:self.yend, self.xstart:self.xend]]

# 2. Register the layer with OpenCV
cv.dnn_registerLayer('Crop', CropLayer)

def find_faces(image_path="hmm.jpg"):
    # Initialize Haar Cascade
    face_cascade = cv.CascadeClassifier(
        cv.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    image = cv.imread(image_path)
    
    if image is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")

    # Detect faces
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
    print(f"Detected {len(faces)} faces.")
    image = cv.resize(image, (0, 0), fx=0.5, fy=0.5) # Resize for faster processing
    # h, w = image.shape[:2]
    # image = image[80: h // 2 + 280, :w]

    # Load HED model
    prototxt_path = "deploy.prototxt"
    model_path = "hed_pretrained_bsds.caffemodel"
    
    # This should now work without the C++ exception
    net = cv.dnn.readNetFromCaffe(prototxt_path, model_path)
    
    # Create blob
    blob = cv.dnn.blobFromImage(image, scalefactor=1.0, size=(image.shape[1], image.shape[0]),
                                mean=(104.00698793, 116.66876762, 122.67891434),
                                swapRB=False, crop=False)
    
    # Get HED edges
    print("Running forward pass (this may take a moment)...")
    net.setInput(blob)
    edges_hed = net.forward()
    edges_hed = edges_hed[0, 0]
    edges_hed = (edges_hed * 255).astype(np.uint8)
    edges_hed = np.where(edges_hed > 50, 255, 0).astype(np.uint8)

    white_coords = np.argwhere(edges_hed == 255)
    white_count = len(white_coords)
    target_white_count = white_count // 3
    if white_count > target_white_count:
        keep_idx = np.random.choice(white_count, size=target_white_count, replace=False)
        keep_coords = white_coords[keep_idx]
        reduced_edges = np.zeros_like(edges_hed, dtype=np.uint8)
        reduced_edges[keep_coords[:, 0], keep_coords[:, 1]] = 255
        edges_hed = reduced_edges
    
    cv.imshow("HED Edges", edges_hed)
    cv.waitKey(0)
    cv.destroyAllWindows()
    
    # Process low detail (background)
    edges_low_detail = cv.GaussianBlur(edges_hed, (3, 3), 0)
    edges_low_detail = edges_hed.copy()
    edges_low_detail = cv.threshold(edges_low_detail, 80, 155, cv.THRESH_BINARY)[1]
    
    # Process high detail (faces)
    edges_high_detail = edges_hed.copy()
    edges_high_detail = cv.threshold(edges_high_detail, 10, 155, cv.THRESH_BINARY)[1]
    
    # Combine the layers
    result_edges = edges_low_detail.copy()
    for (x, y, w, h) in faces:
        result_edges[y:y+h, x:x+w] = edges_high_detail[y:y+h, x:x+w]
    cv.imshow("Combined Edges", result_edges)
    cv.waitKey(0)
    cv.destroyAllWindows()
    cv.imwrite("faces_with_detail.jpg", result_edges) # Save the combined edges image
    print("Applying thinning algorithm...")
    # The image must be strictly binary (0 or 255) for thinning
    # We use THINNING_ZHANGSUEN, which is fast and reliable
    thinned_edges = cv.ximgproc.thinning(result_edges, thinningType=cv.ximgproc.THINNING_ZHANGSUEN)
    
    # Convert back to BGR so it matches your expected output
    result_edges_bgr = cv.cvtColor(thinned_edges, cv.COLOR_GRAY2BGR)

    return result_edges_bgr, faces

if __name__ == "__main__":
    try:
        image, faces = find_faces("table.jpg")
        
        # Resize for display (adjust fx/fy if the window is too big/small)
        # display_image = cv.resize(image, None, fx=0.5, fy=0.5)
        display_image = image
        
        cv.imshow("Faces with Detail", display_image)
        # cv.imwrite("faces_with_detail.jpg", image) # Save the full resolution version
        cv.waitKey(0)
        cv.destroyAllWindows()
        
    except Exception as e:
        print(f"An error occurred: {e}")