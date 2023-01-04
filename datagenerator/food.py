# import standard modules
import os
import random
import datetime as dt
# data_pool


class FoodTextDataLoader:

     def __init__(self):
         pass


     
class FoodTextGenerator:

    CONCAT_WORDS = ["und", "ähm", "err", " ", "außerdem noch", "sowie", ","]

    def __init__(self):
        self.products = self.read_from_data_pool("data_pool/products.txt")
        self.measures = self.read_from_data_pool("data_pool/measures.txt")

    @classmethod
    def read_from_data_pool(cls, path: str) -> list:
        return open(path, "r").read().split()

    def concat_word(self):
        return random.choice(self.CONCAT_WORDS)

    def create_random_product_entity(self):
        return {
            "P-LOC": random.choice(self.products),
            "M-LOC": random.choice(self.measures),
            "A-LOC": str(random.randint(1, 1000))
        }

    def sentence_blueprint(self):
        return random.choice(["ich mische", "dazu kommen noch", "hinzu kommen", "", "es kommen noch rein", "dazu"])

    def generate_random_sentence(self, params):
        sentences = list()
        targets = list()
        keys = ["P-LOC", "A-LOC", "M-LOC"]
        for ix, entity in enumerate(params):
            reversed_entity = dict(zip(entity.values(), entity.keys()))
            random.shuffle(keys)
            sentence = " ".join([
                self.sentence_blueprint().lower(),
                entity[keys[0]].lower(),
                entity[keys[1]].lower(),
                entity[keys[2]].lower(),
                random.choice(self.CONCAT_WORDS).lower() if ix < len(params) else ""
            ])
            target = [str(0) if x not in list(reversed_entity.keys()) else reversed_entity[x] for x in sentence.split()]
            sentences.append(sentence)
            targets += target

        sentences = " ".join(sentences)
        return sentences.split(), targets


    def generate_random_parameters(self):
        # [{product: x, amount: y, measure: z},...]
        targets = list()
        amount_entity = random.randint(0, 4)
        if amount_entity == 0:
            # TODO: add random sentence
                sentence = "hello there"
                target = "0 0"
        else:
            for count in range(amount_entity):
                targets.append(self.create_random_product_entity())
                sentence, target = self.generate_random_sentence(targets)

        return target, sentence

    def write_data_samples_out(self, data, path_name: str = ""):
        if path_name == "":
            path_name = f"data_{str(dt.datetime.now().date())}"

        with open(os.path.join(os.getcwd(), "output", path_name), "w") as out_file:
            for sample in data:
                sample_length = len(sample[0])
                for i in range(sample_length):
                    out_file.write(f"{sample[1][i]} {sample[0][i]}\n")
                    if i == sample_length-1:
                        out_file.write("\n")

            out_file.close()

    def create(self, n: int = 10, write_out: bool = True, out_path: str = ""):
        data = list()
        for n in range(n):
            data.append(self.generate_random_parameters())

        if write_out:
            self.write_data_samples_out(data, path_name=out_path)



fg = FoodTextGenerator()
fg.create()
