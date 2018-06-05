from collections import  namedtuple
import json
def main():
    Sample=namedtuple('Sample','name score size')
    sample=Sample('dialog',33.33,4)
    with open('./data/data.json','w') as f:
        f.write(json.dumps(sample._asdict()))

    print(sample)

if __name__=='__main__':
    main()
