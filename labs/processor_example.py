import json
import logging
from copy import deepcopy

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s %(message)s', level=logging.ERROR)


class Processor(object):
    """Processor interface
    """

    def __init__(self):
        self.num_processed = 0
        self.num_skip = 0
        self.name = self.__class__.__name__
        self.log = logging.getLogger(self.name)
        self.log.setLevel(logging.INFO)

    def process(self, item):
        raise NotImplementedError

    def stats(self):
        """return statistics of processor
        """
        return {
            'num_processed': self.num_processed,
            'num_skip': self.num_skip
        }


class ProcessorStage1(Processor):

    def process(self, item):
        self.num_processed += 1
        new_item = deepcopy(item)
        new_item['field1'] = 'processed field1 ' + new_item['name']
        return new_item


class ProcessorStage2(Processor):

    def process(self, item):
        self.num_processed += 1
        new_item = deepcopy(item)
        new_item['field2'] = 'processed field2 ' + new_item['name']
        return new_item


class ProcessorPipeline:

    def __init__(self):
        proc1 = ProcessorStage1()
        proc2 = ProcessorStage2()


        self.processors = [
            proc1,
            proc2
        ]

    def process(self, item):
        for proc in self.processors:
            item = proc.process(item)
        return item

    def stats(self):
        """return statistics of processor
        """
        stats = {}
        for proc in self.processors:
            stats[proc.name] = proc.stats()
        return stats


def main():
    pipeline = ProcessorPipeline()

    # create some items for example
    items = []
    for i in range(5):
        item = {
            'id': i,
            'name': 'item_%s' % i
        }
        items.append(item)

    # call pipeline to process all items
    processed_items = []
    for item in items:
        new_item = pipeline.process(item)
        processed_items.append(new_item)

    print('Items after processing:')
    for item in processed_items:
        print(json.dumps(item, indent=2))

    # print out
    print()
    print('Pipeline stats:\n', json.dumps(pipeline.stats(), indent=2))


if __name__ == '__main__':
    main()
