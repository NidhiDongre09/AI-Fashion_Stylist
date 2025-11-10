import cohere

# replace YOUR_KEY_HERE with your actual Cohere API key
co = cohere.Client("zU5U61D2YLSMwvwiy4GmHoLJNbr3RiL0Iuu30SQT")

models = co.models.list()
print("Available models:")
for m in models.models:
    print("-", m.name)
