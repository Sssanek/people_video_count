from typing import Any, Tuple

import cv2
import torch
from PIL import Image, ImageDraw


def count_people_on_video(video_path: str, feature_extractor: Any, model: Any,
                          frames_to_process: int) -> Tuple[int, Image.Image]:
    """
    Counts the number of people in a video and returns the result with an image
    that shows the detected people.

    Args:
        video_path: A string representing the path of the video file.
        feature_extractor: An object that is used to extract features from an
        image.
        model: A machine learning model that can detect people in an image.
        frames_to_process: An integer representing the number of frames to be
        processed.

    Returns:
        A tuple consisting of the number of people detected and an image that
        shows the detected people.

    """
    video_capture = cv2.VideoCapture(video_path)
    length = int(video_capture.get(cv2.CAP_PROP_FRAME_COUNT))
    inference_frame_num = max(length // frames_to_process, 1)
    frame_count, people_count = 0, []
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        frame_count += 1
        if not (frame_count % inference_frame_num):
            color_coverted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(color_coverted)
            logits, bboxes = extract_objects(pil_image, feature_extractor,
                                             model)
            pil_image, num_people = plot_results(pil_image, logits, bboxes)
            people_count.append(num_people)

    video_capture.release()
    return round(sum(people_count) / len(people_count)), pil_image


def extract_objects(image: Image, feature_extractor: Any, model: Any)\
        -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Extracts objects from an image and returns the logits and bounding boxes.

    Args:
        image: A PIL Image object.
        feature_extractor: An object that is used to extract features from an
        image.
        model: A machine learning model that can detect people in an image.

    Returns:
        A tuple consisting of the logits and the bounding boxes of the detected
        objects.
    """
    inputs = feature_extractor(images=image, return_tensors="pt")
    outputs = model(**inputs)
    logits = outputs.logits.softmax(-1)[0, :, :-1]
    keep = logits.max(-1).values > 0.9
    target_sizes = torch.tensor(image.size[::-1]).unsqueeze(0)
    postprocessed_outputs = feature_extractor.post_process(outputs,
                                                           target_sizes)
    bboxes_scaled = postprocessed_outputs[0]['boxes'][keep]
    return logits[keep], bboxes_scaled


def plot_results(pil_img: Image.Image, prob: torch.Tensor,
                 boxes: torch.Tensor) -> Tuple[Image.Image, int]:
    """
    Draws bounding boxes around detected objects in the image and returns the
    resulting image with the count of objects.

    Args:
        pil_img: A PIL Image object.
        prob: A tensor representing the probabilities of the detected objects.
        boxes: A tensor representing the bounding boxes of the detected objects.

    Returns:
        A tuple consisting of the image with bounding boxes drawn around
        detected objects and the count of detected objects.
    """
    draw = ImageDraw.Draw(pil_img)
    counter = 0
    for p, (xmin, ymin, xmax, ymax) in zip(prob, boxes.tolist()):
        cl = p.argmax()
        if cl != 1:
            continue
        draw.rectangle([xmin, ymin, xmax, ymax], outline=(255, 0, 0), width=3)
        counter += 1
    return pil_img, counter
