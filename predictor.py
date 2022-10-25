from typing import List
from unittest import result
from sieve.types import FrameSingleObject, UserMetadata, SingleObject, BoundingBox, Temporal
from sieve.predictors import TemporalPredictor
from hyperlpr import HyperLPR_plate_recognition


class PlateExtractor(TemporalPredictor):
    def predict(self, frame: FrameSingleObject, metadata: UserMetadata) -> List[FrameSingleObject]:
        output_objects = []
        frame_number = frame.get_temporal().frame_number
        frame_data = frame.get_temporal().get_array()
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
        temporal = Temporal(frame_number=frame_number, bounding_box=bounding_box, score=conf, plate=plate)
        out.append(SingleObject(cls="license-plate", temporal=temporal))
        return out
