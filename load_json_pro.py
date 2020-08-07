import json
import argparse
import sys
import pdb
import cv2
import os
import shutil

def main(args):
    id_list = make_id_list(args.data_dir)
    for json_file in os.listdir(args.data_dir):
        if json_file.split('.')[-1]=='json':
            json_path = os.path.join(args.data_dir,json_file)
            data=json.load(open(json_path))
            ports_list=[]
            for i in range(len(data['shapes'])):
                ports_location = data['shapes'][i]['points']
                ports_list.append(ports_location)
        
       
            for i in range(len(data['shapes'])):
                x_lists=[]
                y_lists=[]
                obj_ports = ports_list[i]
                for port in obj_ports:
                    x_lists.append(port[0])
                    y_lists.append(port[1])
                x_max = sorted(x_lists)[-1]
                x_min = sorted(x_lists)[0]
                y_max = sorted(y_lists)[-1]
                y_min = sorted(y_lists)[0]

                width = x_max-x_min
                height = y_max-y_min

                u,v,_ = cv2.imread(os.path.join(args.data_dir,json_file.split('.')[0]+'.jpg')).shape
                
                center_x,center_y = round(float((x_min+width/2.0)/v),6),round(float((y_min+height/2.0)/u),6)

                f_width,f_height = round(float(width/v),6),round(float(height/u),6)

                label_id = str(id_list[data['shapes'][i]['label']])

                save_yolo_file(label_id,str(center_x),str(center_y),str(f_width),str(f_height),args.data_dir,json_path)

        else:
            pass

    for file in os.listdir(args.data_dir):

        b_name = ['png','jpg']
        
        dirs_path = os.path.join(os.path.abspath(os.path.join(args.data_dir, "../")),'yolo_data/images/train')
        dirs_path_val = os.path.join(os.path.abspath(os.path.join(args.data_dir, "../")), 'yolo_data/images/val')
        if os.path.exists(dirs_path):
            pass
        else: 
            os.makedirs(dirs_path)
            os.makedirs(dirs_path_val)

        
        if not os.path.exists(os.path.join(args.data_dir,file.split('.')[0]+'.'+'json')):
                              
                              
             file_name = os.path.join(dirs_path,file.split('.')[0]+'.txt')
             with open(file_name,'a+') as f:
                 pass
        if file.split('.')[-1] in b_name:
             shutil.copyfile(os.path.join(args.data_dir,file),os.path.join(dirs_path,file))
             
    get_train_or_val(args.data_dir)
    get_label_id(args.data_dir,id_list)
    print("save done!")


def make_id_list(src_path):
    json_list=[]
    id_list=[]
    for path in os.listdir(src_path):
        if path.split('.')[-1]=='json':
            json_list.append(os.path.join(src_path,path))
        else:
            pass
    for json_path in json_list:
        data = json.load(open(json_path))
        for i in range(len(data['shapes'])):
            label = data['shapes'][i]['label']
            id_list.append(label)
    id_list=list(set(id_list))

    index = range(len(id_list))

    id_dict = dict(zip(id_list,index))

    return id_dict

def save_yolo_file(id_name,x,y,w,h,path,json_path):
    dir_path = os.path.join(os.path.abspath(os.path.join(path,"../")),'yolo_data/labels/train/')
    dir_path_val = os.path.join(os.path.abspath(os.path.join(path, "../")), 'yolo_data/labels/val/')
    #pdb.set_trace()
    if os.path.exists(dir_path):
        pass
    else:
        os.makedirs(dir_path)
        os.makedirs(dir_path_val)

    txt_path = os.path.join(dir_path,os.path.basename(json_path).split('.')[0]+'.txt')

    with open(txt_path,'a+') as f:
        f.write(id_name+' '+x+' '+y+' '+w+' '+h+'\n')
    
    return 0

def get_train_or_val(path):
    Txt_path = os.path.join(os.path.abspath(os.path.join(path, "../"))+'/yolo_train.txt')
    for file_name in os.listdir(path):
        if file_name.split('.')[-1]=='jpg' or file_name.split('.')[-1]=='png':
            img_path = os.path.join(path,file_name)
            with open(Txt_path,'a+') as f:
                f.write(img_path+'\n')


def get_label_id(path,id_list):
    Txt_path = os.path.join(os.path.abspath(os.path.join(path, "../"))+'/names.txt')
    with open(Txt_path,'w') as f:
        atu = sorted(id_list.items(), key=lambda x: x[1], reverse=False )
        for ind in range(len(atu)):
            alist = list(atu[ind])
            print(alist[0])
            f.write(alist[0] + '\n')
        
        

def parseArguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir',type=str,
                        help='the path of the json file',default='labelme_images')
    return parser.parse_args(argv)
            
    
if __name__=='__main__':
   main(parseArguments(sys.argv[1:]))
