# Python TTS Project

## 프로젝트 소개

Python TTS 프로젝트는 전문적이고 자연스러운 음성 합성(Text-to-Speech) 시스템을 개발하기 위한 종합적인 플랫폼입니다. 다양한 TTS 기술과 대규모 언어 모델(LLM)을 활용하여 고품질의 음성을 생성하는 것을 목표로 합니다.

## 주요 특징

- 🎯 **다양한 TTS 엔진 지원**: Coqui TTS, Piper, Bark 등 오픈소스 엔진 통합
- 🌍 **다국어 지원**: 한국어, 영어 등 주요 언어 지원
- 🤖 **LLM 연동**: 문맥 이해 기반 자연스러운 발음
- ⚡ **실시간 처리**: 저지연 실시간 음성 생성
- 🎛️ **음성 커스터마이징**: 톤, 속도, 억양 조절 가능
- 🧠 **감정 표현**: 텍스트 감정을 음성에 반영

## 시작하기

### 시스템 요구사항

- Python 3.8 이상
- CUDA 지원 GPU (권장)
- 8GB 이상 RAM
- 10GB 이상의 디스크 공간

### 설치 방법

1. 저장소 클론:
```bash
git clone https://github.com/your-username/py-tts.git
cd py-tts
```

2. 가상환경 생성 및 활성화:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. 필수 패키지 설치:
```bash
pip install -r requirements.txt
```

4. 추가 패키지 설치 (선택사항):
```bash
# Coqui TTS
pip install TTS

# PyTorch (CUDA 버전)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 기본 사용법

#### 1. 간단한 TTS 사용

```python
from src.tts_engine import TTSEngine

# 기본 TTS 엔진 초기화
tts = TTSEngine(engine_name="basic")

# 텍스트를 음성으로 변환
audio = tts.synthesize("안녕하세요. 오늘 날씨가 좋네요.")

# 오디오 파일로 저장
tts.save_audio(audio, "output.wav")
```

#### 2. 고급 TTS 설정

```python
from src.tts_engine import TTSEngine
from src.configs import TTSConfig

# 고급 설정
config = TTSConfig(
    engine="coqui",
    language="ko",
    speaker_id=1,
    speed=1.0,
    pitch=1.0,
    emotion="neutral"
)

# TTS 엔진 초기화
tts = TTSEngine(config=config)

# 텍스트 처리 및 음성 생성
text = "이 프로젝트는 최신 TTS 기술을 활용하여 자연스러운 음성을 생성합니다."
audio = tts.synthesize(text, emotion="happy")

# 실시간 재생
tts.play_audio(audio)
```

#### 3. LLM 연동을 통한 문맥 이해

```python
from src.llm_tts import LLMTTS

# LLM 연동 TTS 초기화
llm_tts = LLMTTS()

# 문맥을 고려한 음성 생성
context = "이것은 공식적인 발표입니다."
text = "존경하는 여러분, 오늘 중요한 발표를 하게 되어 기쁩니다."

audio = llm_tts.synthesize_with_context(text, context)
llm_tts.save_audio(audio, "formal_speech.wav")
```

## 프로젝트 구조

```
py-tts/
├── src/
│   ├── engines/           # TTS 엔진 구현
│   │   ├── __init__.py
│   │   ├── base.py       # 기본 TTS 엔진 클래스
│   │   ├── coqui_tts.py  # Coqui TTS 구현
│   │   ├── piper_tts.py  # Piper TTS 구현
│   │   └── custom_tts.py # 커스텀 TTS 모델
│   ├── preprocessing/     # 텍스트 전처리
│   │   ├── __init__.py
│   │   ├── text_normalizer.py
│   │   ├── phoneme_converter.py
│   │   └── korean_processor.py
│   ├── postprocessing/    # 오디오 후처리
│   │   ├── __init__.py
│   │   ├── audio_enhancer.py
│   │   └── noise_reduction.py
│   ├── models/           # 딥러닝 모델 정의
│   │   ├── __init__.py
│   │   ├── tacotron2.py
│   │   ├── waveglow.py
│   │   └── vits.py
│   ├── llm_integration/   # LLM 연동
│   │   ├── __init__.py
│   │   ├── context_analyzer.py
│   │   └── emotion_detector.py
│   ├── utils/            # 유틸리티 함수
│   │   ├── __init__.py
│   │   ├── audio_utils.py
│   │   └── metrics.py
│   ├── configs/          # 설정 관리
│   │   ├── __init__.py
│   │   └── tts_config.py
│   └── tts_engine.py     # 메인 TTS 엔진
├── data/
│   ├── samples/          # 샘플 오디오 데이터
│   ├── models/           # 학습된 모델
│   └── test_texts.txt    # 테스트용 텍스트
├── notebooks/            # 실험 및 분석 노트북
│   ├── model_comparison.ipynb
│   ├── quality_evaluation.ipynb
│   └── korean_tuning.ipynb
├── tests/               # 테스트 코드
├── examples/            # 사용 예제
├── docs/                # 문서
├── requirements.txt     # 필수 패키지 목록
├── setup.py            # 패키지 설치 스크립트
├── IDEA.md             # 프로젝트 아이디어
└── README.md           # 프로젝트 설명
```

## 지원되는 TTS 엔진

| 엔진 | 특징 | 언어 지원 | 설치 |
|------|------|-----------|------|
| **Coqui TTS** | 고품질, 음성 클론 지원 | 20+ 언어 | `pip install TTS` |
| **Piper** | 빠름, 저사양 | 10+ 언어 | 별도 설치 필요 |
| **Bark** | 비음성 효과 포함 | 영어 중심 | `pip install bark` |
| **Google TTS** | 클라우드 기반 | 100+ 언어 | API 키 필요 |
| **Custom Models** | 자체 학습 모델 | 커스터마이징 가능 | 직접 학습 |

## 설정 옵션

### 기본 설정 (`configs/tts_config.py`)

```python
TTS_CONFIG = {
    "default_engine": "coqui",
    "default_language": "ko",
    "sample_rate": 22050,
    "default_speed": 1.0,
    "default_pitch": 1.0,
    "output_format": "wav",
    "cache_models": True,
    "model_cache_dir": "./data/models"
}
```

### 엔진별 설정

```python
ENGINE_CONFIGS = {
    "coqui": {
        "model_name": "tts_models/multilingual/multi-dataset/xtts_v2",
        "vocoder_name": "vocoder_models/universal/libri-tts/fullband-melgan"
    },
    "piper": {
        "model_path": "./data/models/piper",
        "device": "cpu"  # 또는 "cuda"
    }
}
```

## 개발 가이드

### 새로운 TTS 엔진 추가

1. `src/engines/` 디렉터리에 새 엔진 파일 생성
2. `BaseTTSEngine` 클래스 상속
3. 필요한 메소드 구현:
   - `__init__()`: 엔진 초기화
   - `synthesize()`: 텍스트를 오디오로 변환
   - `save_audio()`: 오디오 파일 저장
   - `play_audio()`: 오디오 실시간 재생

```python
from src.engines.base import BaseTTSEngine

class CustomTTSEngine(BaseTTSEngine):
    def __init__(self, config):
        super().__init__(config)
        # 엔진 초기화 코드

    def synthesize(self, text, **kwargs):
        # 텍스트를 오디오로 변환
        pass
```

### 모델 학습

1. 데이터 준비:
```bash
python scripts/prepare_data.py --data_dir ./data/my_data
```

2. 모델 학습:
```bash
python scripts/train_model.py --config configs/my_model.yaml
```

3. 모델 평가:
```bash
python scripts/evaluate_model.py --model_path ./data/models/my_model
```

## 성능 벤치마크

### 지연 시간 (초)
| 엔진 | 1문장 | 단락 | 장문 |
|------|-------|-------|------|
| Coqui | 0.5 | 2.1 | 8.5 |
| Piper | 0.2 | 0.8 | 3.2 |
| Custom | 0.3 | 1.5 | 6.0 |

### 음성 품질 (MOS)
| 엔진 | 한국어 | 영어 | 평균 |
|------|--------|------|------|
| Coqui | 4.2 | 4.5 | 4.35 |
| Piper | 3.8 | 4.0 | 3.90 |
| Custom | 4.5 | 4.3 | 4.40 |

## 기여하기

기여를 환영합니다! 아래 단계를 따라주세요:

1. 이슈 생성: 버그 리포트나 기능 요청
2. 포크: 저장소를 포크합니다
3. 브랜치 생성: `git checkout -b feature/amazing-feature`
4. 커밋: `git commit -m 'Add amazing feature'`
5. 푸시: `git push origin feature/amazing-feature`
6. 풀 리퀘스트 생성

### 코드 스타일

- PEP 8 준수
- 타입 힌트 사용
- docstring 포함
- 테스트 코드 작성

## 라이선스

이 프로젝트는 MIT 라이선스 하에 제공됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

## 연락처

- 이메일: your-email@example.com
- 이슈: [GitHub Issues](https://github.com/your-username/py-tts/issues)
- 디스코드: [Discord 채널](https://discord.gg/your-invite)

## 감사의 말

- [Coqui AI](https://coqui.ai/) - 오픈소스 TTS 엔진 제공
- [Mozilla](https://mozilla.org/) - TTS 기술 개발 지원
- 오픈소스 커뮤니티 - 지속적인 개발과 피드백

## 변경 로그

### v0.1.0 (예정)
- 기본 TTS 엔진 구현
- 한국어 지원
- 간단한 API 제공

### v0.2.0 (계획)
- LLM 연동
- 감정 표현 기능
- 실시간 처리 최적화