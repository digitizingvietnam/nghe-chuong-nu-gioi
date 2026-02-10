# Đờn-bà AI Chatbot

## Overview

An AI-powered chatbot that recreates the voices of Vietnamese female writers from _Nữ Giới Chung_ (Women's Bell), a pioneering newspaper from 1918. This project combines historical preservation with modern AI to provide an interactive experience exploring early feminist perspectives and women's rights in colonial Vietnam.

## Feature Highlights

- **Historical Authenticity**: Built from OCR-processed content of 20 volumes of _Nữ Giới Chung_ with proper source citations
- **Period-Accurate Language**: Replicates early 20th-century Vietnamese writing style and vocabulary
- **RAG Architecture**: Uses Retrieval-Augmented Generation for factually grounded responses from historical documents
- **Modern Model AI**: Powered by GPT-4o for optimal performance and cultural accuracy

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python web framework)
- **AI/ML**:
  - LangChain for RAG orchestration
  - OpenAI GPT-4o and embeddings
  - Chroma vector database
- **Data Processing**: ClaudeAI for OCR, custom Python scripts

## Technical Description

### Architecture

The chatbot uses a Retrieval-Augmented Generation (RAG) pipeline:

```
User Query → Flask Server → Vector Search (Chroma) → Context Retrieval →
GPT-4o Processing → Response Generation → User Interface
```

### Key Components

1. **Data Pipeline** (`populate_database.py`): Processes OCR documents, generates embeddings, and populates the Chroma vector database
2. **RAG Engine** (`utils/rag.py`): Handles query processing, semantic search, context assembly, and response generation
3. **Embeddings** (`utils/embedding.py`): Manages vector embeddings for documents and queries
4. **Web Interface** (`main.py`): Flask REST API with session management and message streaming

### How It Works

- Historical documents are chunked and embedded into a vector database
- User queries trigger semantic search to find relevant historical passages
- Retrieved context + conversation history is sent to GPT-4o
- The model generates responses in 1918 Vietnamese writing style with source citations

## Installation

### Prerequisites

- Python 3.8+
- pip and Git

### Setup Steps

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/nghe-chuong-nu-gioi.git
cd nghe-chuong-nu-gioi
```

2. **Create and activate virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Configure API keys**

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

**Get API Keys:**

- OpenAI: [platform.openai.com](https://platform.openai.com/) → API Keys

5. **Initialize the database**

```bash
python populate_database.py
```

_Note: This may take 10-15 minutes_

6. **Run the application**

```bash
python main.py
```

7. **Access at** `http://localhost:5000`

## Example Usage

**Women's Rights**

```
User: Bàn về nữ quyền?

Chatbot: Bàn về nữ quyền, trong bài viết "Trách nhiệm người đờn bà" của tác giả Trần-thị-Đào, được đăng trên số báo 3, ngày 22 tháng 2 năm 1918, có nêu rõ rằng phụ nữ cần có một thế lực riêng để không phụ thuộc hoàn toàn vào nam giới. Tác giả khuyến khích chị em phụ nữ nên trau dồi nghề nghiệp và học thức để tự tạo cho mình một vị trí độc lập trong xã hội. Điều này không chỉ giúp phụ nữ hỗ trợ gia đình mà còn góp phần giảm bớt gánh nặng cho người đàn ông. Tác giả nhấn mạnh: "Thế thì chị em ta, phận đờn-bà yếu-ớt, nghĩ có nên kiếm một cái thế lực gì riêng chăng, dầu đến chơn nghịch cảnh có đũ sức đứng-đợt mộ mình, không nương dựa vào đâu, mà cũng không xiêu ngã." Qua đó, có thể thấy rõ tinh thần nữ quyền thời kỳ đầu, khi phụ nữ bắt đầu nhận thức được vai trò quan trọng của mình trong gia đình và xã hội, và khao khát một sự bình đẳng thực sự với nam giới.
```

**Education**

```
User: Giáo dục phụ nữ quan trọng như thế nào?

Chatbot: Giáo dục phụ nữ giữ vai trò vô cùng quan trọng. Trước hết, như tác giả Nữ-sanh Thu-cúc đã nhấn mạnh trong bài "Chị dạy em luân-lý" (Số báo 5, Ngày 8 tháng 3 năm 1918), học hành không chỉ là để hiểu biết mà còn là nền tảng cho vai trò làm mẹ trong tương lai. Nếu không được học, chúng ta sẽ khó lòng làm tốt vai trò của mình trong gia đình và xã hội. Hơn nữa, bài viết "Trách nhiệm người đờn bà" của Trần-thị-Đào (Số báo 3, Ngày 22 tháng 2 năm 1918) cũng khẳng định rằng việc sở hữu một thế lực riêng bằng tri thức và nghề nghiệp sẽ giúp phụ nữ có khả năng tự lập hơn, không phụ thuộc vào đàn ông, và hơn hết là có thể hỗ trợ gia đình về mặt kinh tế, làm nhẹ bớt gánh nặng cho chồng con. Cuối cùng, Mademoiselle LIÊU trong bài viết không tựa (Số báo 3, Ngày 22 tháng 2 năm 1918) đã chỉ ra rằng việc học hỏi không chỉ giúp nâng cao tri thức mà còn giúp chúng ta hiểu rõ hơn về những giá trị truyền thống và hiện đại, từ đó xây dựng nên một xã hội bình đẳng và hòa thuận. Qua những ý kiến này, ta thấy rằng giáo dục không chỉ mang lại tri thức mà còn là chìa khóa để phụ nữ khẳng định vị thế của mình và đóng góp cho xã hội.
```

**Social Issues**

```
User: Bàn về nữ công gia chánh?

Chatbot: Kính thưa quý độc giả, Trong các bài viết được trích dẫn từ báo *Nữ giới chung* năm 1918, có một số thông tin liên quan đến vai trò của nữ giới trong việc quản lý gia đình và trách nhiệm đối với gia đình. Bài viết của tác giả Mademoiselle LIÊU, ngày 22 tháng 2 năm 1918, nhấn mạnh rằng phụ nữ cần rèn luyện đức hạnh, công dung ngôn hạnh để có thể đảm đương trách nhiệm trong gia đình cũng như ngoài xã hội. Tác giả Trần-thị-Đào cũng bàn về trách nhiệm của người phụ nữ, khuyến khích chị em phụ nữ tìm kiếm một thế lực riêng để tự chủ hơn trong mọi hoàn cảnh. Bà viết: "Thế thì chị em ta, phận đờn-bà yếu-ớt, nghĩ có nên kiếm một cái thế lực gì riêng chăng, dầu đến chơn nghịch cảnh có đũ sức đứng-đợt mộ mình, không nương dựa vào đâu, mà cũng không xiêu ngã." (Trần-thị-Đào, ngày 22 tháng 2 năm 1918). Những bài viết này cho thấy vai trò của nữ công gia chánh không chỉ dừng lại ở việc nội trợ mà còn bao hàm trách nhiệm lớn lao hơn trong việc giữ gìn và phát triển gia đình, tạo dựng một vị thế độc lập cho người phụ nữ. Trân trọng, Một cây viết nữ của báo *Nữ giới chung*, năm 1918.
```

## Project Structure

```
NGHE-CHUONG-NU-GIOI/
├── chroma/               # Chroma vector database
├── data/                 # Historical OCR documents
├── static/               # Frontend assets (CSS, JS, images)
├── templates/            # HTML templates
├── utils/                # Core utilities
│   ├── embedding.py      # Embedding management
│   └── rag.py            # RAG implementation
├── main.py               # Flask application
├── populate_database.py  # Database initialization
├── query_data.py         # Data querying
└── requirements.txt      # Dependencies
```
