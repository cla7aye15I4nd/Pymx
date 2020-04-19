class DataBlock:
    def __init__(self, name, value=0):
        self.name = name
        self.value = value

    def __str__(self):
        text = f'{self.name}:\n'
        text += f'  .word {self.value}\n'
        return text

def build_data(data, args):
    data_block = DataBlock(data.name, data.value)
    return data_block