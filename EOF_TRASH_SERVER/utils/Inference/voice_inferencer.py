"""
whisper와 llama2 recipes를 바탕으로 오디오 파일에 대한 추론 작업을 지원하는 모듈입니다.
"""
import whisper
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import ConversationalRetrievalChain
from langchain.llms.huggingface_pipeline import HuggingFacePipeline
from transformers import LlamaForCausalLM, LlamaTokenizer, pipeline




class VoiceInferencer:
    """Speech To Text, Text Generation을 지원하는 클래스 입니다."""
    def __init__(self):
        self.stt_model = whisper.load_model("medium")
        self.lmm_chain_model = self._init_llama2_recipes()

    def _init_llama2_recipes(self):
        """llama2 모델을 준비합니다."""
        loader = PyPDFLoader("User_Manual.pdf")
        documents = loader.load()

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=20
        )
        all_splits = text_splitter.split_documents(documents)

        model_name = "sentence-transformers/all-mpnet-base-v2"
        model_kwargs = {"device": "cuda"}

        embeddings = HuggingFaceEmbeddings(
            model_name=model_name, model_kwargs=model_kwargs
        )
        vectorstore = FAISS.from_documents(all_splits, embeddings)

        model_id = 'llama-2-7b-hf'

        tokenizer = LlamaTokenizer.from_pretrained(model_id)

        model = LlamaForCausalLM.from_pretrained(
            model_id,
            load_in_4bit=True,
            device_map='auto',
            torch_dtype='auto',
            cache_dir=model_id
        )

        hf_pipeline = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            do_sample=True,
            temperature=0.4,
            top_p=0.85,
            max_new_tokens=50
        )
        hf_llm = HuggingFacePipeline(pipeline=hf_pipeline)

        chain = ConversationalRetrievalChain.from_llm(
            hf_llm, vectorstore.as_retriever(), return_source_documents=True
        )

        return chain

    def get_stt(self, audio_file_path):
        """whisper를 통한 speech to text로 생성된 문자열을 리턴합니다."""
        audio = whisper.load_audio(audio_file_path)
        audio = whisper.pad_or_trim(audio)

        mel = whisper.log_mel_spectrogram(audio).to('cuda')
        # _, probs = self.stt_model.detect_language(mel)
        # print(f"Detected language: {max(probs, key=probs.get)}")

        options = whisper.DecodingOptions(language="en")
        result = whisper.decode(self.stt_model, mel, options)

        # print(result.text)
        return result.text

    def get_llama2_answer(self, text):
        """PDF 사용설명서 기반의 llama2 recipe로 사용자의 질문에 대한 응답을 생성합니다."""
        chat_history = []
        result = self.lmm_chain_model({"question": text, "chat_history": chat_history})

        return result['answer']
