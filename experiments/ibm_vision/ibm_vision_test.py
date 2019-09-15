import json
from watson_developer_cloud import VisualRecognitionV3

visual_recognition = VisualRecognitionV3(
    '2018-03-19',
    iam_apikey='GfBGcjYPrd-38OXXTbV1uPjKZ5Xp4o-20av0onxqqUIF')

url = 'https://watson-developer-cloud.github.io/doc-tutorial-downloads/visual-recognition/640px-IBM_VGA_90X8941_on_PS55.jpg'

classes_result = visual_recognition.classify(url=url).get_result()
print(json.dumps(classes_result, indent=2))
