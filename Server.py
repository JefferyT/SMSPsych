from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from google.cloud import automl_v1beta1 as automl
import os

# pip install --upgrade google-cloud-language
# pip install virtualenv
# pip install google-cloud-automl

class server:
    # sets up authentication and clients
    def __init__(self):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'UnderTheRadar-c390bfc73739.json'
        text = 'The turtle is cute and the rabbit is ugly'
        client = language.LanguageServiceClient()
        clientML = automl.TablesClient(project='undertheradar', region='us-central1')

    # takes a natural language client and text to be analyzed
    # returns an array of
    # 0 - sentiment value
    # 1-3 - top three topics, if there are not enough topics it will fill with NULL
    def sentimentValue(self, client, t):
        document = types.Document(content=t, type=enums.Document.Type.PLAIN_TEXT, language="en")
        score = client.analyze_sentiment(document).document_sentiment.score
        text = list()
        text.append(score)
        i = 0;
        for e in client.analyze_entity_sentiment(document).entities:
            if (i > 2):
                break
            text.append(e.name.replace(",", ""))
            i += 1
        for j in range(3 - i):
            text.append("NULL")
        return text

    # takes a autoML client and inputs in the form of a list
    # returns a dictionary of conditions to score
    def predict(self, clientML, inputs):
        response = clientML.predict(
            model_display_name='OhBoyHesABigOne',
            inputs=inputs)
        # print("Prediction results:")
        conditions = {}
        for result in response.payload:
            conditions[result.tables.value.string_value] = result.tables.score;
            # print(str(result.tables.score) + " " + result.tables.value.string_value)
        return conditions


# print(server.sentimentValue(server,client, text)[0])
# print(server.predict(server,clientML, inputs))
