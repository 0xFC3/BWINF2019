# read text document
f = open('nummern.txt', 'r')
numbers = []
for line in f:
    numbers.append(line[:-1])

def split_number_in_blocks(number):
    ib = 0
    ie = 1
    blocks = []
    # split number into blocks which always end on a 0 (except for the last one)
    for i in range(len(number)):
        if i != 0:
            if number[i] != '0' and i != len(number)-1:
                ie += 1
            else:
                ie += 1
                blocks.append(number[ib: ie])
                ib = ie
                ie = ib
    # find out the blocks which only consist of one number
    indexes = []
    for i in range(len(blocks)):
        if len(blocks[i]) == 1:
            indexes.append(i)
    # append these blocks to the blocks before them
    for index in indexes[::-1]:
        blocks[index - 1] = blocks[index - 1] + blocks[index]
        del blocks[index]
    # devide the too big blocks into blocks of 4 and when fill up with one block of 2 or 3 or both
    split = []
    for block in blocks:
        if len(block) <= 4:
            split.append(block)
        else:
            p = []
            while len(block) > 5:
                p.append(block[-4:])
                block = block[:-4]
            if len(block) == 5:
                p.append(block[-3:])
                p.append(block[:2])
            else:
                p.append(block)
            p.reverse()
            for item in p:
                split.append(item)
    return split
if __name__ == '__main__':
    for number in numbers:
        print(split_number_in_blocks(number))




