import cv2
import easyocr
import numpy as np
from tqdm import tqdm

def ocr_video(
    input_path: str,
    output_path: str,
    langs=('en',),
    threshold: float = 0.5,
    process_every_n_frames: int = 1,
    use_gpu: bool = False
):
    reader = easyocr.Reader(list(langs), gpu=use_gpu)

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open video: {input_path}")

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    if not out.isOpened():
        cap.release()
        raise RuntimeError(f"Could not create output video: {output_path}")

    frame_idx = 0
    last_result = []

    for _ in tqdm(range(total_frames), desc="Processing frames", unit="frame"):
        ret, frame = cap.read()
        if not ret:
            break

        if process_every_n_frames == 1 or (frame_idx % process_every_n_frames == 0):
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            last_result = reader.readtext(rgb)

        for bbox, text, confidence in last_result:
            if confidence < threshold:
                continue

            pts = np.array(bbox, dtype=np.int32)
            x_min = int(np.min(pts[:, 0]))
            y_min = int(np.min(pts[:, 1]))
            x_max = int(np.max(pts[:, 0]))
            y_max = int(np.max(pts[:, 1]))

            cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

            text_y = max(0, y_min - 10)
            cv2.putText(
                frame,
                text,
                (x_min, text_y),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2,
                cv2.LINE_AA
            )

        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()
    print(f"Done. Wrote: {output_path}")


if __name__ == "__main__":
    ocr_video(
        input_path="input.mp4",
        output_path="output_ocr.mp4",
        langs=("en",),
        threshold=0.6,
        process_every_n_frames=5,
        use_gpu=True
    )
