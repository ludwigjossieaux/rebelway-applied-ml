import hou
import sys
sys.path.append(r"E:/repos/rebelway-applied-ml/w03/assignment")
from importlib import reload
import classifier_utils
reload(classifier_utils)

def predict():
   image_path = hou.parm('image').eval()
   utils = classifier_utils.ClassifierUtils()
   predicted = utils.predict(image_path)
   print(predicted)