import cv2

def process_image(img, imsize=112):
    h,w = img.shape[:2]
    if h >= w:
        pad_left = int((h-w)/2)
        pad_right = h - w - pad_left
        pad_top = 0
        pad_bot = 0
    else:
        pad_top = int((w-h)/2)
        pad_bot = w - h - pad_top
        pad_left = 0
        pad_right = 0
    img = cv2.copyMakeBorder(img, pad_top, pad_bot, pad_left, pad_right,cv2.BORDER_CONSTANT, None, value=0)
    img = cv2.resize(img, (imsize, imsize))
    return img    


def resize_ratio(img, imsize = 720):
    h, w = img.shape[:2]
    max_wh = max(h,w)
    if h >= w:
        new_h = imsize
        new_w = int(w * imsize / h)

    else:
        new_w = imsize
        new_h = int(j * imsize / w)
    img = cv2.resize(img, (new_w, new_h))
    return img