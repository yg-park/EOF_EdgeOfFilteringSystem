"""
ㅇ
"""
import os
from langchain_community.llms import Replicate
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import ConversationalRetrievalChain

import whisper
from PyQt5.QtCore import QThread, pyqtSignal

LLAMA2_7B_CHAT = 'meta/llama-2-7b-chat:13c3cdee13ee059ab779f0291d29054dab00a47dad8261375654de5540165fb0'
LLAMA2_7B = "meta/llama-2-7b:77dde5d6c56598691b9008f7d123a18d98f40e4b4978f8a72215ebfc2553ddd8"
REPLICATE_API_TOKEN = 'r8_FC0oSTN78VxAqc8cWbMUSUhJADRPvtG2zFyNu'


class AudioProcessing(QThread):
    """ㅇ"""
    message_signal = pyqtSignal(str)
    model_change_signal = pyqtSignal()
    manual_tts_signal = pyqtSignal()

    AUDIO_FILE_PATH = "resources/received_audio.wav"
    model_change_keywords_kr = ["모델", "바꿔줘"]
    # model_change_keywords_en = ["model", "change"]
    # model_change_keywords = ["switch", "convert", "change", "model"]

    def __init__(self):
        super().__init__()
        self.model = whisper.load_model("base")

    def run(self):
        """ㅇ"""
        stt = self.model.transcribe(self.AUDIO_FILE_PATH, fp16=False)
        print(stt["text"])
        print(stt["language"])

        if stt["language"] == "ko":
            model_change_flag = False
            for keyword in self.model_change_keywords_kr:
                if stt["text"].find(keyword) != -1:
                    model_change_flag = True

            if model_change_flag:
                self.model_change_signal.emit()
            
            #stt_text = stt["text"].strip()
            #print(stt_text)
            self.message_signal.emit(stt["text"])

        elif stt["language"] == "en":
            stt_text = stt["text"].strip()
            # 여기서 LLAMA2 recipes 동작이 필요
            self.llama2_inference(stt_text)

    def llama2_inference(self, text):
        print("라마로 들어왔다")
        # API
        os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

        # 모델 준비
        llama_model = Replicate(
            model=LLAMA2_7B_CHAT,
            model_kwargs={"temperature": 0.95,"top_p": 0.95, "max_new_tokens":500}
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

        chat_history = []
        query = text
        result = chain({"question": query, "chat_history": chat_history})

        response = result['answer']
        response = response[:response.find('\n')]

        print(f"Answer: {response}")
        self.message_signal.emit(response) 
