# DeepMSWeb

A Web-Based Decision Support System via Deep Learning for Automatic Detection of MS Lesions

## Introduction

This reposity a Flask application for detection of MS lession with Mask R-CNN 

![block diagram](static/img/githubs/deppmsblokK2_k.png)

And this application three services

![services](static/img/githubs/deppmsuseCaseB_k.png)

## Background
The application include improved [matterport-maskrcnn](https://github.com/matterport/Mask_RCNN)

## How To Use



`make project`

`cd project`

`python -m venv .env`

`.env\Script\activate`

next 2 lines for cuda 10.1

`pip install tensorflow==2.2.0`

`pip install keras==2.3.1  `    

after at all:

`pip install -r requirements.txt`


Citing Improved Mask R-CNN
--------------------------

```BibTeX
@article{yildirim2020automatic,
  title={Automatic detection of multiple sclerosis lesions using Mask R-CNN on magnetic resonance scans},
  author={Yıldırım, Mehmet Süleyman and Dandıl, Emre},
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

