# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.

import mrcnn.model as modellib
from mrcnn import visualize
from mrcnn import utils
from py import configFile
from py import metricQc
from py import deepmswebFx
from flask import Flask, url_for, request, render_template, Response, jsonify, redirect, flash, abort
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import numpy as np
import uuid

import os
import cv2

import tensorflow as tf
print(tf.__version__)

# from util import base64_to_pil, pil2datauri


gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        # Currently, memory growth needs to be the same across GPUs
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        logical_gpus = tf.config.experimental.list_logical_devices('GPU')
        print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPUs")
    except RuntimeError as e:
        # Memory growth must be set before GPUs have been initialized
        print(e)


DEVICE = "/gpu:0"
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
config = configFile.MsMaskConfig()
MODEL_PATH = 'static/h5/msDet.h5'


class InferenceConfig(config.__class__):
    # Run detection on one image at a time
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1
    ALLOW_GROWTH = True
    PER_PROCESS_GPU_MEMORY_FRACTION = 0.9


config = InferenceConfig()
config.display()
with tf.device(DEVICE):
    model = modellib.MaskRCNN(
        mode="inference", model_dir=MODEL_PATH, config=config)


model.load_weights(MODEL_PATH, by_name=True)
model.keras_model._make_predict_function()
print('Loading Weights')
print('Model loaded. Start serving...')


app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = 'static/uploadFolder'
app.config['TEMPLATES_AUTO_RELOAD'] = True
UPLOAD_PRED_PATH = app.config['UPLOAD_FOLDER']
app.config['MAX_CONTENT_LENGTH'] = 16*1024*1024
app.secret_key = "msy"


@app.route('/')
def index():
    t= "DeepMSWeb"
    cap = "Homepage - Test"
    content = "Multiple Sclerosis Detection And Follow-up System Test Page"
    return render_template('main.html', title=t, cap=cap, content=content)


@app.route('/showPic/<filename>')
def detecFile(filename):
    return redirect(url_for('static', filename='uploadFolder/'+filename), code=301)


@app.route('/msDetectionCompare')
def msDetectionCompare():
    title = "DeepMSWeb - Automatic Detection of MS Lesions"
    cap = "Automatic Detection of MS Lesions"
    abstract = "This application page that automatically detects MS plaques in MR images and compares them with physician vision. For this, you must load the segmentation information of the MR images in VGG 1.0.6 format. "
    fxUrl = url_for("msFinderCompare")
    json = True
    return render_template('detection.html', title=title, cap=cap, abstract=abstract, fx=fxUrl, json1=json)

 
@app.route('/msFinderCompare', methods=['POST'])
def msFinderCompare():
    messages = {}
    if request.method == 'POST':
        # formdan dosya gelip gelmediğini kontrol edelim
        if 'fname' not in request.files:
            messages["fileNotSelected"] = {
                "message": "File not selected", "type": "danger"}
            return redirect('msDetectionCompare')

            # kullanıcı dosya seçmemiş ve tarayıcı boş isim göndermiş mi
        f = request.files['fname']
        if f.filename == '':
            messages["fileNotSelected"] = {
                "message": "File not selected", "type": "danger"}
            return redirect('msDetectionCompare')

            # gelen dosyayı güvenlik önlemlerinden geçir
        if f and deepmswebFx.uzanti_kontrol(f.filename):

            filename = secure_filename(f.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            f.save(filepath)

            image = cv2.imread(filepath)
            results = model.detect([image], verbose=1)

            class_names = ['BG', 'msMask']
            r = results[0]
            predFileName = "det_"+filename.split('.')[0]+".jpg"
            print(predFileName)
            pred_path = UPLOAD_PRED_PATH+"/"+predFileName
            class_names = ['BG', 'msPlaque']
            visualize.save_instances(
                image, r['rois'], r['masks'], r['class_ids'], class_names,  r['scores'], path=pred_path)

            fJson = request.files['jsonfname']
            if fJson and deepmswebFx.uzanti_kontrolJson(fJson.filename):
                jsonFile = str(uuid.uuid4())+".json"
                filenameJ = secure_filename(jsonFile)
                filepathJ = os.path.join(
                    app.config['UPLOAD_FOLDER'], filenameJ)
                fJson.save(filepathJ)

                dataset = configFile.MsMaskDataset()
                dataset.sload_msMask(app.config['UPLOAD_FOLDER'], filepathJ)
                dataset.prepare()
                image1, image_meta, gt_class_id, gt_bbox, gt_mask =\
                    modellib.load_image_gt(
                        dataset, config, 0, use_mini_mask=False)
                info = dataset.image_info[0]
                GTFileName = "GT_"+filename.split('.')[0]+".jpg"
                GTFilePath = UPLOAD_PRED_PATH+"/"+GTFileName

                visualize.save_instances(
                    image1, gt_bbox, gt_mask, gt_class_id, class_names, path=GTFilePath)

                GTMatchFile = "GT_over_"+filename.split('.')[0]+".jpg"
                GTMatchPath = UPLOAD_PRED_PATH+"/"+GTMatchFile
                visualize.save_differences(image, gt_bbox, gt_class_id, gt_mask,
                                           r['rois'], r['class_ids'], r['scores'], r['masks'],
                                           dataset.class_names, path=GTMatchPath,
                                           show_box=False
                                           )

                olcekler1 = {}
                result = deepmswebFx.maskCompound(r['masks'])
                reference = deepmswebFx.maskCompound(gt_mask)

                olcekler1["DC"] = metricQc.dice(result, reference)
                iou = utils.compute_overlaps_masks(result, reference)[0][0]
                olcekler1["VOE"] = 1 - iou
                olcekler1["LTPR"] = metricQc.ltpr(result, reference)
                olcekler1["LFPR"] = metricQc.lfpr(result, reference)

                title = "DeepMSWeb - Automatic Detection of MS Lesions"
                cap = "Automatic Detection of MS Lesions"
                abstract = "As a result of the investigations; the automatically detected MS plaque(s) of the "+filename.split(
                    '.')[0]+" file are displayed in detail."
                return render_template('detectionPre.html', title=title, cap=cap, abstract=abstract,
                                       orjFile=filename,   predFileName=predFileName,
                                       GTOverFileName=GTMatchFile,  GTFileName=GTFileName,
                                       olcekler1=olcekler1, olcekMetin=deepmswebFx.olcekMetin, messages=messages)

            else:
                messages["jsonEx"] = {
                    "message": "MS lession only automatic founded, Ground Truth file not exist or wrong", "type": "danger"}

            title = "DeepMSWeb - Automatic Detection of MS Lesions"
            cap = "Automatic Detection of MS Lesions"
            abstract = "As a result of the investigations; the automatically detected MS plaque(s) of the "+filename.split(
                '.')[0]+" file without ground truth are denoted in detail."
            return render_template('detectionPre.html', title=title, cap=cap, abstract=abstract,
                                   orjFile=filename, predFileName=predFileName, messages=messages)

        else:
            messages["notAllowedFile"] = {
                "message": "File not allowed type", "type": "danger"}
            return redirect('msDetectionCompare')
    else:
        abort(401)





@app.route('/about')
def about():
    title = "About"
    cap = "About - Test"
    return render_template('main.html', title=title, cap=cap)


if __name__ == "__main__":
    app.run(debug=True)
