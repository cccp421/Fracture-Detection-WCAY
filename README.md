# WCAY Object Detection of Fractures for X-ray Images of Multiple Sites  
This article was published in [Scientific Reports](https://www.nature.com/articles/s41598-024-77878-6).  
#### *Subsequent release of the corresponding code file...



## Abstract  
Presented herein is the WCAY (Weighted Channel attention YOLO) model, meticulously crafted to identify fracture features across diverse X-ray image sites. This model integrates novel core operators and an innovative attention mechanism to enhance its efficacy. Initially, leveraging the benefits of DSConv (Dynamic Snake Convolution), adept at capturing elongated tubular structural features, we introduce the DSC-C2f module to augment the model's fracture detection performance by replacing a portion of C2f. Subsequently, we integrate the newly proposed Weighted Channel attention (WCA) mechanism into the architecture to bolster feature fusion and improve fracture detection across various sites. Comparative experiments were conducted, evaluating the performance of several attention mechanisms. These enhancement strategies were validated through experimentation on public X-ray image datasets (FracAtlas and GRAZPEDWRI-DX). Multiple experimental comparisons substantiate the model's efficacy, demonstrating its superior accuracy and real-time detection capabilities. According to the experimental findings, on the FracAtlas dataset, our WCAY model exhibits a notable 8.8% improvement in mean Average Precision (mAP) over the original model. On the GRAZPEDWRI-DX dataset, the mAP reaches 64.4%, with a detection accuracy of 93.9% for the "fracture" category alone. The proposed model represents a substantial advancement over the original algorithm when compared to other state-of-the-art object detection models.     


![Figure6.jpg](https://github.com/cccp421/Fracture-Detection-WCAY/blob/main/Figure6.jpg)  
#### The principle of Weight Channel Attention (WCA) algorithm.  

## Sources of data sets used in this study
`FracAtlas`：https://figshare.com/articles/dataset/The_dataset/22363012  
`GRAZPEDWRI-DX`：https://figshare.com/articles/dataset/GRAZPEDWRI-DX/14825193  
`NEU-DET`：http://faculty.neu.edu.cn/songkechen/zh_CN/zhym/263269/list/index.htm  
`SSDD`：https://github.com/TianwenZhang0825/Official-SSDD  
  
Loading…

  
 | Peer review | date | 
 | --- | --- | 
 | __Production__ |  | 
 | Publishing and rights complete | 28 Oct 2024 | 
 | __Publishing and rights__ |  | 
 | Submission is in publishing and rights | 27 Oct 2024 | 
 | __Submission accepted__ |  | 
 | Submission accepted | 25 Oct 2024 | 
 | __Peer review__ |  | 
 | Reviewer report(s) received | 23 Oct 2024 | 
 | Reviewer(s) accepted | 02 Oct 2024 | 
 | First reviewer(s) invited | 23 Sep 2024 | 
 | Submission passed technical check | 21 Sep 2024 | 
 | Amendment received | 21 Sep 2024 | 
 | Amendment requested | 21 Sep 2024 | 
 | Revision received | 17 Sep 2024 | 
 | Revision requested | 09 Sep 2024 | 
 | Reviewer report(s) received | 21 Aug 2024 | 
 | Reviewer(s) accepted | 09 Aug 2024 | 
 | First reviewer(s) invited | 22 Jul 2024 | 
 | __With editor__ |  | 
 | Editor assigned | 16 Jul 2024 |  
 | __Editorial assignment__ |  | 
 | Ready for editorial assignment | 20 May 2024 | 
 | __Technical check__ |  | 
 | Submission passed technical check | 20 May 2024 | 
 | Amendment received | 19 Apr 2024 | 
 | Amendment requested | 19 Apr 2024 | 
 | Submission is under technical check | 17 Apr 2024 | 
 
