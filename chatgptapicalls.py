from openai import OpenAI 
import os
import base64
import fitz


MODEL="gpt-4o"
client = OpenAI(api_key='API_KEY_HERE')

OUTPUT_FILE = 'OUTPUT_FILE_PATH'
FOLDER_PATH = 'INPUT_FILE_PATH'

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def transcribe_image(image_path):
    base64_image = encode_image(image_path)
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that responds in Markdown. Help me with my math homework!"},
            {"role": "user", "content": [
                {"type": "text", "text": "Can you extract the text from this file formatted as a gold standard for digital humanities, meaning it is cleaned of page breaks, end-of-line hyphens, headers, and extraneous content. preserve the paragraphs and original structure as much as possible. Do not add any comments in your response. Be sure to remove the headers."},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}
                }
            ]}
        ],
        temperature=0.0,
    )
    return response.choices[0].message.content


def process_pdf(pdf_path, output_file):
    document = fitz.open(pdf_path)
    transcriptions = []

    for page_num in range(len(document)):
        page = document.load_page(page_num)
        pix = page.get_pixmap()
        image_path = f"page_{page_num + 1}.png"
        pix.save(image_path)

        transcription = transcribe_image(image_path)
        transcriptions.append(transcription)

        # Remove the temporary image file
        os.remove(image_path)

    # Combine the transcriptions into one text
    combined_text = "\n".join(transcriptions)

    # Write the combined text to the output file
    with open(output_file, 'w') as f:
        f.write(combined_text)

    print(f"Transcriptions saved to {output_file}")


# Example usage
process_pdf('/home/sam/Desktop/Scriptie/Programma/test/The_Method_to_Science_chapter3.pdf', OUTPUT_FILE)