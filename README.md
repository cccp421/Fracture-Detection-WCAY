# WCAY Object Detection of Fractures for X-ray Images of Multiple Sites  
This article was published in [Scientific Reports](https://www.nature.com/articles/s41598-024-77878-6).  


## Abstract  
Presented herein is the WCAY (Weighted Channel attention YOLO) model, meticulously crafted to identify fracture features across diverse X-ray image sites. This model integrates novel core operators and an innovative attention mechanism to enhance its efficacy. Initially, leveraging the benefits of DSConv (Dynamic Snake Convolution), adept at capturing elongated tubular structural features, we introduce the DSC-C2f module to augment the model's fracture detection performance by replacing a portion of C2f. Subsequently, we integrate the newly proposed Weighted Channel attention (WCA) mechanism into the architecture to bolster feature fusion and improve fracture detection across various sites. Comparative experiments were conducted, evaluating the performance of several attention mechanisms. These enhancement strategies were validated through experimentation on public X-ray image datasets (FracAtlas and GRAZPEDWRI-DX). Multiple experimental comparisons substantiate the model's efficacy, demonstrating its superior accuracy and real-time detection capabilities. According to the experimental findings, on the FracAtlas dataset, our WCAY model exhibits a notable 8.8% improvement in mean Average Precision (mAP) over the original model. On the GRAZPEDWRI-DX dataset, the mAP reaches 64.4%, with a detection accuracy of 93.9% for the "fracture" category alone. The proposed model represents a substantial advancement over the original algorithm when compared to other state-of-the-art object detection models.     

![Figure1.jpg](https://github.com/cccp421/Fracture-Detection-WCAY/blob/main/images/%E5%9B%BE%E7%89%871.png)  
#### Figure.1 Model structure of Weight Channel Attention YOLO (WCAY).  
  

![Figure2.jpg](https://github.com/cccp421/Fracture-Detection-WCAY/blob/main/images/%E5%9B%BE%E7%89%872.png)  
#### Figure.2 The principle of Weight Channel Attention (WCA) algorithm.   

## Dynamic Serpentine Convolution Reference Source  
DSCNet：https://github.com/yaoleiqi/dscnet  

## Sources of data sets used in this study
`FracAtlas`：https://figshare.com/articles/dataset/The_dataset/22363012  
`GRAZPEDWRI-DX`：https://figshare.com/articles/dataset/GRAZPEDWRI-DX/14825193  
`NEU-DET`：http://faculty.neu.edu.cn/songkechen/zh_CN/zhym/263269/list/index.htm  
`SSDD`：https://github.com/TianwenZhang0825/Official-SSDD  
  
Loading…

  
