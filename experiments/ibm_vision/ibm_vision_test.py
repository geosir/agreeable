import json
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='GfBGcjYPrd-38OXXTbV1uPjKZ5Xp4o-20av0onxqqUIF')

# url = 'https://watson-developer-cloud.github.io/doc-tutorial-downloads/visual-recognition/640px-IBM_VGA_90X8941_on_PS55.jpg'
url = "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5d/Leopard_2_A7.JPG/220px-Leopard_2_A7.JPG"
classes_result = visual_recognition.classify(url=url).get_result()
print(json.dumps(classes_result, indent=2))
maxscore, maxind = 0, 0
for i in range(len(classes_result["images"][0]["classifiers"][0]["classes"])):
    if classes_result["images"][0]["classifiers"][0]["classes"][i]["score"] > maxscore:
        maxscore = classes_result["images"][0]["classifiers"][0]["classes"][i]["score"]
        maxind = i
print(classes_result["images"][0]["classifiers"][0]["classes"][maxind])
