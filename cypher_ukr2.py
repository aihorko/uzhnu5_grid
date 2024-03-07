import random
import heapq
from collections import Counter

### --------------------------------------------------------------------------- ###
### Шифр Віженера

def vigenere_cipher(text, key, lang = "eng"):
  if (lang == "eng"):
    result = []
    key_repeated = (key * (len(text) // len(key) + 1))[:len(text)]
    for i in range(len(text)):
      char = text[i]
      if char.isalpha():
        shift = ord(key_repeated[i].lower()) - ord('a')
        if char.isupper():
          result.append(chr((ord(char) + shift - ord('A')) % 26 + ord('A')))
        else:
          result.append(chr((ord(char) + shift - ord('a')) % 26 + ord('a')))
      else:
        result.append(char)
  elif (lang == "ukr"):
    result = []
    key_repeated = (key * (len(text) // len(key) + 1))[:len(text)]
    for i in range(len(text)):
      char = text[i]
      if char.isalpha():
        shift = ord(key_repeated[i].lower()) - ord('а') # а - 1072 unicode
        if char.isupper():
          result.append(chr((ord(char) + shift - ord('Є')) % 44 + ord('Є'))) # Є - 1028 unicode
        else:
          result.append(chr((ord(char) + shift - ord('а')) % 40 + ord('а'))) # а - 1072 unicode
      else:
        result.append(char)
  else:
    return "Unsupported language - please use 'eng' or 'ukr'!\nНепідтримувана мова - будь ласка використовуйте 'eng' чи 'ukr'!"
  return ''.join(result)

def vigenere_decipher(text, key, lang = "eng"):
  if (lang == "eng"):
    result = []
    key_repeated = (key * (len(text) // len(key) + 1))[:len(text)]
    for i in range(len(text)):
      char = text[i]
      if char.isalpha():
        shift = ord(key_repeated[i].lower()) - ord('a')
        if char.isupper():
          result.append(chr((ord(char) - shift - ord('A')) % 26 + ord('A')))
        else:
          result.append(chr((ord(char) - shift - ord('a')) % 26 + ord('a')))
      else:
        result.append(char)
  elif (lang == "ukr"):
    result = []
    key_repeated = (key * (len(text) // len(key) + 1))[:len(text)]
    for i in range(len(text)):
      char = text[i]
      if char.isalpha():
        shift = ord(key_repeated[i].lower()) - ord('а') # а - 1072 unicode
        if char.isupper():
          result.append(chr((ord(char) - shift - ord('Є')) % 44 + ord('Є'))) # Є - 1028 unicode
        else:
          result.append(chr((ord(char) - shift - ord('а')) % 40 + ord('а'))) # а - 1072 unicode
      else:
        result.append(char)
  else:
    return "Unsupported language - please use 'eng' or 'ukr'!\nНепідтримувана мова - будь ласка використовуйте 'eng' чи 'ukr'!"
  return ''.join(result)


### --------------------------------------------------------------------------- ###
### Кодування Хафмена

class HuffmanNode:
  def __init__(self, char, freq):
    self.char = char
    self.freq = freq
    self.left = None
    self.right = None

  def __lt__(self, other):
    return self.freq < other.freq

def build_huffman_tree(text):
  frequency = Counter(text)
  #print(frequency.items())
  priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
  heapq.heapify(priority_queue)

  while len(priority_queue) > 1:
    left = heapq.heappop(priority_queue)
    right = heapq.heappop(priority_queue)

    merged_node = HuffmanNode(None, left.freq + right.freq)
    merged_node.left = left
    merged_node.right = right

    heapq.heappush(priority_queue, merged_node)

  return priority_queue[0], frequency

def build_huffman_codes(root, current_code, codes):
  if root is None:
    return

  if root.char is not None:
    codes[root.char] = current_code

  build_huffman_codes(root.left, current_code + "0", codes)
  build_huffman_codes(root.right, current_code + "1", codes)

def get_huffman_encoded(text, codes):
  return "".join([codes[char] for char in text])

def huffman_decode(encoded_text, root):
  current = root
  decoded_text = ""
  
  for bit in encoded_text:
    if bit == '0':
      current = current.left
    else:
      current = current.right

    if current.char:
      decoded_text += current.char
      current = root

  return decoded_text

def huffman_encode(text):
  root, frequency = build_huffman_tree(text)
  codes = {}
  build_huffman_codes(root, "", codes)

  encoded_bits = get_huffman_encoded(text, codes)
  return encoded_bits, root, codes, frequency


### --------------------------------------------------------------------------- ###
### Гамування XOR
def generate_xor_key(length):
  return [random.randint(0, 1) for _ in range(length)]

def xor_encrypt(message, key):
  chars = list(message)
  bits = [int(i) for i in chars]
  xor_bits = [m ^ k for m, k in zip(bits, key)]
  xor_message="".join([str(i) for i in xor_bits])
  return xor_message

def xor_decrypt(ciphertext, key):
  chars = list(ciphertext)
  bits = [int(i) for i in chars]
  xor_bits = [c ^ k for c, k in zip(bits, key)]
  xor_message="".join([str(i) for i in xor_bits])
  return xor_message


if __name__ == "__main__":
  ### ---------------------------------------------------------- ###
  ### Шифрування
  # ---- # Початковий текст англійською ('eng')
  initial_text = "To be, or not to be, that is the question,\nWhether 'tis nobler in the mind to suffer\nThe slings and arrows of outrageous fortune,\nOr to take arms against a sea of troubles,\nAnd by opposing end them? To die: to sleep;\nNo more;"
  vigenere_key = "Shakespeare"
  lang = "eng"
  print(f"\nПочатковий текст:\n\n{initial_text}\n\nКлюч для шифру Віженера:\n{vigenere_key}\n" )

  # ---- # Початковий текст українською ('ukr')
  initial_text = "Чи бути, чи не бути — ось питання.\nЩо благородніше? Коритись долі\nІ біль від гострих стріл її терпіти,\nА чи, зітнувшись в герці з морем лиха,\nПокласти край йому? Заснути, вмерти —\nІ все."
  vigenere_key = "Шекспір"
  lang = "ukr"
  print(f"\nПочатковий текст:\n\n{initial_text}\n\nКлюч для шифру Віженера:\n{vigenere_key}\n" )

  # ---- # Закодувати кодом Хафмена оригінальний текст без шифрування
  huffman_encoded_bits_2, huffman_root_2, codes_2, frequency_2  = huffman_encode(initial_text)
  print(frequency_2.items(), "\n")
  print(codes_2, "\n")
  print(f"\nЗакодовано кодом Хафмена:\n\n{huffman_encoded_bits_2}\n")

  # -1a- # Накласти шифр Віженера
  encrypted_text_vigenere = vigenere_cipher(initial_text, vigenere_key, lang)
  print(f"\nЗашифровано шифром Віженера):\n\n{encrypted_text_vigenere}\n")

  # -2a- # Закодувати кодом Хафмена
  huffman_encoded_bits, huffman_root, codes, frequency  = huffman_encode(encrypted_text_vigenere)
  print(frequency.items(), "\n")
  print(codes, "\n")
  print(f"\nЗакодовано кодом Хафмена:\n\n{huffman_encoded_bits}\n")

  # -3a- # Накласти гамування
  xor_key = generate_xor_key(len(huffman_encoded_bits))
  ciphertext = xor_encrypt(huffman_encoded_bits, xor_key)
  print(f"\nНакладено гамування:\n\n{ciphertext}\n")

  ### ---------------------------------------------------------- ###
  ### Розшифрування
  # -3b- # Зняти гамування
  decrypted_message = xor_decrypt(ciphertext, xor_key)
  print(f"\nЗнято гамування:\n\n{decrypted_message}\n")

  # -2b- # Розкодувати Хафмена
  huffman_dencoded = huffman_decode(decrypted_message, huffman_root)
  print(f"\nРозкодовано код Хафмена:\n\n{huffman_dencoded}\n")

  # -1b- # Розкодувати Віженера
  decrypted_text_vigenere = vigenere_decipher(huffman_dencoded, vigenere_key,lang)
  print(f"\nРозшифровано шифр Віженера:\n\n{decrypted_text_vigenere}")

  # ---- # Порівняти з початковим текстом
  print(initial_text == decrypted_text_vigenere)
  
  # ---- # Порівняти закодований віженера і розкодований хафмена
  print(encrypted_text_vigenere == huffman_dencoded)

  # ---- # Порівняти закодований Хафмена і розкодоване гамування
  print(huffman_encoded_bits == decrypted_message)
