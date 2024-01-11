"""
whisper와 llama2 recipes를 바탕으로 오디오 파일에 대한 추론 작업을 지원하는 모듈입니다.
"""
import os
import whisper
from langchain_community.llms import Replicate
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain

LLAMA2_7B_CHAT = 'meta/llama-2-7b-chat:13c3cdee13ee059ab779f0291d29054dab00a47dad8261375654de5540165fb0'
LLAMA2_7B = "meta/llama-2-7b:77dde5d6c56598691b9008f7d123a18d98f40e4b4978f8a72215ebfc2553ddd8"
REPLICATE_API_TOKEN = 'r8_FC0oSTN78VxAqc8cWbMUSUhJADRPvtG2zFyNu'


class VoiceInferencer:
    """Speech To Text, Text Generation을 지원하는 클래스 입니다."""
    def __init__(self):
        self.stt_model = whisper.load_model("base")
        self.lmm_chain_model = self._init_llama2_recipes()

    def _init_llama2_recipes(self):
        # API
        os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
        # 모델 준비
        llama_model = Replicate(
            model=LLAMA2_7B_CHAT,
            model_kwargs={"temperature": 0.95, "top_p": 0.95, "max_new_tokens": 500}
        )
        # PDF 파일 준비
        loader = PyPDFLoader("resources/User_Manual.pdf")
        documents = loader.load()
        # PDF 파일 내용 분할 / 벡터화
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20)
        all_splits = text_splitter.split_documents(documents)
        # 자연어 처리에서 텍스트의 특징을 추출하기 위해 벡터화를 해야한다.
        # 허깅페이스에서 제공하는 embedding 모델을 사용
        model_name = "sentence-transformers/all-mpnet-base-v2"
        model_kwargs = {"device": "cpu"}
        embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)
        # FAISS는 고차원 벡터 데이터의 유사성 검색을 빠르게 수행하는 도구
        vectorstore = FAISS.from_documents(all_splits, embeddings)
        # langchain의 chain (대규모 언어 모델과 애플리케이션의 통합을 간소화하는 SDK)
        chain = ConversationalRetrievalChain.from_llm(llama_model, vectorstore.as_retriever(), return_source_documents=True)

        return chain

    def get_stt(self, audio_file_path):
        """whisper를 통한 speech to text로 생성된 문자열을 리턴합니다."""
        stt = self.stt_model.transcribe(audio_file_path, language="ko", fp16=False)
        return stt["text"].strip()

    def get_llama2_answer(self, text):
        """PDF 사용설명서 기반의 llama2 recipe로 사용자의 질문에 대한 응답을 생성합니다."""
        chat_history = []
        result = self.lmm_chain_model({"question": text, "chat_history": chat_history})
        response = result['answer']
        response = response[:response.find('\n')]

        print(f"Answer: {response}")
        return response
