import hashlib

#seed phrase separata da spazi
seed_phrase = "hobby spend slam element elder liar lucky speak insane vital vehicle thunder appear dune despair steak lunar develop letter useless spoil top fan ?"

#converto la stringa in una lista
seed_phrase_list = seed_phrase.split(" ")
print("Seed Phrase senza l'ultima parola: ")
print(seed_phrase_list)

#apro il file english.txt
english = open("english.txt")
#leggo il file e lo trasformo in una lista
word_list = english.read().split("\n")
#chiudo il file
english.close()

#converte la seed phrase nell'indice della word_list
seed_phrase_index = []
for word in seed_phrase_list:
    if(word != "?"):
        index = word_list.index(word)
        seed_phrase_index.append(index)
    else:
        seed_phrase_index.append(word)
print("Indice parole della Seed Phrase: ")
print(seed_phrase_index)

#converte l'indice in binario
seed_phrase_binary = []
for number in seed_phrase_index:
    if(number != "?"):
        seed_phrase_binary.append(format(number, "011b"))
    else:
        seed_phrase_binary.append(number)
print("Indice convertito in binario a 11 bit: ")
print(seed_phrase_binary)

#calcolo del numero di bits mancanti
num_missing_bits = int(11-(1/3)*(len(seed_phrase_list)))
print("Numero bits mancanti: " + str(num_missing_bits))

#calcolo di tutte le permutazione possibili dei bit mancanti
missing_bits_possibile = []
for x in range (2**num_missing_bits):
    missing_bits_possibile.append(bin(x)[2:].rjust(num_missing_bits, "0"))
print("Permutazioni possibili dei " + str(num_missing_bits) + " bits mancanti")
print(missing_bits_possibile)

#combina la rappresentazione binaria della seed phrase con ogni possibile bit mancante per ottenere la possibile entropia
entropy_possible = []
for bits in missing_bits_possibile:
    entropy_possible.append("".join(seed_phrase_binary[:-1])+bits)
print("Rappresentazione binaria della seed phrase con ogni possibile combinazione di " + str(num_missing_bits) + " bits mancanti")
print(entropy_possible)

#calcolo checksum con la funzione SHA256 della libreria hashlib
checksum = []
for entropy in entropy_possible:
    entropy_int = int(entropy, 2)
    entropy_bytes = entropy_int.to_bytes(len(entropy) // 8, byteorder="big")
    sha256_hash = hashlib.sha256(entropy_bytes).digest()
    checksum_bits = format(sha256_hash[0], "08b")
    checksum.append(checksum_bits[:11 - num_missing_bits])
print("Calcolo della checksum dalle possibili combinazioni precedenti: ")
print(checksum)

#combino i bits mancanti con il suo corrispondente checksum
last_word_bits = []
for missing_bits, checksum_bit in zip(missing_bits_possibile, checksum):
    combined_bits = missing_bits + checksum_bit
    last_word_bits.append(combined_bits)
print("Combinazione dei bits mancanti con il corrispondente checksum: ")
print(last_word_bits)

#trasformo nella corrispondente parola
last_word = []
for bits in last_word_bits:
    last_word.append(word_list[int(bits, 2)])
print("Parole corrispondenti alle combinazione precedenti: ")
print(last_word)

#scrivo le possibili combinazioni su un file txt
file = open("seedphrase.txt", "w")
index = seed_phrase_list.index("?")
for word in last_word:
    seed_phrase_list[index] = word
    for item in seed_phrase_list:
        file.write(item+" ")
    file.write("\n")
file.close()
print("Le possibili Seed Phrase di ripristino sono state salvate sul file seedphrase.txt")
