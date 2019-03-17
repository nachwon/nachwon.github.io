---
layout: post
title: '[SoundHub] Web Audio API로 오디오 제어하기'
excerpt: Web Audio API를 이용하여 좀 더 다양한 오디오 제어 기능을 구현 해보자.
project: true
tags:
  - HTML
  - CSS
  - Javascript
  - Audio
  - Web Audio API
  - SoundHub
  - Project
category: Front-end
---

## Web Audio API

> The **Web Audio API** provides a powerful and versatile system for controlling audio on the Web, allowing developers to choose audio sources, add effects to audio, create audio visualizations, apply spatial effects (such as panning) and much more.  
> \- *[Mozilla Web docs](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)*

`Web Audio API` 는 자바스크립트로 오디오 소스에 다양한 변화를 줄 수 있는 시스템이다. 기본적인 음원 로딩, 재생, 정지 뿐만 아니라 패닝, 디스토션, 딜레이 등 여러가지 음향 효과를 추가할 수도 있고, 파형 막대를 그리는 등 음원 데이터의 시각화도 손쉽게 가능하다.  

**Internet Explorer 를 제외한 모든 브라우저에서 지원함.**

- - -

## 왜 Web Audio API를 사용하는가?

웹에서 오디오 소스를 제어하려면 `<audio>` 태그를 통해 오디오를 불러와서 자바스크립트로 오디오 엘리먼트가 기본적으로 가지는 여러 프로퍼티나 이벤트 등을 활용해 손쉽게 제어할 수 있다. 그러나 기본적인 오디오 엘리먼트는 제어할 수 있는 요소가 그리 많지 않다. 만약 구현하고자 하는 오디오 컨트롤링 기능이 재생, 일시정지 등과 같은 단순한 기능이라면 기본적인 오디오 엘리먼트를 사용하는 것이 성능상에서 더 이득이 된다. 그러나 웹에서 좀 더 복잡하고 고차원적인 음원 처리를 필요로 한다면 Web Audio API를 사용한다.

이와 관련한 [Stackoverflow 답변](https://stackoverflow.com/questions/13121250/whats-the-difference-between-web-audio-and-html5-audio-anyway)

- - -

## Web Audio API 동작 과정

Web Audio API의 모든 기능은 `AudioContext` 객체를 생성하면서 시작된다. AudioContext 객체는 내부에 여러 개의 `Audio Node` 들을 가질 수 있다. Audio Node 들은 각각 하나의 역할을 수행하는 모듈들이다. 예를 들어 `GainNode` 는 음원의 볼륨 크기를 조절한다. `PannerNode` 는 음원에 패닝 효과를 적용하고 조절한다. `AnalyserNode` 는 음원으로부터 데이터를 추출한다. 하나의 AudioContext 안에 있는 노드들은 서로 연결되어 `하나의 연결된 그래프(Audio routing graph)` 를 형성하게 된다.  

기본적인 Web Audio API의 흐름은 다음과 같다.

1. `AudioContext` 객체를 생성한다.

2. AudioContext 내부에 오디오 소스를 생성한다. 오디오 소스는 `<audio>` 태그, `Oscillator(발진기)`, Raw PCM 데이터, 실시간 Stream 등이 될 수 있다.

3. 게인, 패너, 리버브, 컴프레서 등 여러가지 이펙터 노드들을 생성한다. 

4. 오디오의 최종 목적지를 정한다. 예를 들면 내 노트북의 스피커

5. 소스 -> 이펙터 노드 -> 목적지 순으로 연결시킨다.

<img src="/img/front/Web_Audio_API/webaudioAPI_en.svg">

- - -

## Javascript로 Web Audio API 사용해보기

Web Audio API로 간단한 볼륨 조절 장치를 만들어보자.

### AudioContext 생성

먼저 AudioContext 객체를 생성하기 위해서는 다음과 같이 한다.

```js
var audioCtx = new AudioContext();
```

아래와 같이 바꿔주면 Webkit/Blink 브라우저를 위한 버전도 포함하여 AudioContext를 생성할 수 있다.
`Safari` 의 경우 `window` 를 통해 생성하지 않으면 작동하지 않을 수 있기 때문에 앞에 window 까지 붙여준다.

```js
var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
```

- - -

### 오디오 소스 불러오기

생성한 AudioContext 안에 오디오 소스를 불러와준다.  

Web Audio API 는 다음과 같은 형태의 음원으로부터 오디오 소스를 불러 올 수 있다.  

- `createMediaElementSource`: audio 태그로부터 불러오기
- `createBufferSource`: Raw PCM 데이터로부터 음원 불러오기. 직접 오디오 파일을 불러오는 방법.
- `createMediaStreamSource`: 설치된 마이크 등에서 실시간으로 음원 데이터를 받아오는 방법.
- `createOscillator`: 자바스크립트로 즉석에서 생성된 음원을 사용하는 방법. 

가장 간단한 방법으로는 페이지 상에 로드된 `<audio>` 태그로부터 음원을 불러오는 방법이다.  

```html
<audio id="audio-source" src="/assets/src/audio.mp3">
```

위와 같은 오디오 태그가 있다고 할 때 아래와 같이 불러올 수 있다.

```js
var audio = document.getElementById("audio-source");

var source = audioCtx.createMediaElementSource(audio);
``` 

- - -

### GainNode 생성

다음으로 생성한 AudioContext 안에 볼륨을 조절할 수 있는 `GainNode` 를 만들어보자.  

```js
var gainNode = audioCtx.createGain();
```

GainNode 는 오디오의 볼륨을 조절하는데 사용한다. 

<img src="/img/front/Web_Audio_API/WebAudioGainNode.png">

GainNode 는 `gain` 이라는 프로퍼티를 가진다.  

볼륨 값을 조절해주기 위해서는 아래와 같이 해준다.  

```js
gainNode.gain.value = 볼륨값
```

볼륨값은 1을 기준으로 1보다 크면 더 커지고 1보다 작으면 작아진다.

- - -

### 연결하기

이제 만들어준 노드들을 서로 연결시켜주면 된다.

순서는 source -> gainNode -> destination 순서이다.

```js
var gainConnected = source.connect(gainNode);
gainConnected.connect(AudioCtx.destination)
```

각 AudioNode 들은 `connect` 메서드를 가지고 있으며 이 메서드는 자기 자신까지 연결된 객체를 반환한다. 따라서 다음 노드를 연결할 때에는 connect 메서드로 반환된 객체를 연결시켜주어야 한다.

가장 마지막으로는 노드들이 포함된 AudioContext의 목적지를 연결해주어야 한다. AudioContext의 `destination` 프로퍼티를 연결해주면 된다.

- - -

### 예제

- HTML

```html
<audio id="audio-source" src="/assets/src/audio.mp3">

<button id="play" onclick="play()">재생</button>
<button id="up" onclick="volumeDown()">볼륨 다운</button>
<button id="down" onclick="volumeUp()">볼륨 업</button>
```

- Javascript

```js
var audio = document.getElementById("audio-source");
var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
var source = audioCtx.createMediaElementSource(audio);
var gainNode = audioCtx.createGain();

var gainConnected = source.connect(gainNode);
gainConnected.connect(audioCtx.destination);

function play() {
    if (audio.paused) {
        audio.play()
    }
    else {
        audio.pause()
    }
}

function volumeUp() {
    
    if (gainNode.gain.value > 2) {
        gainNode.gain.value = 2
    }
    else {
        gainNode.gain.value += 0.2
    }
}

function volumeDown() {
    
    if (gainNode.gain.value < 0) {
        gainNode.gain.value = 0
    }
    else {
        gainNode.gain.value -= 0.2 
    }
}
```

<button id="play" onclick="play()">재생</button>
<button id="up" onclick="volumeDown()">볼륨 다운</button>
<button id="down" onclick="volumeUp()">볼륨 업</button>

- - -

#### Reference

[Mozilla web docs](https://developer.mozilla.org/en-US/docs/Web/API/Web_Audio_API)

<audio id="audio-source" src="/assets/src/audio.mp3">

<script>
var audio = document.getElementById("audio-source");
var audioCtx = new (window.AudioContext || window.webkitAudioContext)();
var source = audioCtx.createMediaElementSource(audio);
var gainNode = audioCtx.createGain();

var gainConnected = source.connect(gainNode);
gainConnected.connect(audioCtx.destination);

function play() {
    if (audio.paused) {
        audio.play()
    }
    else {
        audio.pause()
    }
}

function volumeUp() {
    
    if (gainNode.gain.value > 2) {
        gainNode.gain.value = 2
    }
    else {
        gainNode.gain.value += 0.2
    }
}

function volumeDown() {
    
    if (gainNode.gain.value < 0) {
        gainNode.gain.value = 0
    }
    else {
        gainNode.gain.value -= 0.2 
    }
}

</script>