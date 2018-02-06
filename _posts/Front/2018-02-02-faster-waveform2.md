---
layout: post
title: '[SoundHub] 오디오 파형 로딩 속도 개선하기'
excerpt: Python을 이용하여 생성한 파형 이미지들을 가지고 오디오 파일을 컨트롤할 수 있도록 만들어보자. Wavesurfer.js 를 사용할 때 보다 훨씬 빠르게 페이지를 로드할 수 있다.
project: true
tags:
  - HTML
  - CSS
  - Javascript
  - Audio
  - Wavesurfer
  - SoundHub
  - Project
category: Front-end
---

`Wavesurfer.js` 라이브러리를 1도 쓰지 않고 똑같은 기능을 구현해보았다.  
이미지는 Python 으로 생성하고 CSS 로 겹쳐준 다음 Javascript 로 조정해주었다.

- - -

## HTML

```html
<audio id="file" src="/home/che1/Projects/Django/django_audiomix/temp/user_6/Post_None/author_track/author_track.mp3"></audio>

<button onclick="audio.play()">Play</button>
<button onclick="audio.pause()">Pause</button>

<div id="container" class="wrap">
    <img id="back-image" draggable="false" src="/home/che1/Projects/Django/django_audiomix/temp/user_6/Post_None/author_track/author_track.png" alt="">
    <div id="cutter" class="cutter">
        <img id="cover-image" draggable="false" src="/home/che1/Projects/Django/django_audiomix/temp/user_6/Post_None/author_track/author_track_cover.png" alt="">
    </div>
</div>
```

- - -

## CSS

```css
.wrap {
    position: relative;
    display: inline-block;
    width: 1000px;
    height: 150px;
    margin: 0 auto;
}
.cutter {
    pointer-events: none;
    position: absolute;
    width: 0px;
    height: 100%;
    overflow: hidden;
}
img {
    position: absolute;
}
#cover-image {
    pointer-events: none;
}
```

- - -

## Javascript

```js
// 웨이브폼 이미지
var box = document.getElementById("back-image");
// 웨이브폼을 덮어씌워 색을 입혀주는 div
var cutter = document.getElementById("cutter");
// 오디오 객체
var audio = document.getElementById("file");
// 웨이브폼을 담고있는 div의 가로 길이
var box_width = document.getElementById("back-image").offsetWidth;

// 웨이브폼을 클릭할 경우 getClickPosition 실행
box.addEventListener('click', getClickPosition, false);

// 웨이브폼을 클릭한 위치로 오디오 탐색
function getClickPosition(e) {
    // 이미지 내의 클릭 위치를 계산
    // pageX: 스크린 왼쪽 끝에서부터 클릭 위치까지의 값
    // offsetParent.offsetLeft: 클릭한 요소의 부모 요소가 스크린 왼쪽끝에서부터 떨어져있는 거리 값
    var x = e.pageX - box.offsetParent.offsetLeft;
    console.log(e.pageX, box.offsetParent.offsetLeft);
    // 덮어씌우는 div의 길이를 클릭위치만큼의 픽셀로 변경
    cutter.style.width = x + 'px';
    // 클릭 위치를 박스 전체 길이로 나누어서 클릭 위치의 비율 계산
    var percent_position = x / box_width;
    // 오디오 전체 길이에 클릭 위치 비율을 곱해서 같은 비율의 오디오 재생 위치 계산
    var rel_duration = audio.duration * percent_position;
    // 계산한 상대 위치를 오디오 현재 위치로 지정
    audio.currentTime = rel_duration
}

// 오디오 재생시 웨이브폼 업데이트
// timeupdate 리스너를 등록해서 지속적인 이벤트 발생 캐치
audio.addEventListener('timeupdate', getCurrentTime, false);

// timeupdate 이벤트 발생시 웨이브폼을 업데이트 해주는 함수
function getCurrentTime(e) {
    // 현재 오디오 재생 위치의 비율 값을 계산
    var re_current = audio.currentTime / audio.duration;
    // 계산한 비율을 div의 전체 넓이에 곱해서 구해진 비례 넓이를 덮는 div의 넓이로 설정
    cutter.style.width = (box_width * re_current) +'px'
}
```