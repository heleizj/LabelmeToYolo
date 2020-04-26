# LabelmeToYolo
  YOLO-Mark is not a good tool to get labels of the training sets for object detection,So we use labelme to get the labels, then transform them to the format of YOLO.
  this program only need one parameter --data_dir. this is your derictory which contains the images and the json files.the json files are generated after you use labelme to annotated images.
  the json files contain the information of the polygon, the aim of this program is contvert the json files to the information of bounding boxes which are needed in YOLO training.
  the command is like this "python load_json_pro.py --data_dir D:\your_derictory\"(just a example)
after running this program you will see a derictrory at your data derictory's parent derictory named 'yolo_need' and a text file named
'yolo_train.txt' both of them are needed for YOLO training.
if any problem or bug appearance ,please contact with this email 17796488802@163.com.
