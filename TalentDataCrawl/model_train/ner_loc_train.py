import spacy
from spacy.util import minibatch, compounding
import random
import ast
from spacy.gold import GoldParse
from spacy.scorer import Scorer
import os


def evaluate(nlp, examples, ent='LOC'):
    scorer = Scorer()
    for input_, annot in examples:
        text_entities = []
        for entity in annot.get('entities'):
            if ent in entity:
                text_entities.append(entity)
        doc_gold_text = nlp.make_doc(input_)
        gold = GoldParse(doc_gold_text, entities=text_entities)
        pred_value = nlp(input_)
        scorer.score(pred_value, gold)
    return scorer.scores


def get_data_train_from_paths(paths):
    data = []
    for path in paths:
        with open(path, "r", encoding="UTF-8") as f:
            lines = f.readlines()
            for line in lines:
                line = line[:-1]
                tuple_data = ast.literal_eval(line)
                data.append(tuple_data)
    return data


def train_spacy_ner(model, data, iterations):
    if model is not None:
        nlp = spacy.load(model)
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('vi')  # create blank Language class
        print("Created blank 'vi' model")
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner, last=True)
    else:
        ner = nlp.get_pipe('ner')

    for _, annotations in data:
        for entity in annotations.get('entities'):
            ner.add_label(entity[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only extract_xpath NER
        if model is None:
            optimizer = nlp.begin_training()
        else:
            # optimizer = nlp.resume_training()
            optimizer = nlp.entity.create_optimizer()
        for itn in range(iterations):
            print("Statring iteration " + str(itn))
            random.shuffle(data)
            split = int(len(data) * 5/6)
            training_data = data[:split]
            test_data = data[split + 1:]

            losses = {}
            batches = minibatch(training_data, size=compounding(2000, 5000., 1.5))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, drop=0.35,
                           losses=losses)
            print('Losses:', losses)
            print('Score:', evaluate(nlp, test_data))

    return nlp


# paths = ["data_province_train.txt",
#          "data_city_train.txt"]
dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = os.path.join(dir_path, 'data_train')
files = ["data_loc_train.txt"]
paths = [os.path.join(dir_path, file) for file in files]
train_data = get_data_train_from_paths(paths)
prd_nlp = train_spacy_ner("model/loc_ner", train_data, 1)

# Save our trained Model
model_file = input("Enter your Model Name: ")
prd_nlp.to_disk("model/"+model_file)

# # Test your textt
# test_text = input("Enter your testing text: ")
# doc = prdnlp(test_text)
# for ent in doc.ents:
#     print(ent.text, ent.start_char, ent.end_char, ent.label_)