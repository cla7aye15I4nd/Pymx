class DataBlock:
    def __init__(self, name, value=0):
        self.name = name
        self.value = value

    def __str__(self):
        if type(self.value) is str:
            text = f'{self.name}.size:\n'
            text += f'  .word {len(self.value)}\n'     
            text += f'{self.name}.data:\n'
            text += f'  .asciz "{self.value}"\n'
            text += f'{self.name}:\n'
            text += f'  .word {self.name}.data\n'            
        else:
            text = f'{self.name}:\n'
            text += f'  .word {self.value}\n'
        return text

def build_data(data, args):
    data_block = DataBlock(data.name, data.value)
    return data_block