"""
whisper와 llama2 recipes를 바탕으로 오디오 파일에 대한 추론 작업을 지원하는 모듈입니다.
"""
import os
import configparser

import whisper
from googletrans import translate
from langchain_community.llms import Replicate
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain


class VoiceInferencer:
    """Speech To Text, Text Generation을 지원하는 클래스 입니다."""

    config = configparser.ConfigParser()
    config.read("resources/api_tokens.ini")

    def __init__(self):
        self.stt_model = whisper.load_model("medium")
        self.lmm_chain_model = self._init_llama2_recipes()

    def _init_llama2_recipes(self):
        # API
        os.environ["REPLICATE_API_TOKEN"] = \
            self.config["REPLICATE"]["API_TOKEN"]

        # 모델 준비
        llama_model = Replicate(
            model=self.config["LLAMA2"]["7B"],
            model_kwargs={"temperature": 0.4, "top_p": 0.85, "max_new_tokens": 50}
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
        model_kwargs = {"device": "cuda"}
        embeddings = HuggingFaceEmbeddings(model_name=model_name, model_kwargs=model_kwargs)
        # FAISS는 고차원 벡터 데이터의 유사성 검색을 빠르게 수행하는 도구
        vectorstore = FAISS.from_documents(all_splits, embeddings)
        # langchain의 chain (대규모 언어 모델과 애플리케이션의 통합을 간소화하는 SDK)
        chain = ConversationalRetrievalChain.from_llm(llama_model, vectorstore.as_retriever(), return_source_documents=True)

        return chain

    def get_stt(self, audio_file_path):
        """whisper를 통한 speech to text로 생성된 문자열을 리턴합니다."""
        audio = whisper.load_audio(audio_file_path)
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to('cuda')

        options = whisper.DecodingOptions(language="en")
        result = whisper.decode(self.stt_model, mel, options)

        return result.text.lower()

    def get_llama2_answer(self, text):
        """PDF 사용설명서 기반의 llama2 recipe로 사용자의 질문에 대한 응답을 생성합니다."""
        chat_history = []
        result = self.lmm_chain_model({"question": text, "chat_history": chat_history})
        response = result['answer']
        response = response[:response.find('\n')]

        response = translate(response, "ko")
        return response
