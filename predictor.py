from typing import List
from sieve.types import FrameSingleObject, UserMetadata, SingleObject, BoundingBox, TemporalObject
from sieve.predictors import TemporalProcessor
from darknet2pytorch import Darknet
from utils import do_detect, read_plates

class PlateExtractor(TemporalProcessor):
    def setup(self):
        self.model = Darknet("yolov4.cfg")
        self.model.load_weights("yolov4.weights")

    def predict(self, frame: FrameSingleObject, metadata: UserMetadata) -> List[FrameSingleObject]:
        frame_number = frame.temporal_object.frame_number
        frame_data = frame.temporal_object.get_array()
        
        # Get boxes detected from model
        boxes = do_detect(self.model, frame_data)

        # Get plates from boxes
        results = read_plates(boxes, "classes.names", frame_number)
        output_objects = self.postprocess_yolo(results)
        
        return output_objects

    def postprocess_yolo(self, results):
        out = []
        for box, plate, conf, frame_number in results:
            bounding_box = BoundingBox.from_array([float(i) for i in box])
            score = float(conf)
            temporal_object = TemporalObject(frame_number=frame_number, bounding_box=bounding_box, score=score, plate=plate)
            out.append(SingleObject(cls="license_plate", temporal_object=temporal_object))
