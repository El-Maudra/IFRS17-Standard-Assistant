import openai


models = openai.OpenAI().models.list()

with open('models.txt', 'w') as f:
    model = f.write(str(models))
    f.close()

print (models)