import cv2
import numpy as np
import tensorflow as tf

new_model=tf.keras.models.load_model('blog\cnn.h5')
tmp_images=cv2.imread('./asdf.jpg',cv2.IMREAD_GRAYSCALE)
img_input=tmp_images.copy()

img=cv2.cvtColor(img_input,cv2.COLOR_GRAY2RGB)
img_rgb=img.copy()
img_rgb=(img_rgb/255.).astype(np.float32)
img_lab=cv2.cvtColor(img_rgb,cv2.COLOR_RGB2Lab)

img_1=img_lab[:,:,0]
input_img=cv2.resize(img_1,(28,28))
input_img-=50
test=[]
test.append(input_img)
test=np.array(test)
idx=np.argmax(new_model.predict(test)[0])
car_dict={0:'K9',1:'carnival',2:'santafe',3:'sportage'}
print(car_dict[idx])