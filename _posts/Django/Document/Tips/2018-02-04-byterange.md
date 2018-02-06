---
layout: post
title: '[SoundHub] HTTP Range Requests'
excerpt: HTTP Range Requests 는 서버에서 전송하는 HTTP 메세지의 일부만을 클라이언트에 전달하는 것을 가능하게 한다. 이런 분할된 요청은 대용량의 미디어 전송이나 파일 다운로드를 처리하는데 유용하며, 미디어의 탐색을 가능하게 한다.
project: true
tags:
  - Django
  - HTTP Range Requests
  - NginX
  - Audio
  - SoundHub
  - Project
category: Django
---

앞서서 오디오 트랙들을 `Wavesurfer.js` 가 아닌 `audio` 태그로 불러오도록 해주어서 페이지 로딩 속도를 크게 향상 시키는데 성공했다. 하지만 또다른 문제가 발생했다. 오디오를 불러오고 파형을 그려서 오디오 파일의 진행 상황을 나타내도록 설정하는 과정에서 오디오 탐색이 안되는 것을 발견했다.  

- - -

## HTML Audio/Video DOM의 currentTime 메서드

`audio` 요소의 `currentTime()` 메서드는 오디오가 재생 중인 현재 시점을 초 단위로 리턴하는데, `currentTime = 초` 와 같이 입력해줄 경우 입력한 초의 위치로 재생 위치을 이동한다. 그런데 이 기능이 작동을 하지 않는 것이다. 파형의 특정 위치를 클릭하면 그 위치의 비율값을 오디오 트랙 전체 길이에 대한 비율 값으로 `currentTime` 함수에 할당해주도록 했는데, 아무리 클릭을 해도 처음 위치로 되돌아갈 뿐이었다.  
분명 따로 만들었던 연습용 html 파일에서는 모든 것이 의도대로 잘 작동했는데 Django runserver 를 통해서0 테스트 해볼 경우 작동을 하지 않았다. 뭔가 javascript 코드를 잘못 짠 것인가 싶어서 오디오 파일에 직접 접근해서 재생시켜보아도 마찬가지 문제가 발생했다. 아예 오디오 탐색 자체가 안되는 것이었다.

- - -

## HTTP Range Requests

삽질을 거듭한 결과 문제의 원인이 `HTTP Range Rquests` 라는 것 때문에 발생하는 것임을 알아냈다.  
`HTTP Range Requests` 는 서버에 HTTP 메세지의 일부만을 요청할 때 사용하는 요청이라고 한다. 오디오나 비디오의 탐색이 가능한 이유가 바로 서버가 Range 요청을 받을 수 있도록 되어있기 때문이라고 한다. `HTTP Response` 헤더에 `Accept-Ranges` 라는 항목이 있으면 해당 서버는 Range 요청을 지원하는 상태임을 알 수 있다.  

runserver 를 열어 두고 프로젝트에서 사용 중인 한 오디오 파일에 요청을 보내보았다.  

```
curl -I localhost:8000/temp/user_2/Post_17/author_track/author_track.mp3
```

```
HTTP/1.0 200 OK
Date: Mon, 05 Feb 2018 10:17:41 GMT
Server: WSGIServer/0.2 CPython/3.6.3
Content-Type: audio/mpeg
Last-Modified: Mon, 05 Feb 2018 06:45:10 GMT
Content-Length: 6415717
X-Frame-Options: SAMEORIGIN
```

`Accept-Ranges` 라는 항목을 찾아볼 수가 없었다.  
다른 탐색이 가능한 오디오 파일의 위치에 요청을 한 번 보내보았다.  

```
curl -I http://www.mule.co.kr/files/2013/8/1/17430924.mp3               
```
```
HTTP/1.1 200 OK
Content-Length: 13903992
Content-Type: audio/mpeg
Last-Modified: Sun, 15 Mar 2015 20:46:46 GMT
Accept-Ranges: bytes
ETag: "beade726615fd01:0"
Date: Mon, 05 Feb 2018 10:42:38 GMT
```

저 위치에 있는 오디오 파일은 탐색이 가능한데 요청을 보내본 결과 정말로 `Accept-Ranges` 라는 항목이 응답 헤더에 담겨있는 것을 볼 수 있다.  
여기서 `Content-Length` 항목은 파일의 전체 길이가 byte 단위로 표시되어있는 것이다.

- - -

## HTTP Range Requests 보내기

Range 요청을 지원하는 서버로 Range 요청을 보내려면 Request 헤더에 `Range` 라는 항목에 다음과 같은 형식으로 입력해서 요청을 보내면 된다.  

- unit: 데이터 단위
- range-start: 범위 시작 지점
- range-end: 범위 끝지점

```
Range: <unit>=<range-start>-
Range: <unit>=<range-start>-<range-end>
Range: <unit>=<range-start>-<range-end>, <range-start>-<range-end>
Range: <unit>=<range-start>-<range-end>, <range-start>-<range-end>, <range-start>-<range-end>
```

하나의 범위를 요청할 수도 있고 동시에 여러 개의 범위를 요청할 수도 있다.  

실제로 한 번 보내보자.  

```
curl http://www.mule.co.kr/files/2013/8/1/17430924.mp3 -i -H "Range: bytes=0-1023"
```
```
HTTP/1.1 206 Partial Content
Content-Type: audio/mpeg
Last-Modified: Sun, 15 Mar 2015 20:46:46 GMT
Accept-Ranges: bytes
ETag: "beade726615fd01:0"
Date: Mon, 05 Feb 2018 10:49:01 GMT
Content-Length: 1024
Content-Range: bytes 0-1023/13903992
```

돌아온 응답은 `206 Partial Content` 라는 상태 코드를 가지는 것을 볼 수 있다.  
`Content-Length` 는 1024로 딱 요청을 보낸 만큼의 길이로 되돌아온 것을 확인할 수 있으며 `Content-Range` 라는 항목에는 요청 보냈던 범위가 표시되어 있는 것을 확인할 수 있었다.  

실제로 크롬 개발자 도구의 네트워크 탭에서 네트워크 활동 로그를 확인해보면 오디오 파일을 탐색할 때 마다 아래와 같은 `206` 상태 코드를 가지는 여러 개의 응답들이 돌아오는 것을 확인 할 수 있었다.  

<image src="/img/http/range.png"></image>  


Range 요청이 성공적으로 처리되었으면 서버는 `206 Partial Content` 라는 메세지를 되돌려준다.  
만약 전체 파일 길이를 넘어서는 범위를 요청하거나 하는 등으로 Range 요청이 실패하면 서버는 `416 Requested Range Not Satisfiable` 이라는 메세지를 되돌려준다.  
서버가 Range 요청을 지원하지 않는 경우에는 `200 OK` 로 응답한다.  


- - -

그럼 왜 runserver 에서는 오디오 탐색이 되지 않았던 것일까? 알아본 바로는 일단 장고는 Range 요청을 지원하지 않는다고 한다. 크롬 브라우저는 `Accept-Ranges` 라는 항목이 응답 헤더에 들어있어야 Range 요청을 처리해주는 것 같은데 장고에서 요청을 받아서 응답을 돌려줄 때 `Accept-Ranges` 항목을 따로 담아주지 않는다. 이걸 해줄려면 커스텀 미들웨어를 작성해서 추가해주어야 할 것 같다. 그리고 굳이 장고에서 이걸 해주지 않아도 상관이 없는 이유는 보통 웹 서버에서 Range 요청을 처리해주기 때문이라고 누군가가 StackOverflow 에 답변을 달아 놓은 것을 보았다.  
그래서 로컬에서는 작동하지 않는 채로 배포를 해보았더니 정말로 오디오 탐색이 정상적으로 작동했다. `NginX` 에서 Range 요청을 처리해주는 것 같다.  
그리고 알 수 없는 이유로 파이어폭스에서는 로컬에서도 오디오 탐색이 정상적으로 작동했다. 뭔가 `Accept-Ranges` 라는 항목이 없어도 알아서 Range 요청을 처리해주는 것 같은데 자세하게 어떤 원리로 오디오 탐색이 정상작동하는 것인지는 좀 더 알아봐야 할 것 같다.  


- - -

#### Reference

[MDN web doc - HTTP Range Requests](https://developer.mozilla.org/en-US/docs/Web/HTTP/Range_requests)  
[MDN web doc - Range](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Range)