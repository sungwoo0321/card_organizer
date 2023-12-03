#!/usr/bin/env python3

import os
import cv2
# import matplotlib.pyplot as plt

class ORBImageComparator:
    def __init__(self, cardtype):
        self.cardtype = cardtype
        self.img_dir = os.path.abspath(f"./img/{self.cardtype}")
        self.imgs = []
        self.back_img = None
        self.back_kp = None
        self.back_des = None
        self.orb = cv2.ORB_create()
        self.load_imgs()

    def load_imgs(self):
        for img_path in os.listdir(self.img_dir):
            if img_path.endswith(('.png', '.jpeg', '.jpg')):
                img = cv2.imread(os.path.join(self.img_dir, img_path))
                if img_path.startswith('back'):
                    self.back_img = img
                    self.back_kp, self.back_des = self.orb.detectAndCompute(self.back_img, None)
                else:
                    self.imgs.append(img)

    def compare_images_with_backImg(self, match_threshold=30):
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        titles = []

        for i, img in enumerate(self.imgs):
            kp, des = self.orb.detectAndCompute(img, None)
            matches = bf.match(self.back_des, des)
            matches = sorted(matches, key=lambda x: x.distance)

            # Define a threshold to consider a match as a good match
            good_matches = [m for m in matches if m.distance < match_threshold]

            match_number_threshold = 10
            if len(good_matches) > match_number_threshold:
                print(f"Image{i + 1} | Back  | Match number: {len(good_matches)}")
                titles.append(f'img{i + 1} (Back)')
            else:
                print(f"Image{i + 1} | Front | Match number: {len(good_matches)}")
                titles.append(f'img{i + 1} (Front)')

        # # Display images
        # _, axs = plt.subplots(1, len(self.imgs) + 1, figsize=(10, 10))

        # kp, des = self.orb.detectAndCompute(self.back_img, None)
        # back_img_with_kp = cv2.drawKeypoints(self.back_img, kp, None, color=(0, 0,255), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        # axs[0].imshow(cv2.cvtColor(back_img_with_kp, cv2.COLOR_BGR2RGB))
        # axs[0].set_title('back')
        # axs[0].axis('off')

        # for i, img in enumerate(self.imgs):
        #     kp, des = self.orb.detectAndCompute(img, None)
        #     img_with_kp = cv2.drawKeypoints(img, kp, None, color=(0, 0,255), flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        #     axs[i + 1].imshow(cv2.cvtColor(img_with_kp, cv2.COLOR_BGR2RGB))
        #     axs[i + 1].set_title(titles[i])
        #     axs[i + 1].axis('off')
        # plt.show()

if __name__ == "__main__":
    cardtype = "trump"
    comparator = ORBImageComparator(cardtype)
    comparator.compare_images_with_backImg()
