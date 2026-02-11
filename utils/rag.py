"""
rag.py

Core Retrieval-Augmented Generation (RAG) logic.

This module performs the following steps:
1. Loads a vector database (Chroma or Pinecone)
2. Performs semantic similarity search
3. Constructs a prompt using retrieved context
4. Invokes a large language model to generate a response

This module can be used by:
- Command-line scripts
- Web APIs (Flask/FastAPI)
"""

from dotenv import load_dotenv
import os
from pinecone import Pinecone
from utils.embedding import get_embedding_function
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain_chroma import Chroma

load_dotenv()

# Pinecone configuration
PINECONE_INDEX_NAME = os.getenv("PROJECT_INDEX_NAME")
PROJECT_NAMESPACE = os.getenv("PROJECT_NAMESPACE")

PROMPT_TEMPLATE = """
Trả lời theo ngôn ngữ giống thông tin dưới đây:

{context}

---
Hãy trả lời câu hỏi dựa vào thông tin trong dữ liệu trên: {question}.

Khi tìm thông tin, **không giới hạn ở việc khớp từ ngữ nguyên văn**. 
Hãy **xem xét và suy luận các từ hoặc khái niệm đồng nghĩa, gần nghĩa, hoặc cùng trường nghĩa**.
Ví dụ (nhưng không giới hạn):
- “vợ chồng”, “phu thê”, “kết hôn”, “lập gia đình”, “đạo vợ chồng”
- “đàn bà”, “phụ nữ”, “nữ giới”, “đờn bà”
- “bổn phận”, “trách nhiệm”, “nghĩa vụ”

Nếu nội dung câu hỏi **về mặt ý nghĩa** có liên quan đến thông tin trong dữ liệu, hãy sử dụng thông tin đó để trả lời, **dù cách diễn đạt khác nhau**.

Trong câu trả lời:
- **Phải trích dẫn đúng thông tin từ dữ liệu** (bao gồm tên tác giả, ngày xuất bản, số báo).
- **Không suy diễn vượt quá nội dung dữ liệu**.

Nếu **hoàn toàn không tìm được nội dung liên quan về mặt ý nghĩa**, hãy ghi đúng câu:
> "Thông tin không bao gồm, vui lòng thử lại."

Nếu tìm được thông tin, hãy trả lời **theo giọng văn của một cây viết nữ của báo *Nữ giới chung* vào năm 1918**:  
văn phong ôn tồn, lễ độ, giàu đạo lý, mang tinh thần khai trí và nữ quyền thời kỳ đầu.

"""


def query_rag(query_text: str) -> str:
    # Connect to Pinecone
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(PINECONE_INDEX_NAME)

    # Get query embedding
    embedding_function = get_embedding_function()
    query_embedding = embedding_function.embed_query(query_text)

    # Search in Pinecone
    results = index.query(
        vector=query_embedding,
        top_k=5,
        namespace=PROJECT_NAMESPACE,
        include_metadata=True
    )

    if not results.matches:
        return "Thông tin không bao gồm, vui lòng thử lại"

    # Extract context from results
    context_text = "\n\n---\n\n".join(
        [match.metadata.get("text", "") for match in results.matches]
    )

    # Generate response
    prompt = ChatPromptTemplate.from_template(
        PROMPT_TEMPLATE
    ).format(
        context=context_text,
        question=query_text
    )

    model = ChatOpenAI(model="gpt-4o")
    response_text = model.invoke(prompt).content

    return response_text
