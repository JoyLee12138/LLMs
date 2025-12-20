import re

#固定长度baseline
def fixed_chunk(text, chunk_size=300, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks


#递归切分(结构感知),先按照段落分，如果段落太长，在段落里面再按照。.?!切分
def recursive_chunk(text, max_len=500):
    paragraphs = text.split("\n\n")
    chunks = []

    for p in paragraphs:
        if len(p) <= max_len:
            chunks.append(p)
        else:
            sentences = re.split(r'(?<=[。.!?])', p)
            buf = ""
            for s in sentences:
                if len(buf) + len(s) <= max_len:
                    buf += s
                else:
                    chunks.append(buf)
                    buf = s
            if buf:
                chunks.append(buf)
    return chunks



#语义切分，假设是markdown/README
def semantic_chunk_md(text):
    chunks = []
    current = ""
    for line in text.splitlines():
        if line.startswith("## "):
            if current:
                chunks.append(current)
            current = line + "\n"
        else:
            current += line + "\n"
    if current:
        chunks.append(current)
    return chunks



