import torch
import torchvision
import mmpose
import cv2
from mmpose.apis import (
    inference_top_down_pose_model,
    init_pose_model,
    vis_pose_result,
    process_mmdet_results,
)
from mmdet.apis import inference_detector, init_detector

try:
    from google.colab.patches import cv2_imshow  # for image visualization in Colab
except ImportError:
    cv2_imshow = cv2.imshow  # for image visualization in local runtime

class PoseEstimator:
    def __init__(self, pose_config, pose_checkpoint, det_config, det_checkpoint):
        self.pose_model = init_pose_model(pose_config, pose_checkpoint)
        self.det_model = init_detector(det_config, det_checkpoint)

    def detect_objects(self, image_path):
        mmdet_results = inference_detector(self.det_model, image_path)
        person_results = process_mmdet_results(mmdet_results, cat_id=1)
        return person_results

    def estimate_pose(self, image_path, person_results, bbox_thr=0.3):
        pose_results, returned_outputs = inference_top_down_pose_model(
            self.pose_model,
            image_path,
            person_results,
            bbox_thr=bbox_thr,
            format='xyxy',
            dataset=self.pose_model.cfg.data.test.type,
        )
        return pose_results

    def visualize_pose(self, image_path, pose_results):
        vis_result = vis_pose_result(
            self.pose_model,
            image_path,
            pose_results,
            dataset=self.pose_model.cfg.data.test.type,
            show=False,
        )
        vis_result = cv2.resize(vis_result, dsize=None, fx=0.5, fy=0.5)
        return vis_result

class ImageProcessor:
    def __init__(self, pose_estimator):
        self.pose_estimator = pose_estimator

    def process_image(self, image_path):
        person_results = self.pose_estimator.detect_objects(image_path)
        pose_results = self.pose_estimator.estimate_pose(image_path, person_results)
        vis_result = self.pose_estimator.visualize_pose(image_path, pose_results)
        return vis_result

# Configuration
pose_config = #pose_conf
pose_checkpoint = #pose_checkpoint
det_config = #detectin_config
det_checkpoint = #detection_checkpoint
image_path = #image_path

# Initialize pose estimator
pose_estimator = PoseEstimator(pose_config, pose_checkpoint, det_config, det_checkpoint)

# Process image
image_processor = ImageProcessor(pose_estimator)
result_image = image_processor.process_image(image_path)

# Display result
cv2_imshow(result_image)