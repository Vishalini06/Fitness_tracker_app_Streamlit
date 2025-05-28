from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import CharacterTextSplitter
from langchain.llms import HuggingFacePipeline
from langchain.chains import RetrievalQA
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

def load_bot():
    with open("fitness_data.txt", "r", encoding="utf-8") as f:
        content = f.read()

    # Split the text
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_text(content)

    # Vector store
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = FAISS.from_texts(texts, embedding=embeddings)
    retriever = db.as_retriever()

    # ✅ Load model locally using transformers
    model_name = "google/flan-t5-base"  # works fine with text2text when used locally
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

    pipe = pipeline(
        "text2text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=256
    )

    local_llm = HuggingFacePipeline(pipeline=pipe)

    qa_chain = RetrievalQA.from_chain_type(
        llm=local_llm,
        retriever=retriever,
        return_source_documents=False
    )

    return qa_chain
