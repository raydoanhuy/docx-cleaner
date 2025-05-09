import os
import re
from docx import Document

def clean_text(text):
    """Làm sạch văn bản: thay thế thông tin nhạy cảm."""
    # Thay tên khách hàng (giả sử tên là 2-4 từ tiếng Việt)
    text = re.sub(r'\b[A-ZÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪỬỮỰỲỴỶỸ\s]{2,20}\b', '[Tên Khách Hàng]', text)
    # Thay số CMND/CCCD (9 hoặc 12 số)
    text = re.sub(r'\b\d{9}(\d{3})?\b', '[Số CMND]', text)
    # Thay số điện thoại (10 số, định dạng Việt Nam)
    text = re.sub(r'\b0\d{9}\b', '[Số Điện Thoại]', text)
    # Thay email
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[Email]', text)
    return text

def process_docx_files(input_dir, output_file):
    """Xử lý tất cả file .docx trong input_dir, lưu kết quả vào output_file."""
    output_texts = []
    for filename in os.listdir(input_dir):
        if filename.endswith('.docx'):
            file_path = os.path.join(input_dir, filename)
            try:
                doc = Document(file_path)
                full_text = []
                for para in doc.paragraphs:
                    cleaned = clean_text(para.text)
                    if cleaned.strip():
                        full_text.append(cleaned)
                output_texts.append('\n'.join(full_text))
                print(f"Processed {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")
    if output_texts:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(output_texts))
        print(f"Saved output to {output_file}")
    else:
        print("No .docx files processed")

if __name__ == "__main__":
    input_dir = "legal_docs"
    output_file = "training_data.txt"
    process_docx_files(input_dir, output_file)
