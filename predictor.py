from typing import List
from unittest import result
from sieve.types import FrameSingleObject, UserMetadata, SingleObject, BoundingBox, TemporalObject
from sieve.predictors import TemporalProcessor
from hyperlpr import HyperLPR_plate_recognition


class PlateExtractor(TemporalProcessor):
    def predict(self, frame: FrameSingleObject, metadata: UserMetadata) -> List[FrameSingleObject]:
        output_objects = []
        frame_number = frame.temporal_object.frame_number
        frame_data = frame.temporal_object.get_array()
        try: 
            results = HyperLPR_plate_recognition(frame_data) 
        except Exception as e:
            print(
                "Caught exception during prediction: ", e
            )    
            return output_objects
        if len(results) > 0:
            res = list(results[0])
            plate, conf, bbox = res[0], res[1], res[2]
            if conf > 0.75:
                output_objects.extend(self.postprocess(plate, conf, bbox, frame_number))
        return output_objects
    
    def postprocess(self, plate, conf, bbox, frame_number):
        out = []
        bounding_box = BoundingBox.from_array([float(i) for i in bbox])
        temporal_object = TemporalObject(frame_number=frame_number, bounding_box=bounding_box, score=conf, plate=plate)
        out.append(SingleObject(cls="license-plate", temporal_object=temporal_object))
        return out
