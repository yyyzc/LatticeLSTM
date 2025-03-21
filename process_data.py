import json

file = "ResumeNER/dev.char.bmes"

lines = []
with open(file, 'r', encoding='utf-8') as f:
    lines.extend(f.readlines())

train_data = []
train_item = {}
entity_set = set()
entity_map = {
    'CONT': 'country',
    'RACE': 'race',
    'NAME': 'name',
    'PRO': 'profession',
    'LOC': 'address',
    'ORG': 'organization',
    'EDU': 'education',
    'TITLE': 'job'
}
entity = ['', '']


for line in lines:
    if line == '\n':
        train_data.append(train_item)
        train_item = {}
        continue
    token, label = line.strip('\n').split(' ')
    train_item['tokenized_text'] = train_item.get('tokenized_text', '') + token
    label_parts = label.split('-')

    if label == 'O':
        continue

    pos = label_parts[0]
    type = label_parts[1]
    if pos == 'B':
        entity_set.add(label.split('-')[-1])
        entity[0] = token
        entity[1] = type
    elif pos == 'M':
        entity[0] += token
    elif pos == 'E':
        entity[0] += token
        train_item['entities'] = train_item.get('entities', []) + [{
            'entity': entity[0],
            'types': [entity_map[entity[1]]]
        }]
        entity = ['', '']

print(train_data[:10])
print(entity_set)

with open('resume_dev.json', 'w', encoding='utf-8') as f:
    json.dump(train_data, f, ensure_ascii=False)