# -*- coding: utf-8 -*-
"""
图像直方图均衡处理
对光线质量不好的照片进行直方图均衡修正，对比处理前后的相片和直方图曲线
"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# =====================================================
# 请修改此处的图片路径为您的图片路径
# =====================================================
image_path = r'D:\10408\Pictures\test.jpg'
# =====================================================

# 读取图片
print(f"正在读取图片: {image_path}")
im_original = Image.open(image_path)

# 获取原始图片的RGB通道
im_array = np.array(im_original)
Red_orig = im_array[:, :, 0]
Green_orig = im_array[:, :, 1]
Blue_orig = im_array[:, :, 2]

# 计算原始图片的RGB直方图
rHist_orig = np.zeros(256)
gHist_orig = np.zeros(256)
bHist_orig = np.zeros(256)

N, M = Red_orig.shape[0], Red_orig.shape[1]
for i in range(N):
    for j in range(M):
        rHist_orig[Red_orig[i, j]] += 1
        gHist_orig[Green_orig[i, j]] += 1
        bHist_orig[Blue_orig[i, j]] += 1

# 使用HSV空间进行直方图均衡（只对亮度V通道均衡）
im_hsv = im_original.convert("HSV")
h, s, v = im_hsv.split()

# 对亮度通道进行直方图均衡
v_equalized = ImageOps.equalize(v, mask=None)

# 合并均衡后的HSV图像并转换回RGB
im_hsv_equalized = Image.merge('HSV', (h, s, v_equalized))
im_equalized = im_hsv_equalized.convert("RGB")

# 获取均衡后图片的RGB通道
im_eq_array = np.array(im_equalized)
Red_eq = im_eq_array[:, :, 0]
Green_eq = im_eq_array[:, :, 1]
Blue_eq = im_eq_array[:, :, 2]

# 计算均衡后图片的RGB直方图
rHist_eq = np.zeros(256)
gHist_eq = np.zeros(256)
bHist_eq = np.zeros(256)

for i in range(N):
    for j in range(M):
        rHist_eq[Red_eq[i, j]] += 1
        gHist_eq[Green_eq[i, j]] += 1
        bHist_eq[Blue_eq[i, j]] += 1

# 计算灰度直方图（用于更直观地观察亮度分布）
# Grey = R×0.299 + G×0.587 + B×0.114
gray_orig = (0.299 * Red_orig + 0.587 * Green_orig + 0.114 * Blue_orig).astype(np.uint8)
gray_eq = (0.299 * Red_eq + 0.587 * Green_eq + 0.114 * Blue_eq).astype(np.uint8)

grayHist_orig = np.zeros(256)
grayHist_eq = np.zeros(256)

for i in range(N):
    for j in range(M):
        grayHist_orig[gray_orig[i, j]] += 1
        grayHist_eq[gray_eq[i, j]] += 1

# 创建对比图
fig = plt.figure(figsize=(16, 12))

# 第一行：原始图片和均衡后图片对比
ax1 = plt.subplot(3, 2, 1)
ax1.imshow(im_original)
ax1.set_title('原始图片', fontsize=14)
ax1.axis('off')

ax2 = plt.subplot(3, 2, 2)
ax2.imshow(im_equalized)
ax2.set_title('直方图均衡后图片', fontsize=14)
ax2.axis('off')

# 第二行：灰度直方图对比
ax3 = plt.subplot(3, 2, 3)
ax3.plot(grayHist_orig, 'k-', linewidth=1)
ax3.fill_between(range(256), grayHist_orig, alpha=0.3, color='gray')
ax3.set_title('原始图片灰度直方图', fontsize=12)
ax3.set_xlabel('灰度值 (0-255)')
ax3.set_ylabel('像素数量')
ax3.set_xlim([0, 255])
ax3.grid(True, alpha=0.3)

ax4 = plt.subplot(3, 2, 4)
ax4.plot(grayHist_eq, 'k-', linewidth=1)
ax4.fill_between(range(256), grayHist_eq, alpha=0.3, color='gray')
ax4.set_title('均衡后图片灰度直方图', fontsize=12)
ax4.set_xlabel('灰度值 (0-255)')
ax4.set_ylabel('像素数量')
ax4.set_xlim([0, 255])
ax4.grid(True, alpha=0.3)

# 第三行：RGB三通道直方图对比
ax5 = plt.subplot(3, 2, 5)
ax5.plot(rHist_orig, 'r-', linewidth=1, label='Red', alpha=0.8)
ax5.plot(gHist_orig, 'g-', linewidth=1, label='Green', alpha=0.8)
ax5.plot(bHist_orig, 'b-', linewidth=1, label='Blue', alpha=0.8)
ax5.set_title('原始图片RGB直方图', fontsize=12)
ax5.set_xlabel('像素值 (0-255)')
ax5.set_ylabel('像素数量')
ax5.set_xlim([0, 255])
ax5.legend(loc='upper right')
ax5.grid(True, alpha=0.3)

ax6 = plt.subplot(3, 2, 6)
ax6.plot(rHist_eq, 'r-', linewidth=1, label='Red', alpha=0.8)
ax6.plot(gHist_eq, 'g-', linewidth=1, label='Green', alpha=0.8)
ax6.plot(bHist_eq, 'b-', linewidth=1, label='Blue', alpha=0.8)
ax6.set_title('均衡后图片RGB直方图', fontsize=12)
ax6.set_xlabel('像素值 (0-255)')
ax6.set_ylabel('像素数量')
ax6.set_xlim([0, 255])
ax6.legend(loc='upper right')
ax6.grid(True, alpha=0.3)

plt.suptitle('图像直方图均衡处理对比', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.subplots_adjust(top=0.93)

# 保存结果
output_path = image_path.rsplit('.', 1)[0] + '_equalized_comparison.png'
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"对比图已保存为: {output_path}")

# 保存均衡后的图片
equalized_image_path = image_path.rsplit('.', 1)[0] + '_equalized.jpg'
im_equalized.save(equalized_image_path)
print(f"均衡后图片已保存为: {equalized_image_path}")

plt.show()

print("\n处理完成！")
print("直方图均衡通过对HSV颜色空间中的V（亮度）通道进行均衡化，")
print("改善了图片的对比度和整体亮度分布。")
