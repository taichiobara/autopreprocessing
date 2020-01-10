
from flask import Flask, render_template, request,send_file,after_this_request


from icrawler.builtin import GoogleImageCrawler
import sys
import os
import zipfile
from io import BytesIO
import shutil
import time

#水増し用
import glob
import numpy as np
from keras.preprocessing.image import ImageDataGenerator,load_img, img_to_array, array_to_img,save_img
import cv2


app = Flask(__name__)


#render_templateを使って、htmlファイルを表示する。
#render_templateの第二引数以降に値を指定することで、index.htmlに値を渡す事ができる。
@app.route('/')
def hello():

    # s="abc"
    # lis=["a1","a2","a3"]
    # dic = {"name":"John", "age":24}
    # bl = True
    return render_template('hukuda.html')
    



# @app.route('/good')
# def good():
#     name = "Good"
#     return name


# @app.route('/test',methods=["GET","POST"])
# def test():
#     if request.method=="GET":
#         res =request.args.get('test')
#     elif request.method=="POST":
#         res =request.form['test']
#     return res


# @app.route('/test',methods=["GET","POST"])
# def test():
    
#     query =request.form['query']
#     num=request.form['num']
#     crawler = GoogleImageCrawler(storage = {"root_dir" : query+"folder"})
#     crawler.crawl(keyword = query , max_num = int(num))
#     path = os.path.abspath(__file__)
#     dir = query+"folder"
#     data_files = os.listdir(dir)
#     memory_file = BytesIO() 
#     with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf: # 圧縮する
#         os.chdir(dir) # データ格納ディレクトリへ移動
#         for individualFile in data_files:
#             print('データファイル圧縮: ' + individualFile)
#             zf.write(individualFile)
#     memory_file.seek(0)
#     time.sleep(3)
#     @after_this_request
#     def remove_file(response):
#         try:

#             shutil.rmtree(dir)
#         except Exception as error:
#             app.logger.error("Error removing or closing downloaded file handle", error)
#         return response

#     return send_file(memory_file, attachment_filename=query+'.zip', as_attachment=True)


@app.route('/preprocessing',methods=["GET","POST"])
def mizumashi():
    query =request.form['query']
    num=int(request.form['num'])
    size=int(request.form["size"])
    mizumashiselct=int(request.form["mizumashiselct"])
    kakeru=int(request.form["kakeru"])
    tate1=int(request.form["tate1"])
    yoko1=int(request.form["yoko1"])

    rr=int(request.form["rr"])
    wsr=int(request.form["wsr"])
    sr=int(request.form["sr"])
    hsr=int(request.form["hsr"])
    zr=int(request.form["zr"])
    csr=int(request.form["csr"])

    crawler = GoogleImageCrawler(storage = {"root_dir" : query+"folder"})
    crawler.crawl(keyword = query , max_num = int(num))

    # path = os.path.abspath(__file__)
    dir = query+"folder"
    
    data_files = os.listdir(dir)
    #images = glob.glob(os.path.join(dir, "*.jpg"))

    datagen = ImageDataGenerator(rotation_range=rr,
                            width_shift_range=wsr,
                            shear_range=sr,
                            height_shift_range=hsr,
                            zoom_range=zr,
                            horizontal_flip=True,
                            fill_mode="nearest",
                            channel_shift_range=csr)

    if mizumashiselct==1:
        for i in range(len(data_files)):
            img = load_img(dir+"/"+data_files[i])
            #img = img.resize((tate1,yoko1 ))
            x = img_to_array(img)
            x = np.expand_dims(x, axis=0)

            save_name = 'extened-' + str(i)
            output_dir = dir

            g = datagen.flow(x, batch_size=1, save_to_dir=output_dir,
                        save_prefix=save_name, save_format='jpeg')
            for i in range(kakeru):
                bach = g.next()
                

    next_data_files = os.listdir(dir)
    if size==1:
        for i in range(len(next_data_files)):
            img = load_img(dir+"/"+next_data_files[i])
            img = img.resize((tate1,yoko1 ))
            x = img_to_array(img)
            save_img(dir+"/"+next_data_files[i], x)



    memory_file = BytesIO() 
    with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf: # 圧縮する
        os.chdir(dir) # データ格納ディレクトリへ移動
        for individualFile in next_data_files:
            print('データファイル圧縮: ' + individualFile)
            zf.write(individualFile)
    memory_file.seek(0)
    #time.sleep(3)
    @after_this_request
    def remove_file(response):
        try:
            shutil.rmtree(dir)
        except Exception as error:
            app.logger.error("Error removing or closing downloaded file handle", error)
        return response

    return send_file(memory_file, attachment_filename=query+'.zip', as_attachment=True)
    
    
    

    

## おまじない
if __name__ == "__main__":
    app.run(debug=True)