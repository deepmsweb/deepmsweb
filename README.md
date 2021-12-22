# DeepMSWeb

A Web-Based Decision Support System via Deep Learning for Automatic Detection of MS Lesions



https://user-images.githubusercontent.com/94227541/147167047-c2a6ba07-8348-496b-855e-035c5ad4860b.mp4



## Introduction

This reposity a Flask application for detection of MS lession with Mask R-CNN 

![block diagram](static/img/githubs/deppmsblokK2_k.png)

And this application three services

![services](static/img/githubs/deppmsuseCaseB_k.png)

## Background
The application include improved [matterport-maskrcnn](https://github.com/matterport/Mask_RCNN)

## How To Use


```
make project
cd project
python -m venv .env
.env\Script\activate
```
next 2 lines for cuda 10.1
```
pip install tensorflow==2.2.0
pip install keras==2.3.1    
```
after at all:
```
pip install -r requirements.txt
```


Citing Improved Mask R-CNN
--------------------------

```BibTeX
@article{yildirim2020automatic,
  title={Automatic detection of multiple sclerosis lesions using Mask R-CNN on magnetic resonance scans},
  author={Y{\i}ld{\i}r{\i}m, Mehmet S{\"u}leyman and Dand{\i}l, Emre},
  journal={IET Image Processing},
  volume={14},
  number={16},
  pages={4277--4290},
  year={2020},
  publisher={IET}
}
```

Citing DeepMSWeb 
----------------
```
@inproceedings{yildirim2021automated,
  title={Automated Multiple Sclerosis Lesion Segmentation on MR Images via Mask R-CNN},
  author={Y{\i}ld{\i}r{\i}m, Mehmet S{\"u}leyman and Dand{\i}l, Emre},
  booktitle={2021 5th International Symposium on Multidisciplinary Studies and Innovative Technologies (ISMSIT)},
  pages={570--577},
  year={2021},
  organization={IEEE}
}
```
