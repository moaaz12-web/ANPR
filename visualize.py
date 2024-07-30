import ast
import cv2
import numpy as np
import pandas as pd

def draw_border(img, top_left, bottom_right, color=(0, 255, 0), thickness=5, line_length_x=200, line_length_y=200):
    x1, y1 = top_left
    x2, y2 = bottom_right

    cv2.line(img, (x1, y1), (x1, y1 + line_length_y), color, 2)  #-- top-left
    cv2.line(img, (x1, y1), (x1 + line_length_x, y1), color, 2)

    cv2.line(img, (x1, y2), (x1, y2 - line_length_y), color, 2)  #-- bottom-left
    cv2.line(img, (x1, y2), (x1 + line_length_x, y2), color, 2)

    cv2.line(img, (x2, y1), (x2 - line_length_x, y1), color, 2)  #-- top-right
    cv2.line(img, (x2, y1), (x2, y1 + line_length_y), color, 2)

    cv2.line(img, (x2, y2), (x2, y2 - line_length_y), color, 2)  #-- bottom-right
    cv2.line(img, (x2, y2), (x2 - line_length_x, y2), color, 2)

    return img

def process_video_with_license_plate(video_path, results_path, output_path, authorized_plates):
    print("Called process_video_with_license_plate function")
    results = pd.read_csv(results_path)

    cap = cv2.VideoCapture(video_path)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Specify the codec
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    license_plate = {}
    for car_id in np.unique(results['car_id']):
        max_ = np.amax(results[results['car_id'] == car_id]['license_number_score'])
        license_plate[car_id] = {'license_crop': None,
                                 'license_plate_number': results[(results['car_id'] == car_id) &
                                                                 (results['license_number_score'] == max_)]['license_number'].iloc[0]}
        cap.set(cv2.CAP_PROP_POS_FRAMES, results[(results['car_id'] == car_id) &
                                                 (results['license_number_score'] == max_)]['frame_nmr'].iloc[0])
        ret, frame = cap.read()

        x1, y1, x2, y2 = ast.literal_eval(results[(results['car_id'] == car_id) &
                                                  (results['license_number_score'] == max_)]['license_plate_bbox'].iloc[0].replace('[ ', '[').replace('   ', ' ').replace('  ', ' ').replace(' ', ','))

        license_crop = frame[int(y1):int(y2), int(x1):int(x2), :]
        license_crop = cv2.resize(license_crop, (int((x2 - x1) * 400 / (y2 - y1)), 400))

        license_plate[car_id]['license_crop'] = license_crop

    frame_nmr = -1

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    ret = True
    while ret:
        ret, frame = cap.read()
        frame_nmr += 1
        if ret:
            df_ = results[results['frame_nmr'] == frame_nmr]
            for row_indx in range(len(df_)):
                car_x1, car_y1, car_x2, car_y2 = ast.literal_eval(df_.iloc[row_indx]['car_bbox'].replace('[ ', '[').replace('   ', ' ').replace('  ', ' ').replace(' ', ','))

                x1, y1, x2, y2 = ast.literal_eval(df_.iloc[row_indx]['license_plate_bbox'].replace('[ ', '[').replace('   ', ' ').replace('  ', ' ').replace(' ', ','))
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 2)

                license_crop = license_plate[df_.iloc[row_indx]['car_id']]['license_crop']
                H, W, _ = license_crop.shape

                license_plate_number = license_plate[df_.iloc[row_indx]['car_id']]['license_plate_number']
                text_position = (int((x1 + x2) / 2), int(y1 - 10))  # Position slightly above the rectangle's top edge

                if license_plate_number not in authorized_plates:
                    draw_border(frame, (int(car_x1), int(car_y1)), (int(car_x2), int(car_y2)), (0, 0, 255), 25,
                            line_length_x=200, line_length_y=200)
                    cv2.putText(frame,
                            f"Unauthorized {license_plate_number}",
                            text_position,
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.5,  # Font scale
                            (0, 0, 255),  # Red color for the text
                            2)  # Thickness of the text
                else:
                    draw_border(frame, (int(car_x1), int(car_y1)), (int(car_x2), int(car_y2)), (0, 255, 0), 25,
                            line_length_x=200, line_length_y=200)
                    cv2.putText(frame,
                                f"Authorized {license_plate_number}",
                                text_position,
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.5,  # Font scale
                                (0, 255, 0),  # Red color for the text
                                2)  # Thickness of the text

            out.write(frame)
            # frame = cv2.resize(frame, (1280, 720))

            # cv2.imshow('frame', frame)
            # cv2.waitKey(1)

    out.release()
    cap.release()

# Usage:
# process_video_with_license_plate('./assets/demo.mp4', './assets/results/test_interpolated.csv', './assets/results/out.mp4', ['GY15OGJ', 'GX15OGJ', 'JP05JED'])


