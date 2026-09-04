def create_chunks(text, chunk_size=500, overlap=50):
    paragraphs = text.split("\n\n")

    chunks = []
    current_chunk = ""

    for paragraph in paragraphs:
        paragraph = paragraph.strip()

        if not paragraph:
            continue

        if len(current_chunk) + len(paragraph) <= chunk_size:
            current_chunk += paragraph + "\n\n"
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())

            # Keep some previous text as overlap
            overlap_text = current_chunk[-overlap:] if current_chunk else ""

            current_chunk = overlap_text + paragraph + "\n\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks