#!/usr/bin/env python3

import os
import cv2
import numpy as np
import matplotlib.pylab as plt

class HistogramComparator:
    def __init__(self, cardtype):
        self.cardtype = cardtype
        self.img_dir = os.path.abspath(f"./img/{self.cardtype}")
        self.imgs = []
        self.load_imgs()

    def load_imgs(self):
        for img_path in os.listdir(self.img_dir):
            if img_path.endswith(('.png', '.jpeg', '.jpg')):
                img = cv2.imread(os.path.join(self.img_dir, img_path))
                if img_path.startswith('back'):
                    self.back_img = img
                    self.back_img_hist = self._compute_histogram(img)
                else:
                    # TODO: 이미지를 저장하는 것이 아니라 히스토그램을 저장하도록 수정
                    self.imgs.append(img)

    def _compute_histogram(self, img):
        if img is None:
            print("이미지 로드에 실패했습니다.")
            return None
        if img.shape[-1] != 3:
            print("이미지가 BGR 색 공간이 아닙니다.")
            return None
        
        hist_img = cv2.calcHist([img], [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])

        cv2.normalize(hist_img, hist_img, 0, 1, cv2.NORM_MINMAX)

        return hist_img
    
    def compare_histograms_with_backImg(self):
        # TODO: 적당한 비교 방법 결정하기
        methods = {'CORREL': cv2.HISTCMP_CORREL, 'CHISQR': cv2.HISTCMP_CHISQR,
                   'INTERSECT': cv2.HISTCMP_INTERSECT, 'BHATTACHARYYA': cv2.HISTCMP_BHATTACHARYYA}
        
        for name, flag in methods.items():
            print(f'{name: <10}', end='\t')

            ret = cv2.compareHist(self.back_img_hist, self.back_img_hist, flag)
            if flag == cv2.HISTCMP_INTERSECT:
                ret = ret / np.sum(self.back_img_hist)
            print(f"back : {ret:.2f}", end='\t')

            for i, img in enumerate(self.imgs):
                hist = self._compute_histogram(img)
                ret = cv2.compareHist(self.back_img_hist, hist, flag)

                if flag == cv2.HISTCMP_INTERSECT:
                    ret = ret / np.sum(self.back_img_hist)

                print(f"img{i+1} : {ret:.2f}", end='\t')
            print()

        # Display images
        _, axs = plt.subplots(1, len(self.imgs)+1, figsize=(10, 10))

        # Plot back image
        axs[0].imshow(cv2.cvtColor(self.back_img, cv2.COLOR_BGR2RGB))
        axs[0].set_title('back')
        axs[0].axis('off')

        # Plot other images
        for i, img in enumerate(self.imgs):
            axs[i+1].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            axs[i+1].set_title(f'img{i + 1}')
            axs[i+1].axis('off')
        plt.show()


if __name__ == "__main__":
    cardtype = "trump"
    comparator = HistogramComparator(cardtype)
    comparator.compare_histograms_with_backImg()